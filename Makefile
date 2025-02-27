# Tools
CC  ?= gcc
CXX ?= g++
AR  ?= ar

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
TEST_SRCS := $(sell find $(TESTS_DIR) -name '*.cpp')

# Object file paths
APP_OBJS := $(patsubst $(SRC_DIR)/%.c, $(APP_BUILD_DIR)/%.o, $(APP_SRCS))
TEST_OBJS := $(patsubst $(SRC_DIR)/%.c, $(TEST_BUILD_DIR_APP_OBJS)/%.o, $(APP_SRCS))
UNIT_TESTS_OBJS := $(patsubst $(TESTS_DIR)/%.cpp, $(TEST_BUILD_DIR_UNIT_TESTS_OBJS)/%.o, $(TEST_SRCS))

# Google Test headers
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h

# Creating build directories
$(shell mkdir -p $(APP_BUILD_DIR) $(TEST_BUILD_DIR))



all: $(BUILD_DIR)/app.exe $(BUILD_DIR)/unit-tests.exe

clean: 
	@rm -rf $(BUILD_DIR)

run-int: $(BUILD_DIR)/app.exe
	@$<

run-float: $(BUILD_DIR)/app.exe
	@$< --float
	
run-unit-tests: $(BUILD_DIR)/unit-tests.exe
	@$<
	
	
	
-include $(APP_OBJS: .o=.d)
$(APP_BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@
	
$(BUILD_DIR)/app.exe: $(APP_OBJS)
	$(CC) $(CFLAGS) $^ -o $@	
