# Tools
CC  ?= gcc
CXX ?= g++
AR  ?= ar

#venv
VENV_DIR ?= venv
PYTEST = $(VENV_DIR)/bin/pytest 

# Google Test directory
GTEST_DIR ?= googletest/googletest

# Directories
SRC_DIR ?= src
TESTS_DIR ?= tests
BUILD_DIR ?= build

APP_BUILD_DIR=$(BUILD_DIR)/app
TEST_BUILD_DIR=$(BUILD_DIR)/test

# Flags
CPPFLAGS += -isystem $(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra -pthread
CFLAGS += -g -Wall -Wextra -Wpedantic -Werror -std=c11

# Find C source files
APP_SRCS := $(shell find $(SRC_DIR) -name '*.c')

# Find test files
TEST_SRCS := $(shell find $(TESTS_DIR) -name '*.cpp')

# Object file paths
APP_OBJS := $(patsubst $(SRC_DIR)/%.c, $(APP_BUILD_DIR)/%.o, $(APP_SRCS))
TEST_OBJS := $(patsubst $(SRC_DIR)/%.c, $(TEST_BUILD_DIR_APP_OBJS)/%.o, $(APP_SRCS))
UNIT_TESTS_OBJS := $(patsubst $(TESTS_DIR)/%.cpp, $(TEST_BUILD_DIR_UNIT_TESTS_OBJS)/%.o, $(TEST_SRCS))

# Google Test headers
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h

# Creating build directories
$(shell mkdir -p $(APP_BUILD_DIR) $(TEST_BUILD_DIR))

# Clone gtest repo
$(shell git clone https://github.com/google/googletest &> /dev/null)


all: $(BUILD_DIR)/app.exe 
#$(BUILD_DIR)/unit-tests.exe

clean: 
	@echo "Deleting building"
	@rm -rf $(BUILD_DIR)
	@rm -rf $(VENV_DIR)
	@rm -rf .pytest_cache
	@rm -rf $(TEST_DIR)/integration/__pycache__

create-venv:
	@sudo apt-get install python3.10-venv
	@python -m venv $(VENV_DIR)
	@source $(VEVN_DIR)/bin/activate; pip install -U pytest

run-int: $(BUILD_DIR)/app.exe
	@$<

run-float: $(BUILD_DIR)/app.exe
	@$< --float
	
run-unit-tests: $(BUILD_DIR)/unit-tests.exe
	@$<

run-integration-test: $(BUILD_DIR)/app.exe create-venv tests/integration/simple_test.py
	@echo "Running integration test"
	@pytest tests/integration/simple_test.py

run-server: $(BUILD_DIR)/app.exe create-venv server/server.py
	@source $(VEVN_DIR)/bin/activate; server/server.py
	
-include $(APP_OBJS: .o=.d)
$(APP_BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) -MD -MP -c $< -o $@
	@tr < $@ -d '\000' > $@
	
$(BUILD_DIR)/app.exe: $(SRC_DIR)/main.c
	@echo "Building app.exe"
	@$(CC) $(CFLAGS) $^ -o $@
	
$(BUILD_DIR)/app-test.o:
	@$(CC) -DGTEST -c $(SRC_DIR)/main.c -o $@
	
$(BUILD_DIR)/unit-tests.exe: $(BUILD_DIR)/gtest/gtest_main.a $(BUILD_DIR)/app-test.o
	@$(CXX) -isystem $(GTEST_DIR)/include -pthread \
		$(TEST_SRCS) \
		$(BUILD_DIR)/gtest/gtest_main.a $(BUILD_DIR)/app-test.o \
		-o $(BUILD_DIR)/unit-tests.exe




$(BUILD_DIR)/gtest/gtest-all.o: $(GTEST_DIR)/src/*cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	@mkdir -p $(BUILD_DIR)/gtest
	@$(CXX) -isystem $(GTEST_DIR)/include -I$(GTEST_DIR) -c $(GTEST_DIR)/src/gtest-all.cc -o $@
	
$(BUILD_DIR)/gtest/gtest_main.o: $(GTEST_DIR)/src/*cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	@$(CXX) -isystem $(GTEST_DIR)/include -I$(GTEST_DIR) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

$(BUILD_DIR)/gtest/gtest_main.a: $(BUILD_DIR)/gtest/gtest-all.o $(BUILD_DIR)/gtest/gtest_main.o
	ar rv $@ $^ -o $@

