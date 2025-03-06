#include <gtest/gtest.h>

extern "C" {
    int opRank(char op);
}

TEST(opRankTest, OpRank) {
    EXPECT_EQ(2, opRank('*'));
}
