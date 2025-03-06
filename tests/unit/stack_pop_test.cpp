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
    void push(Stack* stack, int elem);
    void push_d(Stack* stack, double elem);
    
    int pop(Stack* stack);
    double pop_d(Stack* stack);
}

TEST(stackPopTest, IntStack) {
    Stack stack;
    stack.head=-1;
    init_stack(&stack, false);
    push(&stack, 11);
    EXPECT_EQ(11, pop(&stack));
}

TEST(stackPopTest, FloatStack) {
    Stack stack;
    stack.head=-1;
    init_stack(&stack, true);
    push_d(&stack, 11.05);
    EXPECT_EQ(11.05, pop_d(&stack));
}
