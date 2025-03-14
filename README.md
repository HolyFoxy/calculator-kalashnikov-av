# calculator-kalashnikov-av

## Project description

### Program description

The calculator is written in the ```C``` programming language.
The sorting station (shunting yard) algorithm was chosen as the parsing algorithm.
The main idea of the algorithm is to convert an input string with an expression from an infix form to a reverse polish notation. Implemented on the basis of a stack storing readed operations.

### Parameters' description

During the work, a calculator was created with the following parameters:
- Retrieving data from ```stdin```
- Output data to ```stdout```
- Correct operation for input data less than 1KiB
- Operation with expressions in the alphabet ```[0-9()*+/-]```(space characters are allowed: ```\n,\f,\t,\v,\r```)
- Handling of expression input errors (returning a non-zero error code)
- Support for input consisting of integers in the range from 0 to $2\times10^9$
- Works correctly for all expressions in which each result of intermediate calculations (in any of the available calculation orders) is within $[-2\times10^9\dots+2\times10^9]$ (otherwise ```UB```)
- Support for the ```--float``` flag to switch the calculator to floating-point calculation mode
- In integer mode, division is integer
- In floating-point mode, division is fractional and the answer accuracy is $10^{-4}$
- If at any time during the calculations division by a number less than $10^{-4}$ occurs, correct operation is not guaranteed(```UB```)

### Using

To compile the program just enter the bath program:
```bash
make all
```

The program can read your input data in one of two ways:
- You can use bash command echo like this:
```bash
echo "123 + 123" | ./build/app.exe
```
```bash
echo "123 + 3/2" | ./build/app.exe --float
```
- Or you can use make to run in needed mode like this (after command input your expression in bash):
```bash
make run-int
```
```bash
make run-float
```

Both methods will lead to the same result -> the expression will be solved. The program will outputs the answer in stdout.

Also was written unit and integration tests, which can be launched by these bash commands:
```bash
make run-unit-tests
```
```bash
make run-integration-tests
```

## Development diary
### 13.03.25
The initial configuration of remote developer's machine was performed. Server's folder and main file have been created

### 14.03.25
Simple server have been created with option to process GET request
