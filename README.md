# arrianish

>An interpreted programming language written in Python 3

arrianish is built on a recursive descent parser, written with the goal of learning more about compilers and programming languages.

## Compiler

The arrianish scanner will analyze user input, tokenize the input if no errors are detected, and pass the tokens onto the parser. At this point, arrianish will parse the tokens, and if no errors are found at this stage, generate an abstract syntax tree.

Once the AST is built, the interpreter will visit each node in a top-down, left-to-right order and return the appropriate values and errors as output.

## Syntax

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
```

## Usage

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

Comparison operators, logical operators, and booleans are supported in arrianish. Boolean values for true and false are set to the values 1, and 0, respectfully.

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


Logical operators:

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

## Exception handling

arrianish has fully functioning exception handling, with traceback functionality to provide context in the event of exceptions arising, such as division by zero runtime errors, and properly catching illegal or invalid syntax entries.

In the event of a runtime error, the compiler will display run a traceback function to display context, and highlight the characters that raised the exception.

Division by zero runtime error handling:

```
$ arrianish > var a = 0
0
$ arrianish > 5 / a
Traceback (most recent call last):
    File <stdin>, line 1, in <program>
Runtime Error: Division by zero

5 / a
    ^
```
Invalid syntax error handling:

```
$ arrianish > var a = 10
10
$ arrianish > a 6
Invalid Syntax: Expected '+', '-', '*', '/', or '^'
File <stdin>, line 1

a 6
  ^
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
The code in this project is licensed under the MIT license.