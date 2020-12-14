# arrianish

>An interpreted programming language written in Python 3

arrianish is built on a recursive descent parser, written with the goal of learning more about compilers and programming languages. It is based on the Pascal language, with some personal modifications such as the language being entirely lowercase, out of a personal design choice. I plan on expanding arrianish to include more unique defining features in the future.

## compiler

The arrianish scanner will analyze user input, tokenize the input if no errors are detected, and pass the tokens onto the parser. At this point, arrianish will parse the tokens, and if no errors are found at this stage, generate an abstract syntax tree.

Once the AST is built, the interpreter will visit each node in a top-down, left-to-right order and return the appropriate values and errors as output.

## syntax

Operator precedence is present in arrianish, all expressions follow the order of operations.

```
expr            : keywords:var identifier eq expr
                : comp-expr ((keyword: and|keyword: or) comp-expr)*

comp-expr       : not comp-expr
                : arith-expr ((ee|lt|gt|lte|gte) arith-expr)*

arith-expr      : term ((plus|minus) term)*

term            : factor ((mul|div) factor)*

factor          : (plus|minus) factor
                : power

power           : atom (pow factor)*

atom            : int|float|identifier
                : lparen expr rparen

if-expr         : keyword:if expr keyword:then expr
                 (keyword:elif expr keyword:then expr)*
                 (keyword:else expr)?

for-expr        : keyword:for identifier eq expr keyword:to expr
                 (keyword: step expr)? keyword:then expr

while-expr      : keyword:while expr keyword:then expr
```

## arithmetic 

arrianish supports unary and binary mathematical operations, including the elementary arithmetic operations and exponentiation with the (^) operator. 

```
$ arrianish > -5
-5

$ arrianish > 1 + 2
3

$ arrianish > 5^5
3125

$ arrianish > (9*2)/5
3.6
```

variables can be defined with the 'var' keyword:
```
$ arrianish > var a = 10
10
```


multiple variables can be assigned at once, and will be stored as needed

```
$ arrianish > var a = var b = var c = 10
10
```

Comparison operators, logical operators, and booleans are supported in arrianish. Boolean values for true and false are set to the values 1 and 0, respectively.

```
$ arrianish > true
1
$ arrianish > false
0
```
Comparison operators:

- greater than (>)
- greater than or equal to (>=)
- less than (<)
- less than or equal to (<=)
- equal to (==)
- not equal to (!=)

```
$ arrianish > 1 > 2
0
$ arrianish > 1 >= 2
0
$ arrianish > 1 < 2
1
$ arrianish > 1 <= 2
1
$ arrianish > 1 == 2
0
$ arrianish > 1 != 2
1
```

## keywords


Logical operators supported in arrianish include:

- and 
- or
- not

```
$ arrianish > 1 == 1 and 2 == 4
0

$ arrianish > 1 == 1 or 2 == 3
1

$ arrianish > var a = 1
1
$ arrianish > not a < 0 and a < 10
1
$ arrianish > not a < 5 and a < 10
0
```
If statements are supported in arrianish, with elif and else keywords to allow for multiple expressions, and conditional output. If statements are expressed in this format:

```
$ arrianish > if 1 == 1 then 2  
2

$ arrianish > var foo = 10
10
$ arrianish > var bar = if foo >= 5 then 8 else 12
8
$ arrianish > bar
8
```

For loops in arrianish allow for a start value, end value, and step size value between those points to be defined, as shown here: 

```
$ arrianish > var result = 5
5
$ arrianish > for i = 5 to 0 step -1 then var result = result * i
$ arrianish > result
600
```
While loops are currently supported, but as there is no print function, the output is not currently any way for me to show an example in the command line. I will update this in the readme when a print feature is supported

## exception handling

arrianish has fully functioning exception handling, with traceback functionality to provide context in the event of exceptions arising, such as division by zero runtime errors, and properly catching illegal or invalid syntax entries.

In the event of a runtime error, the compiler will run a traceback function to display context and highlight the characters that raised the exception.

Division by zero runtime error handling:

```
$ arrianish > var a = 0
0
$ arrianish > 5 / a
traceback (most recent call last):
    file <stdin>, line 1, in <program>
runtime error: Division by zero

5 / a
    ^
```
Invalid syntax error handling:

```
$ arrianish > var a = 10
10
$ arrianish > a 6
invalid syntax: expected '+', '-', '*', '/', or '^'
file <stdin>, line 1

a 6
  ^
```
Undefined variable handling:

```
$ arrianish > abc
traceback (most recent call last):
    file <stdin>, line 1, in <program>
runtime error: 'abc' is not defined

abc
^^^
```

## contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## license
The code in this project is licensed under the MIT license.