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
CYAN = "\033[96m"
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
    HANG = "hang"
    ERROR = "error"


STATUS_ICON = {
    Status.PASS:    f"{GREEN}✓{RESET}",
    Status.FAIL:    f"{RED}✗{RESET}",
    Status.TIMEOUT: f"{YELLOW}T{RESET}",
    Status.SKIPPED: f"{DIM}–{RESET}",
    Status.CRASH:   f"{RED}!{RESET}",
    Status.HANG:    f"{YELLOW}H{RESET}",
    Status.ERROR:   f"{RED}E{RESET}",
}

STATUS_MD_LABEL = {
    Status.PASS: "Pass",
    Status.FAIL: "**FAIL**",
    Status.TIMEOUT: "Timeout",
    Status.SKIPPED: "Skipped",
    Status.CRASH: "**CRASH**",
    Status.HANG: "Hang",
    Status.ERROR: "**ERROR**",
}

STATUS_MD_ICON = {
    Status.PASS:    '<span style="color:green">✓</span>',
    Status.FAIL:    '<span style="color:orangered">✗</span>',
    Status.TIMEOUT: '<span style="color:goldenrod">T</span>',
    Status.SKIPPED: '<span style="color:gray">–</span>',
    Status.CRASH:   '<span style="color:orangered">!</span>',
    Status.HANG:    '<span style="color:goldenrod">H</span>',
    Status.ERROR:   '<span style="color:red">E</span>',
}

