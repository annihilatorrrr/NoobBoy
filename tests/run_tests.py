#!/usr/bin/env python3
"""NoobBoy Test Suite Runner

Discovers test ROMs, runs them headlessly via the NoobBoyTester binary,
and reports results to the terminal, a markdown file, and README badges.
"""

import argparse
import dataclasses
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import zipfile
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
TESTROMS_DIR = SCRIPT_DIR / "testroms"
CONFIG_PATH = SCRIPT_DIR / "config.json"
RESULTS_JSON_PATH = SCRIPT_DIR / "results.json"
TESTS_MD_PATH = SCRIPT_DIR / "TESTS.md"
README_PATH = PROJECT_DIR / "README.md"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_DOWN = "\033[J"
IS_TTY = sys.stdout.isatty()

SPINNER_CHARS = "⠋⠙⠹⠸⠼⠴⠦⠧"


class Status(Enum):
    """Possible outcomes for a single test ROM."""
    PASS = "pass"
    FAIL = "fail"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"
    CRASH = "crash"


STATUS_ICON = {
    Status.PASS:    f"{GREEN}✓{RESET}",
    Status.FAIL:    f"{RED}✗{RESET}",
    Status.TIMEOUT: f"{YELLOW}T{RESET}",
    Status.SKIPPED: f"{DIM}–{RESET}",
    Status.CRASH:   f"{RED}!{RESET}",
}

STATUS_MD_ICON = {
    Status.PASS: "✅", Status.FAIL: "❌", Status.TIMEOUT: "⏱",
    Status.SKIPPED: "⊘", Status.CRASH: "💥",
}


@dataclass
class TestInfo:
    """Metadata for a discovered test ROM."""
    path: str
    rel: str
    name: str
    suite: str
    subsuite: str
    is_gbc: bool
    
    def as_skipped(self, reason: str) -> "TestResult":
            """Convenience method to convert metadata into a skipped result."""
            return TestResult(
                name=self.name,
                rel=self.rel,
                suite=self.suite,
                subsuite=self.subsuite,
                status=Status.SKIPPED,
                reason=reason
            )

@dataclass
class TestResult:
    """Result of running a single test ROM."""
    name: str
    rel: str
    suite: str
    subsuite: str
    status: Status
    serial: str = ""
    reason: Optional[str] = None


def load_config() -> dict:
    """Load test suite configuration from config.json."""
    with open(CONFIG_PATH) as fh:
        return json.load(fh)


def get_suite_config(config: dict, suite_name: str) -> dict:
    """Return config for a suite, falling back to its top-level parent."""
    suites = config.get("suites", {})
    
    if suite_name in suites:
        return suites[suite_name]

    return suites.get(suite_name.split("/")[0], {})


def discover_tests(filter_pattern: Optional[str] = None) -> list[TestInfo]:
    """Find all .gb/.gbc test ROMs under TESTROMS_DIR, optionally filtered by path prefix."""
    tests = []
    for rom_path in sorted(TESTROMS_DIR.rglob("*.gb*")):
        if not rom_path.is_file() or rom_path.suffix.lower() not in (".gb", ".gbc"):
            continue

        relative = rom_path.relative_to(TESTROMS_DIR)
        relative_str = str(relative)

        if filter_pattern and not relative_str.startswith(filter_pattern):
            continue

        parts = relative.parts
        test_info = TestInfo(
            path=str(rom_path),
            rel=relative_str,
            name=rom_path.name,
            suite=parts[0] if len(parts) > 1 else "",
            subsuite="/".join(parts[:-1]),
            is_gbc=rom_path.suffix.lower() == ".gbc",
        )
        tests.append(test_info)

    return tests


def run_single_test(binary: str, info_dict: dict, config: dict) -> dict:
    """Run one test ROM headlessly. Uses plain dicts for process-pool pickling."""
    suite_conf = get_suite_config(config, info_dict["suite"])
    timeout_cycles = suite_conf.get("timeout_cycles", config.get("default_timeout_cycles", 100_000_000))
    wall_timeout = suite_conf.get("wall_timeout_seconds", config.get("default_process_timeout_seconds", 120))

    cmd = [
        binary, "--headless",
        "--rom", info_dict["path"],
        "--timeout", str(timeout_cycles),
        "--detection", suite_conf.get("detection", "auto"),
    ]

    base_result = {
        "name": info_dict["name"],
        "rel": info_dict["rel"],
        "suite": info_dict["suite"],
        "subsuite": info_dict["subsuite"],
    }

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=wall_timeout)
        status, serial = "fail", ""
        for line in proc.stdout.splitlines():
            if line.startswith("SERIAL:"):
                serial = line[len("SERIAL:"):]
            elif line.startswith("RESULT:"):
                tag = line[len("RESULT:"):].strip().upper()
                if tag in ("PASS", "FAIL", "TIMEOUT"):
                    status = tag.lower()

        if proc.returncode != 0 and status == "fail":
            status = "crash"

        return {**base_result, "status": status, "serial": serial}
    except subprocess.TimeoutExpired:
        return {**base_result, "status": "timeout", "serial": "", "reason": f"Wall-clock timeout ({wall_timeout}s)"}
    except Exception as exc:
        return {**base_result, "status": "crash", "serial": "", "reason": str(exc)}


