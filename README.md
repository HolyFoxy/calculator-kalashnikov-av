# calculator-kalashnikov-av

A program written in C. It reads an arithmetic expression from standart input, parses it, and prints the result. The program supports the following operations on integers: *, -, +, /, (, ). Any whitespace characters are allowed in input.

### Algoritm

The sorting station (shunting yard) algorithm was chosen as the parsing algorithm.
The main idea of the algorithm is to convert an input string with an expression from an infix form to a reverse polish notation. Implemented on the basis of a stack storing readed operations.

### Using

To compile the program just enter the bath program:
```bash
gcc main.c -o calc.exe
```

The program can read your input data in one of two ways:
- You can use bash command echo like this:
```bash
echo "123 + 123" | calc.exe
```
- Or you can use program argument like this:
```bash
calc.exe "123 + 123"
```

Both methods will lead to the same result -> the expression will be solved. The program will outputs the answer in stdout:
```bash
246
```
