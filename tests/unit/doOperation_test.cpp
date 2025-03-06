#include <gtest/gtest.h>
#include <fcntl.h>
#include <cstdio>
#include <string>

extern "C" {
    typedef struct
    {
        int head;
        int* elems;
        double* d_elems;
        bool is_float;
    } Stack;

    void init_stack(Stack* stack, bool flag);
    void push(Stack* s, int elem);
    void push_d(Stack* s, double elem);
    int pop(Stack* s);
    double pop_d(Stack* s);

    void doOperation(Stack* values, Stack* ops, bool _float);
}

TEST(doOperationTest, IntOperands) {
    Stack values, ops;
    init_stack(&values, false);
    init_stack(&ops, false);
    
    values.head = -1;
    ops.head = -1;
    
    push(&values, 11);
    push(&values, 11);
    push(&ops, '-');
    
    doOperation(&values, &ops, false);
    EXPECT_EQ(0, pop(&values));
}

TEST(doOperationTest, FloatOperands) {
    Stack values, ops;
    init_stack(&values, true);
    init_stack(&ops, false);
    
    values.head = -1;
    ops.head = -1;
    
    push_d(&values, 11.5);
    push_d(&values, 11.5);
    push(&ops, '-');
    
    doOperation(&values, &ops, true);
    EXPECT_EQ(0, pop_d(&values));
}