def dict_to_result(raw: dict) -> TestResult:
    """Convert a result dict from the subprocess back to a TestResult."""
    return TestResult(
        name=raw["name"],
        rel=raw["rel"],
        suite=raw["suite"],
        subsuite=raw["subsuite"],
        status=Status(raw["status"]),
        serial=raw.get("serial", ""),
        reason=raw.get("reason"),
    )


class LiveDisplay:
    """Animated terminal display showing suite progress and active tests during execution."""
    def __init__(self, suite_stats: dict, total: int, workers: int):
        self._visible_suites = sorted(
            suite for suite, stats in suite_stats.items() if stats["runnable"] > 0
        )
        self._suite_stats = suite_stats
        self._total = total
        self._workers = workers
        self._completed_count = 0
        self._pending_rels: list[str] = []
        self._done_rels: set[str] = set()
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._frame = 0
        self._drawn_lines = 0
        self._thread: Optional[threading.Thread] = None

    def set_pending(self, rels: list[str]):
        """Set the ordered list of pending test paths."""
        with self._lock:
            self._pending_rels = list(rels)

    def start(self):
        """Start the render thread."""
        if IS_TTY:
            sys.stdout.write(HIDE_CURSOR)
            sys.stdout.flush()

        self._thread = threading.Thread(target=self._render_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop rendering and clear the display area."""
        self._stop_event.set()

        if self._thread:
            self._thread.join()

        self._erase()

        if IS_TTY:
            sys.stdout.write(SHOW_CURSOR)
            sys.stdout.flush()

    def mark_done(self, result: TestResult):
        """Update stats when a test completes."""
        with self._lock:
            self._done_rels.add(result.rel)
            self._completed_count += 1
            if result.status == Status.PASS:
                stats = self._suite_stats.get(result.suite)
                if stats:
                    stats["passed"] += 1

    def _render_loop(self):
        while not self._stop_event.is_set():
            self._render()
            self._stop_event.wait(0.08)
            self._frame += 1

    def _render(self):
        if not IS_TTY:
            return

        with self._lock:
            output_lines = []

            for suite in self._visible_suites:
                stats = self._suite_stats[suite]
                passed, runnable = stats["passed"], stats["runnable"]
                if passed == runnable and runnable > 0:
                    color = GREEN
                elif passed > 0:
                    color = YELLOW
                else:
                    color = DIM
                output_lines.append(f"  {suite:<28} {color}{passed:>3}/{runnable}{RESET}")

            output_lines.append("")

            active_rels = [
                rel for rel in self._pending_rels if rel not in self._done_rels
            ][:self._workers]
            spinner_char = SPINNER_CHARS[self._frame % len(SPINNER_CHARS)]
            for rel in active_rels:
                display_name = rel if len(rel) <= 55 else "…" + rel[-54:]
                output_lines.append(f"  {YELLOW}{spinner_char}{RESET} {DIM}{display_name}{RESET}")

            queued_count = len(self._pending_rels) - len(self._done_rels) - len(active_rels)
            if queued_count > 0:
                output_lines.append(f"    {DIM}+{queued_count} queued{RESET}")

            output_lines.append("")
            percent = (self._completed_count * 100 // self._total) if self._total else 100
            output_lines.append(f"  {self._completed_count}/{self._total} completed ({percent}%)")

            self._erase()
            sys.stdout.write("\n".join(output_lines) + "\n")
            sys.stdout.flush()
            self._drawn_lines = len(output_lines)

    def _erase(self):
        if self._drawn_lines > 0:
            sys.stdout.write(f"\033[{self._drawn_lines}A\r{CLEAR_DOWN}")
            sys.stdout.flush()
            self._drawn_lines = 0


def count_statuses(results: list[TestResult]) -> dict[str, int]:
    """Return a dict with counts per status value, plus 'total'."""
    counts = defaultdict(int)

    for result in results:
        counts[result.status.value] += 1

    counts["total"] = len(results)
    return counts


def print_grouped_results(results: list[TestResult], verbose: bool = False):
    """Print results grouped by subsuite with right-aligned pass counts."""
    by_subsuite: dict[str, list[TestResult]] = defaultdict(list)
    for result in results:
        by_subsuite[result.subsuite].append(result)

    pad_width = 50

    for subsuite in sorted(by_subsuite):
        group = by_subsuite[subsuite]
        passed = sum(result.status == Status.PASS for result in group)
        skipped = sum(result.status == Status.SKIPPED for result in group)
        total = len(group)
        runnable = total - skipped

        display_name = subsuite or "(root)"
        padding = max(2, pad_width - len(display_name))

        if skipped == total:
            label = f"{DIM}SKIP{RESET}"
            print(f"  {BOLD}{display_name}{RESET}{' ' * padding}{label}")
            reasons = sorted(set(result.reason or "Skipped" for result in group))
            for reason in reasons:
                print(f"     {DIM}{reason}{RESET}")
        elif passed == runnable:
            label = f"{GREEN}{passed}/{runnable}  PASS{RESET}"
            print(f"  {BOLD}{display_name}{RESET}{' ' * padding}{label}")
        else:
            color = YELLOW if passed > 0 else RED
            label = f"{color}{passed}/{runnable}{RESET}"
            print(f"  {BOLD}{display_name}{RESET}{' ' * padding}{label}")

            for result in group:
                if result.status in (Status.PASS, Status.SKIPPED):
                    continue
                icon = STATUS_ICON[result.status]
                print(f"     {icon} {result.name}")
                
                if not verbose or not result.serial:
                    continue

                for serial_line in result.serial.splitlines()[:5]:
                    print(f"       {DIM}{serial_line}{RESET}")

        print()


def print_summary(results: list[TestResult], elapsed: float, workers: int):
    """Print an aligned summary block."""
    counts = count_statuses(results)
    divider = "-" * 40

    print(f"  {BOLD}Summary{RESET}")
    print(f"  {divider}")

    rows = [
        ("Total",   counts["total"],   BOLD),
        ("Passed",  counts["pass"],    GREEN),
        ("Failed",  counts["fail"],    RED),
        ("Timeout", counts["timeout"], YELLOW),
        ("Skipped", counts["skipped"], DIM),
        ("Crashed", counts["crash"],   RED),
    ]
    for label, value, color in rows:
        if value > 0 or label == "Total":
            print(f"  {label:<12} {color}{value:>5}{RESET}")

    print(f"  {divider}")
    print(f"  {DIM}{elapsed:.1f}s · {workers} workers{RESET}")
    print()


def generate_tests_md(results: list[TestResult]):
    """Write tests/TESTS.md with a redesigned per-suite report."""
    counts = count_statuses(results)
    total_runnable = counts["total"] - counts["skipped"]
    pass_rate = (counts["pass"] / total_runnable * 100) if total_runnable else 0

    lines = [
        "# NoobBoy — Test Results",
        "",
        f"> Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"**{counts['pass']}** of **{total_runnable}** runnable tests passing ({pass_rate:.0f}%)",
        f" · {counts['skipped']} skipped",
        "",
        "| | Count |",
        "|---|--:|",
        f"| Passed | {counts['pass']} |",
        f"| Failed | {counts['fail']} |",
        f"| Timeout | {counts['timeout']} |",
        f"| Crashed | {counts['crash']} |",
        f"| Skipped | {counts['skipped']} |",
        f"| **Total** | **{counts['total']}** |",
        "",
        "---",
        "",
    ]

    by_subsuite = defaultdict(list)
    for result in results:
        by_subsuite[result.subsuite].append(result)

    current_suite = None
    for subsuite in sorted(by_subsuite):
        group = by_subsuite[subsuite]
        suite = group[0].suite
        passed = sum(result.status == Status.PASS for result in group)
        skipped = sum(result.status == Status.SKIPPED for result in group)
        total = len(group)
        runnable = total - skipped

        if suite != current_suite:
            if current_suite is not None:
                lines.append("---")
                lines.append("")
            lines.append(f"## {suite}")
            lines.append("")
            current_suite = suite

        heading = "General"
        if subsuite != suite:
            heading = "/".join(subsuite.split("/")[1:])

        if skipped == total:
            lines.append(f"### {heading}")
            lines.append("")
            lines.append(f"*{group[0].reason or 'Skipped'}*")
            lines.append("")
            continue

        status_label = "✅" if passed == runnable else ""
        lines.append(f"### {heading} — {passed}/{runnable} {status_label}")
        lines.append("")

        has_failures = any(result.status not in (Status.PASS, Status.SKIPPED) for result in group)
        if passed == runnable:
            lines.append("All tests passing.")
            lines.append("")
            continue

        lines.append("<details>")
        if has_failures:
            lines.append("<summary>Details</summary>")
        lines.append("")
        lines.append("| Test | Result |")
        lines.append("|---|---|")
        for result in sorted(group, key=lambda r: r.name):
            icon = STATUS_MD_ICON.get(result.status, "?")
            lines.append(f"| {result.name} | {icon} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    TESTS_MD_PATH.write_text("\n".join(lines) + "\n")


def save_results_json(results: list[TestResult]):
    """Write tests/results.json with structured data."""
    counts = count_statuses(results)

    suites_data: dict = defaultdict(lambda: defaultdict(list))
    for result in results:
        sub_key = "/".join(result.subsuite.split("/")[1:]) or "(root)"
        suites_data[result.suite][sub_key].append({
            "name": result.name,
            "status": result.status.value,
            "serial": result.serial,
            "reason": result.reason or "",
        })

    with open(RESULTS_JSON_PATH, "w") as fh:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {key: counts[key] for key in ("total", "pass", "fail", "timeout", "skipped", "crash")},
            "suites": {key: dict(val) for key, val in suites_data.items()},
        }, fh, indent=2)


def update_readme_badges(results: list[TestResult]):
    """Update shields.io badges between TEST_BADGES markers in README.md."""
    if not README_PATH.exists():
        return

    readme_text = README_PATH.read_text()
    badge_pattern = r"(<!-- TEST_BADGES_START -->).*?(<!-- TEST_BADGES_END -->)"
    if not re.search(badge_pattern, readme_text, flags=re.DOTALL):
        return

    suite_stats: dict = defaultdict(lambda: {"passed": 0, "total": 0})
    for result in results:
        if result.status == Status.SKIPPED:
            continue

        stats = suite_stats[result.suite]
        stats["total"] += 1
        stats["passed"] += int(result.status == Status.PASS)

    badges = []
    for suite in sorted(suite_stats):
        passed, total = suite_stats[suite]["passed"], suite_stats[suite]["total"]
        if total == 0:
            continue
        ratio = passed / total
        colour = "brightgreen" if ratio >= 0.8 else ("yellow" if ratio >= 0.5 else "red")
        badge_label = quote(suite, safe="")
        badge_value = quote(f"{passed}/{total}", safe="")
        badges.append(f"![{suite}](https://img.shields.io/badge/{badge_label}-{badge_value}-{colour})")

    badge_block = "\n" + " ".join(badges) + "\n" if badges else "\n"
    updated = re.sub(badge_pattern, rf"\1{badge_block}\2", readme_text, flags=re.DOTALL)
    README_PATH.write_text(updated)


def extract_testroms():
    """Extract testroms.zip into tests/testroms/ if the directory is empty or missing."""
    if TESTROMS_DIR.exists() and any(TESTROMS_DIR.iterdir()):
        return

    zip_path = SCRIPT_DIR / "testroms.zip"
    if not zip_path.exists():
        print(f"{RED}Error: tests/testroms.zip not found.{RESET}")
        sys.exit(1)

    print(f"{DIM}Extracting test ROMs...{RESET}")
    TESTROMS_DIR.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(TESTROMS_DIR)


def setup_signal_handler():
    """Catch exit signals cleanly without traceback dumps."""
    def handler(_sig, _frame):
        if IS_TTY:
            sys.stdout.write(SHOW_CURSOR)

        print(f"\n  {RED}Interrupted.{RESET}\n")
        sys.exit(1)

    signal.signal(signal.SIGINT, handler)


def list_suites(config: dict):
    """Print available test suites from config.json."""
    suites = config.get("suites", {})
    print(f"\n  {BOLD}Available suites:{RESET}\n")
    for name in sorted(suites):
        suite_conf = suites[name]
        if suite_conf.get("skip"):
            detail = f"{DIM}(skipped: {suite_conf.get('skip_reason', '')}){RESET}"
        else:
            detail = f"detection={suite_conf.get('detection', 'auto')}"
        print(f"    {name:<30} {detail}")
    print()


def list_tests():
    """Print all discovered test ROM paths."""
    tests = discover_tests()
    if not tests:
        print(f"{YELLOW}No tests found.{RESET}")
        return
    
    print(f"\n  {BOLD}{len(tests)} test ROMs:{RESET}\n")
    for test in tests:
        suffix = f"  {DIM}(GBC){RESET}" if test.is_gbc else ""
        print(f"    {test.rel}{suffix}")
    print()


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="run_tests.py",
        description="Run the NoobBoy test suite against ROM-based tests.",
    )
    parser.add_argument("--binary",
                        default=str(PROJECT_DIR / "build" / "tester" / "NoobBoyTester"),
                        help="path to NoobBoyTester binary")
    parser.add_argument("--filter", metavar="PREFIX",
                        help="filter tests by path prefix (e.g. 'blargg', 'mooneye/acceptance/timer')")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show serial output for failing tests")
    parser.add_argument("-j", "--jobs", type=int, default=None, metavar="N",
                        help="parallel workers (default: CPU count)")
    parser.add_argument("--report", action="store_true", help="Generate TESTS.md and results.json reports")
    parser.add_argument("--badges", action="store_true", help="Update README badges")
    parser.add_argument("--list-suites", action="store_true",
                        help="list available test suites and exit")
    parser.add_argument("--list-tests", action="store_true",
                        help="list all discovered test ROMs and exit")
    return parser


def main():
    """Entry point."""
    setup_signal_handler()
    parser = build_parser()
    args = parser.parse_args()

    config = load_config()

    if args.list_suites:
        list_suites(config)
        return

    extract_testroms()
        
    if args.list_tests:
        list_tests()
        return

    if not os.path.isfile(args.binary):
        print(f"{RED}Error: binary not found at {args.binary}{RESET}")
        print("Run 'make test' or 'make tester' first.")
        sys.exit(1)

    all_tests = discover_tests(args.filter)
    if not all_tests:
        print(f"{YELLOW}No tests found.{RESET}")

        if args.filter:
            print(f"  Filter: {args.filter}")
            
        sys.exit(0)

    all_results: list[TestResult] = []
    runnable_tests: list[TestInfo] = []
    for info in all_tests:
        suite_conf = get_suite_config(config, info.suite)
        
        reason = None
        if info.is_gbc:
            reason = "GBC ROM (DMG only)"
        elif suite_conf.get("skip"):
            reason = suite_conf.get("skip_reason", "Skipped")

        if not reason:
            runnable_tests.append(info)
            continue
        
        # Create the skipped test result
        skipped_result = TestResult(
            info.name, info.rel, info.suite, info.subsuite,
            Status.SKIPPED, reason=reason
        )
        all_results.append(skipped_result)

    suite_count = len({test.suite for test in all_tests})
    workers = args.jobs or min(os.cpu_count() or 4, max(1, len(runnable_tests)))

    print()
    print(f"  {BOLD}NoobBoy Test Suite{RESET}")
    print(f"  {'-' * 40}")
    print(f"  {len(all_tests)} tests · {suite_count} suites · {workers} workers")
    print(f"  {'-' * 40}")
    print()

    elapsed = 0
    if runnable_tests:
        suite_stats: dict[str, dict] = defaultdict(lambda: {"passed": 0, "runnable": 0})
        for info in runnable_tests:
            suite_stats[info.suite]["runnable"] += 1

        display = LiveDisplay(dict(suite_stats), len(runnable_tests), workers)
        display.set_pending([test.rel for test in runnable_tests])
        display.start()

        run_results: list[TestResult] = []
        start_time = time.time()

        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(run_single_test, args.binary, dataclasses.asdict(info), config): info
                for info in runnable_tests
            }
            for future in as_completed(futures):
                result = dict_to_result(future.result())
                run_results.append(result)
                display.mark_done(result)

        display.stop()

        all_results += run_results
        elapsed = time.time() - start_time

    print_grouped_results(all_results, verbose=args.verbose)
    print_summary(all_results, elapsed, workers)

    if args.report:
        save_results_json(all_results)
        generate_tests_md(all_results)
        print(f"  {DIM}Report:  {TESTS_MD_PATH.relative_to(PROJECT_DIR)}{RESET}")
        print(f"  {DIM}Results: {RESULTS_JSON_PATH.relative_to(PROJECT_DIR)}{RESET}")

    if args.badges:
        update_readme_badges(all_results)
        print(f"  {DIM}Badges:  README.md updated{RESET}")

    print()

    if any(result.status not in (Status.PASS, Status.SKIPPED) for result in all_results):
        print(f"  {RED}Some tests failed.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
