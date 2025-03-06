#include <gtest/gtest.h>

extern "C" {
    typedef struct
    {
        int head;
        int* elems;
        double* d_elems;
        bool is_float;
    } Stack;

    int isEmpty(Stack* stack);
}

TEST(stackEmptyCheckTest, EmptyStack) {
    Stack stack;
    stack.head=-1;
    EXPECT_EQ(1, isEmpty(&stack));
}
