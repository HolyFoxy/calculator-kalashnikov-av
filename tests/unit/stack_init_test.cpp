#include <gtest/gtest.h>

extern "C" {
    typedef struct
    {
        int head;
        int* elems;
        double* d_elems;
        bool is_float;
    } Stack;

    void init_stack(Stack* s, bool flag);
}

TEST(stackInitTest, IntStack) {
    Stack stack;
    init_stack(&stack, false);
    EXPECT_EQ(false, stack.is_float);
}

TEST(stackInitTest, FloatStack) {
    Stack stack;
    init_stack(&stack, true);
    EXPECT_EQ(true, stack.is_float);
}
