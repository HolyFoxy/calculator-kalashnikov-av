#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_LENGTH 1000

typedef struct 
{
	int head;
	int elems[MAX_LENGTH];
} Stack;

int isEmpty(Stack *s){
	return s->head == -1;
}

void push(Stack *s, int elem){
	s->elems[++(s->head)] = elem;
}

char top(Stack *s){
	if (isEmpty(s))
		return 0;
	return s->elems[s->head];
}

int pop(Stack *s){
	if (!isEmpty(s))
		return s->elems[(s->head)--];
	return NULL;
}

int opRank(char op){
	switch (op){
		case '+': return 1;
		case '-': return 1;
		case '*': return 2;
		case '/': return 2;
		default: return 0;
	}
	
}

void doOperation(Stack *values, Stack *ops){
	if ((values->head < 1)||(ops->head < 0))
		return;
	
	int a = pop(values);
	int b = pop(values);
	char op = pop(ops);
	
	switch(op){
		case '+': 
			push(values, (a + b));
			break;
		case '-':
			push (values, (b - a));
			break;
		case '*':
			push (values, (a * b));
			break;
		case '/':
			if (a == 0)
				break;
			push(values, (b/a));
			break;
	}
}

int main (int argc, char* argv[]){
	char exp [MAX_LENGTH];
	char temp [MAX_LENGTH];
	int i = 0;
	int temp_sym = 0;
	int length = 0;
	if (argc < 2){
		fgets (temp, MAX_LENGTH, stdin); 
		while (temp[i]!=EOF && (isdigit(temp[i])||(temp[i] == '+')||(temp[i] == '-')||(temp[i] == '*')||(temp[i] == '/')||(temp[i] == '(')||(temp[i] == ')')||(temp[i] == ' '))){
			if (temp[i] == ' '){i++; continue;}
			exp[temp_sym++] = temp[i++];
		}
	}else{
		while (i<strlen(argv[1])){
			if (temp_sym > MAX_LENGTH){
				printf("Too long expression\n");
				return 0;
			}
			if (argv[1][i] == ' '){i++; continue;}
			exp[temp_sym++] = argv[1][i++];
		}
	}
	length = temp_sym;
	
	Stack values, ops;
	values.head = -1;
	ops.head = -1;
	
	
	temp_sym = 0;
	while (temp_sym < length){
		if (isdigit(exp[temp_sym])){
			int num = 0;
			while (isdigit(exp[temp_sym])){
				num = num*10 + (exp[temp_sym++] - '0');
			}
			push(&values, num);
			continue;
		}
		else if (exp[temp_sym] == '('){
			push(&ops, exp[temp_sym++]);
			continue;
		}
		else if (exp[temp_sym] == ')'){
			while((!isEmpty(&ops))&&(top(&ops)!= '(')){
				doOperation(&values, &ops);
			}
			pop(&ops);
			temp_sym++;
			continue;
		}
		else {
			while ((!isEmpty(&ops))&&(opRank(top(&ops)) >= opRank(exp[temp_sym]))){
				doOperation(&values, &ops);
			}
			push (&ops, exp[temp_sym++]);
		}
	}
	
	while (!isEmpty(&ops)){
		doOperation(&values, &ops);
	}
	
	printf("%i\n", pop(&values));
	
	return 0;
}
