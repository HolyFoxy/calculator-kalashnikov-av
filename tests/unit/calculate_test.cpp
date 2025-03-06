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
    
    int isEmpty(Stack* stack);
    char top(Stack* stack);
    int opRank(char op);
    void doOperation(Stack* values, Stack* ops, bool _float);
    
    char* deleteSpaces();
    size_t arlen(char* ar);
    int calculate(int argc, char* argv[]);
}

TEST(calculateTest, SimpleIntExpression) {
    const char* exp = "1 + 1  -  2";
    FILE* instream = fmemopen((void*)exp, strlen(exp), "r");
    FILE* t = stdin;
    stdin = instream; 
    char* arg[] = {};
    EXPECT_EQ(0, calculate(0, arg));
}

TEST(calculateTest, HarderIntExpression) {
    const char* exp = "(105 + 25/5)*(90 - 75)";
    FILE* instream = fmemopen((void*)exp, strlen(exp), "r");
    FILE* t = stdin;
    stdin = instream;
    char* arg[] = {};
    EXPECT_EQ(0, calculate(0, arg));
}
