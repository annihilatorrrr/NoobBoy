BUILD_ROOT   := build
DESKTOP_DIR  := $(BUILD_ROOT)/desktop
WEB_DIR      := $(BUILD_ROOT)/web
TERM_DIR     := $(BUILD_ROOT)/terminal
TESTER_DIR   := $(BUILD_ROOT)/tester

# CMake Options for Different Targets
DESKTOP_OPTS := -DBUILD_DESKTOP=ON -DCMAKE_BUILD_TYPE=Release
TESTER_OPTS  := -DBUILD_TESTER=ON -DCMAKE_BUILD_TYPE=Release
WEB_OPTS     := -DBUILD_WEB=ON -DCMAKE_BUILD_TYPE=Release
TERM_OPTS    := -DBUILD_TERMINAL=ON -DCMAKE_BUILD_TYPE=Release

# Default target: build the desktop version
.PHONY: all
all: desktop

####################################
# Desktop Build
####################################

$(DESKTOP_DIR):
	@echo "Creating desktop build directory..."
	@mkdir -p $(DESKTOP_DIR)

.PHONY: desktop
desktop: $(DESKTOP_DIR)
	@echo "Configuring Desktop Build..."
	@cd $(DESKTOP_DIR) && cmake $(CURDIR) $(DESKTOP_OPTS)
	@echo "Building Desktop Version..."
	@$(MAKE) -C $(DESKTOP_DIR)
	@echo "Desktop build complete. Executable is in $(DESKTOP_DIR)"

####################################
# Tester Build
####################################

$(TESTER_DIR):
	@echo "Creating tester build directory..."
	@mkdir -p $(TESTER_DIR)

.PHONY: tester
tester: $(TESTER_DIR)
	@echo "Configuring Tester Build..."
	@cd $(TESTER_DIR) && cmake $(CURDIR) $(TESTER_OPTS)
	@echo "Building Tester Version..."
	@$(MAKE) -C $(TESTER_DIR)
	@echo "Tester build complete. Executable is in $(TESTER_DIR)"

####################################
# Test Suite
####################################

.PHONY: test
test: tester
ifdef SUITE
	@python3 tests/run_tests.py --binary $(TESTER_DIR)/NoobBoyTester --filter "$(SUITE)" || true
else
	@python3 tests/run_tests.py --binary $(TESTER_DIR)/NoobBoyTester || true
endif

####################################
# Clean Target
####################################
.PHONY: clean
clean:
	@echo "Removing all build directories..."
	@rm -rf $(BUILD_ROOT)
