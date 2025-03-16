#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 65534

bool _float = false;

typedef enum Errors {
    NOT_PARIED_BRACKED_FOUND = -1,
    EMPTY_INPUT = -2,
    INVALID_ARGUMENT = -3,
    UNKNOWN_CHARACTER = -4,
    TOO_MANY_OPERANDS = -5,
    NULL_DIVISION = -6,
    TOO_MANY_OPERATORS = -7
} Errors;

typedef struct
{
    int head;
    int* elems;
    double* d_elems;
    bool is_float;
} Stack;

void init_stack(Stack* s, bool flag)
{
    if (flag)
        s->d_elems = (double*)malloc(sizeof(double) * MAX_LENGTH);
    else
        s->elems = (int*)malloc(sizeof(int) * MAX_LENGTH);
    s->is_float = flag;
}

int isEmpty(Stack* s)
{
    return s->head == -1;
}

void push(Stack* s, int elem)
{
    s->elems[++(s->head)] = elem;
}

void push_d(Stack* s, double elem)
{
    s->d_elems[++(s->head)] = elem;
}

char top(Stack* s)
{
    if (isEmpty(s))
        return 0;
    if (s->is_float)
        return s->d_elems[s->head];
    else
        return s->elems[s->head];
}

int pop(Stack* s)
{
    if (!isEmpty(s)) {
        return s->elems[(s->head)--];
    }
    return 0;
}

double pop_d(Stack* s)
{
    if (!isEmpty(s)) {
        return s->d_elems[(s->head)--];
    }

    return 0;
}

int opRank(char op)
{
    switch (op) {
    case '+':
        return 1;
    case '-':
        return 1;
    case '*':
        return 2;
    case '/':
        return 2;
    default:
        return 0;
    }
}

void doOperation(Stack* values, Stack* ops, bool _float)
{
    if ((values->head < 1) || (ops->head < 0))
        return;

    if (_float) {
        double a = pop_d(values);
        double b = pop_d(values);
        char op = pop(ops);

        switch (op) {
        case '+':
            push_d(values, (a + b));
            break;
        case '-':
            push_d(values, (b - a));
            break;
        case '*':
            push_d(values, (a * b));
            break;
        case '/':
            if ((a <= 0.0001)&&(a >= 0.0001))
                exit(NULL_DIVISION);
            push_d(values, (b / a));
            break;
        }

    } else {
        int a = pop(values);
        int b = pop(values);
        char op = pop(ops);

        switch (op) {
        case '+':
            push(values, (a + b));
            break;
        case '-':
            push(values, (b - a));
            break;
        case '*':
            push(values, (a * b));
            break;
        case '/':
            if (a == 0)
                exit(NULL_DIVISION);
            push(values, (b / a));
            break;
        }
    }
}

char* deleteSpaces()
{
    char temp[MAX_LENGTH];

    size_t i = 0;
    size_t temp_sym = 0;

    char ch = getchar();
    do {
        temp[i++] = ch;
        ch = getchar();
    } while (ch != EOF);
    i = 0;
    
    while (temp[i] != EOF && temp[i] != '\0' && (isdigit(temp[i]) || (temp[i] == '+') || (temp[i] == '-') || (temp[i] == '*') || (temp[i] == '/') || (temp[i] == '(') || (temp[i] == ')') || (isspace(temp[i])) || (temp[i] == '\\'))) {
        if (isspace(temp[i])) {
            if (i > 0 && (temp[i + 1]!= EOF) && isdigit(temp[i - 1]) && isdigit(temp[i + 1]))
                exit (TOO_MANY_OPERATORS);
            i++;
            continue;
        }
        if (temp[i] == '\\' && (temp[i+1] == 't' || temp[i+1] == 'r' || temp[i+1] == 'f' || temp[i+1] == 'n')) {
            if (i > 0 && (temp[i + 2]!= EOF) && isdigit(temp[i - 1]) && isdigit(temp[i + 2]))
                exit (TOO_MANY_OPERATORS);
            i+=2;
            continue;
        }
        temp_sym++;
        i++;
    }

    char* exp = malloc(sizeof(char) * temp_sym);
    if (exp == NULL)
        printf("Malloc Error\n");

    i = 0;
    temp_sym = 0;

    while (temp[i] != EOF && (isdigit(temp[i]) || (temp[i] == '+') || (temp[i] == '-') || (temp[i] == '*') || (temp[i] == '/') || (temp[i] == '(') || (temp[i] == ')') || (isspace(temp[i])) || (temp[i] == '\\'))) {
        if (isspace(temp[i])) {
            i++;
            continue;
        }
        if (temp[i] == '\\' && (temp[i+1] == 't' || temp[i+1] == 'r' || temp[i+1] == 'f' || temp[i+1] == 'n')) {
            i+=2;
            continue;
        }
        exp[temp_sym++] = temp[i++];
    }
    if (temp[i] != (char)0)
    	exit(UNKNOWN_CHARACTER);
    return exp;
}

