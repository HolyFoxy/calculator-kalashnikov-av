#include <gtest/gtest.h>

extern "C" {
    size_t arlen(char* ar);
}

TEST(arlenTest, ArLen) {
    char ar[] = {'1','+','1','+','1'};
    EXPECT_EQ(5, arlen(ar));
}