STATUS_MD_COLOR = {
    Status.PASS:    'green',
    Status.FAIL:    'orangered',
    Status.TIMEOUT: 'goldenrod',
    Status.SKIPPED: 'gray',
    Status.CRASH:   'orangered',
    Status.HANG:    'goldenrod',
    Status.ERROR:   'red',
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
        return TestResult(
            name=self.name,
            rel=self.rel,
            suite=self.suite,
            subsuite=self.subsuite,
            status=Status.SKIPPED,
            reason=reason,
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
    with open(CONFIG_PATH) as fh:
        return json.load(fh)


def get_suite_config(config: dict, rel: str, suite: str, subsuite: str = "") -> dict:
    suites = config.get("suites", {})
    
    if rel in suites:
        return suites[rel]
    
    if subsuite and subsuite in suites:
        return suites[subsuite]
    
    if suite in suites:
        return suites[suite]
        
    return suites.get(suite.split("/")[0], {})

def discover_tests(filter_pattern: Optional[str] = None) -> list[TestInfo]:
    tests = []
    for rom_path in sorted(TESTROMS_DIR.rglob("*.gb*")):
        if not rom_path.is_file() or rom_path.suffix.lower() not in (".gb", ".gbc"):
            continue
        relative = rom_path.relative_to(TESTROMS_DIR)
        relative_str = str(relative)
        if filter_pattern and not relative_str.startswith(filter_pattern):
            continue
        parts = relative.parts
        tests.append(TestInfo(
            path=str(rom_path),
            rel=relative_str,
            name=rom_path.name,
            suite=parts[0] if len(parts) > 1 else "",
            subsuite="/".join(parts[:-1]),
            is_gbc=rom_path.suffix.lower() == ".gbc",
        ))
    return tests


def _escape_serial(text: str) -> str:
    """Escape non-printable characters in serial output for safe markdown display."""
    def _escape_char(ch):
        code = ord(ch)
        if ch in ('\n', '\t'):
            return ch
        if code < 0x20 or code == 0x7F:
            return f"\\x{code:02X}"
        return ch
    return "".join(_escape_char(c) for c in text)


def run_single_test(binary: str, info_dict: dict, config: dict) -> dict:
    suite_conf = get_suite_config(config, info_dict["rel"], info_dict["suite"], info_dict.get("subsuite", ""))
    timeout_cycles = suite_conf.get("timeout_cycles", config.get("default_timeout_cycles", 100_000_000))
    wall_timeout = suite_conf.get("wall_timeout_seconds", config.get("default_process_timeout_seconds", 120))

    cmd = [
        binary, "--headless",
        "--rom", info_dict["path"],
        "--timeout", str(timeout_cycles),
        "--detection", suite_conf.get("detection", "auto"),
        "--max-wall-seconds", str(max(1, wall_timeout - 2)),
    ]

    base_result = {
        "name": info_dict["name"],
        "rel": info_dict["rel"],
        "suite": info_dict["suite"],
        "subsuite": info_dict["subsuite"],
    }

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=wall_timeout)
        status, serial_parts = None, []
        has_result_line = False
        for line in proc.stdout.splitlines():
            if line.startswith("SERIAL:"):
                serial_parts.append(line[len("SERIAL:"):])
            elif line.startswith("RESULT:"):
                has_result_line = True
                tag = line[len("RESULT:"):].strip().upper()
                if tag == "PASS":
                    status = "pass"
                elif tag == "FAIL":
                    status = "fail"
                elif tag == "TIMEOUT":
                    status = "timeout"
                elif tag == "HANG":
                    status = "hang"
                else:
                    status = "error"

        serial = "\n".join(serial_parts)

        if not has_result_line or status is None:
            status = "crash"

        return {**base_result, "status": status, "serial": serial}
    except subprocess.TimeoutExpired:
        return {**base_result, "status": "timeout", "serial": "", "reason": f"Wall-clock timeout ({wall_timeout}s)"}
    except Exception as exc:
        return {**base_result, "status": "crash", "serial": "", "reason": str(exc)}


def dict_to_result(raw: dict) -> TestResult:
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
        with self._lock:
            self._pending_rels = list(rels)

    def start(self):
        if IS_TTY:
            sys.stdout.write(HIDE_CURSOR)
            sys.stdout.flush()
        self._thread = threading.Thread(target=self._render_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1)
        self._erase()
        if IS_TTY:
            sys.stdout.write(SHOW_CURSOR)
            sys.stdout.flush()

    def mark_done(self, result: TestResult):
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
    counts = defaultdict(int)
    for result in results:
        counts[result.status.value] += 1
    counts["total"] = len(results)
    return counts


def print_grouped_results(results: list[TestResult], verbose: bool = False):
    by_suite: dict[str, dict[str, list[TestResult]]] = defaultdict(lambda: defaultdict(list))
    for result in results:
        by_suite[result.suite][result.subsuite].append(result)

    first_suite = True
    for suite in sorted(by_suite):
        subsuites = by_suite[suite]

        suite_passed = sum(result.status == Status.PASS for sub in subsuites.values() for result in sub)
        suite_skipped = sum(result.status == Status.SKIPPED for sub in subsuites.values() for result in sub)
        suite_total = sum(len(sub) for sub in subsuites.values())
        suite_runnable = suite_total - suite_skipped

        if not first_suite:
            print()
        first_suite = False

        if suite_runnable == 0:
            print(f"  {DIM}{'─' * 40}{RESET}")
            print(f"  {BOLD}{suite}{RESET}  {DIM}(skipped){RESET}")
            continue

        if suite_passed == suite_runnable:
            suite_color = GREEN
        elif suite_passed > 0:
            suite_color = YELLOW
        else:
            suite_color = RED

        print(f"  {'─' * 40}")
        print(f"  {BOLD}{suite}{RESET}  {suite_color}{suite_passed}/{suite_runnable}{RESET}")
        print(f"  {'─' * 40}")

        for subsuite in sorted(subsuites):
            group = subsuites[subsuite]
            passed = sum(result.status == Status.PASS for result in group)
            skipped = sum(result.status == Status.SKIPPED for result in group)
            total = len(group)
            runnable = total - skipped

            sub_label = subsuite.replace(suite + "/", "") if subsuite != suite else "(root)"

            if skipped == total:
                print(f"    {DIM}{sub_label}  (skipped){RESET}")
                continue

            if passed == runnable:
                sub_color = GREEN
            elif passed > 0:
                sub_color = YELLOW
            else:
                sub_color = RED

            print(f"    {sub_label}  {sub_color}{passed}/{runnable}{RESET}")

            for result in sorted(group, key=lambda x: x.name):
                icon = STATUS_ICON[result.status]
                
                if result.status == Status.SKIPPED:
                    print(f"      {icon} {DIM}{result.name} ({result.reason or 'Skipped'}){RESET}")
                else:
                    print(f"      {icon} {result.name}")

                if verbose and result.serial and result.status != Status.PASS:
                    for serial_line in result.serial.splitlines()[:8]:
                        print(f"        {DIM}{serial_line}{RESET}")

    print()


def print_summary(results: list[TestResult], elapsed: float, workers: int):
    counts = count_statuses(results)
    divider = "-" * 40

    print(f"  {BOLD}Summary{RESET}")
    print(f"  {divider}")

    rows = [
        ("Total",   counts["total"],   BOLD),
        ("Passed",  counts["pass"],    GREEN),
        ("Failed",  counts["fail"],    RED),
        ("Timeout", counts["timeout"], YELLOW),
        ("Hang",    counts["hang"],    YELLOW),
        ("Skipped", counts["skipped"], DIM),
        ("Crashed", counts["crash"],   RED),
        ("Error",   counts["error"],   RED),
    ]
    for label, value, color in rows:
        if value > 0 or label == "Total":
            print(f"  {label:<12} {color}{value:>5}{RESET}")

    print(f"  {divider}")
    print(f"  {DIM}{elapsed:.1f}s · {workers} workers{RESET}")
    print()


def _md_escape(text: str) -> str:
    """Escape pipe characters and newlines for markdown table cells."""
    return text.replace("|", "\\|").replace("\n", "<br>")


def _md_color(text: str, color: str) -> str:
    return f'<span style="color:{color}">{text}</span>'


def generate_tests_md(results: list[TestResult]):
    counts = count_statuses(results)
    total_runnable = counts["total"] - counts["skipped"]
    pass_rate = (counts["pass"] / total_runnable * 100) if total_runnable else 0

    lines = [
        "# NoobBoy — Test Results",
        "",
        f"> Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"**{counts['pass']}** of **{total_runnable}** runnable tests passing ({pass_rate:.0f}%)"
        f" — {counts['skipped']} skipped",
        "",
        "| | Count |",
        "|:--|--:|",
        f"| {_md_color('Passed', 'green')} | {counts['pass']} |",
        f"| {_md_color('Failed', 'red')} | {counts['fail']} |",
        f"| {_md_color('Timeout', 'goldenrod')} | {counts['timeout']} |",
        f"| {_md_color('Hang', 'goldenrod')} | {counts['hang']} |",
        f"| {_md_color('Crashed', 'red')} | {counts['crash']} |",
        f"| {_md_color('Error', 'red')} | {counts['error']} |",
        f"| {_md_color('Skipped', 'gray')} | {counts['skipped']} |",
        f"| **Total** | **{counts['total']}** |",
        "",
    ]

    by_suite: dict[str, dict[str, list[TestResult]]] = defaultdict(lambda: defaultdict(list))
    for result in results:
        by_suite[result.suite][result.subsuite].append(result)

    for suite in sorted(by_suite):
        subsuites = by_suite[suite]

        suite_passed = sum(result.status == Status.PASS for sub in subsuites.values() for result in sub)
        suite_skipped = sum(result.status == Status.SKIPPED for sub in subsuites.values() for result in sub)
        suite_total = sum(len(sub) for sub in subsuites.values())
        suite_runnable = suite_total - suite_skipped

        lines.append("---")
        lines.append("")

        if suite_runnable == 0:
            lines.append(f"## {_md_color(suite, 'gray')} — Skipped")
            lines.append("")
            reasons = sorted(set(
                result.reason or "Skipped"
                for sub in subsuites.values() for result in sub if result.status == Status.SKIPPED
            ))
            for reason in reasons:
                lines.append(f"*{reason}*")
            lines.append("")
            continue

        suite_color = 'green' if suite_passed == suite_runnable else ('goldenrod' if suite_passed > 0 else 'red')
        lines.append(f"## {suite} — {_md_color(f'{suite_passed}/{suite_runnable}', suite_color)}")
        lines.append("")

        for subsuite in sorted(subsuites):
            group = subsuites[subsuite]
            passed = sum(result.status == Status.PASS for result in group)
            skipped = sum(result.status == Status.SKIPPED for result in group)
            total = len(group)
            runnable = total - skipped

            heading = subsuite.replace(suite + "/", "") if subsuite != suite else "General"

            if skipped == total:
                lines.append(f"### {_md_color(heading, 'gray')} — Skipped")
                lines.append("")
                lines.append(f"*{group[0].reason or 'Skipped'}*")
                lines.append("")
                continue

            sub_color = 'green' if passed == runnable else ('goldenrod' if passed > 0 else 'red')
            lines.append(f"### {heading} — {_md_color(f'{passed}/{runnable}', sub_color)}")
            lines.append("")
            lines.append("| | Test | Status | Output |")
            lines.append("|:--|:--|:--|:--|")

            for result in sorted(group, key=lambda x: x.name):
                if result.status == Status.SKIPPED:
                    continue
                icon = STATUS_MD_ICON.get(result.status, "")
                color = STATUS_MD_COLOR.get(result.status, "")
                status_text = _md_color(STATUS_MD_LABEL.get(result.status, "?"), color)
                output = _md_escape(_escape_serial(result.serial.strip())) if result.serial else result.reason or ""
                if len(output) > 300:
                    output = output[:300] + "..."
                lines.append(f"| {icon} | {result.name} | {status_text} | {output} |")

            lines.append("")

    TESTS_MD_PATH.write_text("\n".join(lines) + "\n")


def save_results_json(results: list[TestResult]):
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
            "summary": {key: counts[key] for key in ("total", "pass", "fail", "timeout", "hang", "skipped", "crash", "error")},
            "suites": {key: dict(val) for key, val in suites_data.items()},
        }, fh, indent=2)