size_t arlen(char* ar)
{
    size_t res = 0;
    while (((int)ar[res]) != 0)
        res++;
    return res;
}

int calculate(int argc, char* argv[])
{
    char* exp = deleteSpaces();
    size_t length = 0;
    length = arlen(exp);
    
    if (length == 0) {
        printf("Empty input");
        return EMPTY_INPUT;
    }

    bool _float = false;

    Stack values, ops;
    values.head = -1;
    ops.head = -1;

    if (argc > 1) {
        if (strcmp(argv[1], "--float") == 0)
            _float = true;
        else if (strcmp(argv[1], "--int") == 0)
            _float = false;
        else
            return INVALID_ARGUMENT;
    }

    init_stack(&values, _float);
    init_stack(&ops, false);

    size_t temp_sym = 0;

    while (temp_sym < length) {
        temp_sym++;
    }
    temp_sym = 0;

    while (temp_sym < length) {
        if (isdigit(exp[temp_sym])) {
            int num = 0;
            while (isdigit(exp[temp_sym])) {
                num = num * 10 + (exp[temp_sym++] - '0');
            }
            if (_float)
                push_d(&values, num);
            else
                push(&values, num);
            continue;
        } else if (exp[temp_sym] == '(') {
            push(&ops, exp[temp_sym++]);
            continue;
        } else if (exp[temp_sym] == ')') {
            while ((!isEmpty(&ops)) && (top(&ops) != '(')) {
                doOperation(&values, &ops, _float);
            }
            if (isEmpty(&ops))
                return NOT_PARIED_BRACKED_FOUND;
            pop(&ops);
            temp_sym++;
            continue;
        } else if ((exp[temp_sym] == '+') || (exp[temp_sym] == '-') || (exp[temp_sym] == '*') || (exp[temp_sym] == '/')) {
            if ((temp_sym == 0) || (exp[temp_sym - 1] == '+') || (exp[temp_sym - 1] == '-') || (exp[temp_sym - 1] == '*') || (exp[temp_sym - 1] == '/')) {
                return TOO_MANY_OPERATORS;
            }

            while ((!isEmpty(&ops)) && (opRank(top(&ops)) >= opRank(exp[temp_sym]))) {
                doOperation(&values, &ops, _float);
            }
            push(&ops, exp[temp_sym++]);
        } else {
            return UNKNOWN_CHARACTER;
        }
    }

    while (!isEmpty(&ops)) {
        if (top(&ops) == '(')
            return NOT_PARIED_BRACKED_FOUND;
        if (values.head < 1)
            return TOO_MANY_OPERATORS;
        doOperation(&values, &ops, _float);
    }

    if (_float) {
        double res = pop_d(&values);
        if (!isEmpty(&values))
            return TOO_MANY_OPERANDS;
        printf("%0.4f\n", res);
    } else {
        int res = pop(&values);
        if (!isEmpty(&values))
            return TOO_MANY_OPERANDS;
        printf("%i\n", res);
    }

    return 0;
}

#ifndef GTEST
int main(int argc, char* argv[])
{
    return calculate(argc, argv);
}
#endif
