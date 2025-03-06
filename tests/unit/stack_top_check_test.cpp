#include <gtest/gtest.h>

extern "C" {
    typedef struct
    {
        int head;
        int* elems;
        double* d_elems;
        bool is_float;
    } Stack;

    void init_stack(Stack* stack, bool flag);
    char top(Stack* stack);
    void push(Stack* stack, int elem);
}

TEST(stackTopCheckTest, Stack) {
    Stack stack;
    stack.head=-1;
    init_stack(&stack, false);
    push(&stack, (int)'+');
    EXPECT_EQ('+', top(&stack));
}