def update_readme_badges(results: list[TestResult]):
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


def audit_config_keys(config: dict, discovered_rels: set[str]):
    """Warn about config.json suite keys that look like ROM paths but don't match any discovered ROM."""
    suites = config.get("suites", {})
    for key in suites:
        if "/" in key and (key.endswith(".gb") or key.endswith(".gbc")):
            if key not in discovered_rels:
                print(f"  {YELLOW}WARNING: config.json key '{key}' does not match any discovered ROM{RESET}")


def list_suites(config: dict):
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

    # Audit config.json keys against discovered ROMs
    all_rels = {test.rel for test in all_tests}
    audit_config_keys(config, all_rels)

    all_results: list[TestResult] = []
    runnable_tests: list[TestInfo] = []
    for info in all_tests:
        suite_conf = get_suite_config(config, info.rel, info.suite, info.subsuite)

        reason = None
        if info.is_gbc:
            reason = "GBC ROM (DMG only)"
        elif suite_conf.get("skip"):
            reason = suite_conf.get("skip_reason", "Skipped")

        if not reason:
            runnable_tests.append(info)
            continue

        all_results.append(TestResult(
            info.name, info.rel, info.suite, info.subsuite,
            Status.SKIPPED, reason=reason,
        ))

    suite_count = len({test.suite for test in all_tests})
    workers = args.jobs or min(os.cpu_count() or 4, max(1, len(runnable_tests)))

    print()
    print(f"  {BOLD}NoobBoy Test Suite{RESET}")
    print(f"  {'-' * 40}")
    print(f"  {len(all_tests)} tests · {suite_count} suites · {workers} workers")
    print(f"  {'-' * 40}")
    print()

    elapsed = 0
    display = None
    if runnable_tests:
        suite_stats: dict[str, dict] = defaultdict(lambda: {"passed": 0, "runnable": 0})
        for info in runnable_tests:
            suite_stats[info.suite]["runnable"] += 1

        display = LiveDisplay(dict(suite_stats), len(runnable_tests), workers)
        display.set_pending([test.rel for test in runnable_tests])
        display.start()

        run_results: list[TestResult] = []
        start_time = time.time()

        try:
            with ProcessPoolExecutor(max_workers=workers) as executor:
                futures = {
                    executor.submit(run_single_test, args.binary, dataclasses.asdict(info), config): info
                    for info in runnable_tests
                }
                for future in as_completed(futures):
                    result = dict_to_result(future.result())
                    run_results.append(result)
                    display.mark_done(result)
        except KeyboardInterrupt:
            display.stop()
            print(f"\n  {RED}Interrupted — {len(run_results)} of {len(runnable_tests)} tests completed.{RESET}\n")
            sys.exit(1)

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
        sys.exit(1)


if __name__ == "__main__":
    main()
