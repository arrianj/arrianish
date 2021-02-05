# arrianish

>An interpreted programming language written in Python 3

arrianish is built on a recursive descent parser, written with the goal of learning more about compilers and programming languages. It is based on the Pascal language, with some personal modifications such as the language being entirely lowercase, out of a personal design choice. I plan on expanding arrianish to include more unique defining features in the future.

## compiler

The arrianish scanner will analyze user input, tokenize the input if no errors are detected, and pass the tokens onto the parser. At this point, arrianish will parse the tokens, and if no errors are found at this stage, generate an abstract syntax tree.

Once the AST is built, the interpreter will visit each node in a top-down, left-to-right order and return the appropriate values and errors as output.

## running arrianish

arrianish can be written and run either via a command line interface, or by writing code to a file and running the file. Either way, both Python and arrianish will need to be installed for the shell to launch.

1) Install Python 3.6 or higher from [here](https://www.python.org/downloads/) (arrianish uses f-strings, and will not work on versions of Python prior to 3.6)


2) Download this repo
```
$ git clone https://github.com/arrianj/arrianish.git
```

3) Then navigate in your command line to the arrianish folder, and launch the shell with

```
$ python3 shell.py
```

Refer [here](https://github.com/arrianj/arrianish#multi-line-support) on how to write multi-line code in the CLI, but for larger scripts, saving your code to a file and running the file will be a better course of action.

Place your scripts in the arrianish directory on your computer. arrianish scripts can be written in a generic text file format. The correct usage would be to save the file with a .arrian extension, but files saved with the .txt extension will run as well.

Once the arrianish shell is running, the run command can be used to execute the code. To test the language, write a hello world program by writing the following line to a file, and saving it as hello.arrian

```
print("hello world")
```

and to run it from the arrianish shell:

```
$ arrianish > run("hello.arrian")
hello arrianish user
0
```

## grammar

Operator precedence is present in arrianish, all expressions follow the order of operations. 

```
statements      : newline* statement (newline+ statement)* newline*

statement       : keyword:return expr?
                : keyword:continue
                : keyword:break
                : expr

expr            : keyword:var identifier eq expr
                : comp-expr ((keyword:and|keyword:or) comp-expr)*

comp-expr       : not comp-expr
                : arith-expr ((ee|lt|gt|lte|gte) arith-expr)*

arith-expr      : term ((plus|minus) term)*

term            : factor ((mul|div) factor)*

factor          : (plus|minus) factor
                : power

power           : call (pow factor)*

call            : atom (lparen (expr (comma expr)*)? rparen)?

atom            : int|float|string|identifier
                : lparen expr rparen
                : list-expr
                : if-expr
                : for-expr
                : while-expr
                : func-def

list-expr       : lsqaure (expr (comma expr)*)? rsquare

if-expr         : keyword:if expr keyword:then
                  (expr if-expr-b|if-expr-c?)
                | (newline statements keyword:end|if-expr-b|if-expr-c)

if-expr-b       : keyword:elif expr keyword:then
                  (expr if-expr-b|if-expr-c?)
                | (newline statements keyword:end|if-expr-b|if-expr-c)

if-expr-c       : keyword:else
                  expr
                | (newline statements keyword:end)

for-expr        : keyword:for identifier eq expr keyword:to expr
                 (keyword: step expr)? keyword:then 
                 expr
                | (newline statements keyword:end)

while-expr      : keyword:while expr keyword:then
                 expr
                | (newline statements keyword:end)

func-def        : keyword:fun identifier?
                  lparen (identifier (comma identifier)*)? rparen
                  (arrow expr)
                | (newline statements keyword:end)
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

## functions

Functions in arrianish are defined with the 'fun' keyword, which is a good reminder of how little fun I had when debugging the functionality. 

```
$ arrianish > fun add (a, b) -> a + b
<function add>
$ arrianish > add(10, 5)
15
```

arrianish allows for anonymous function creation, and assigning a variable name to a function, both features demonstrated here:

```
$ arrianish > var new_func = add
<function add>
$ arrianish > new_func
<function add>
$ arrianish > new_func(10,5)
15

$ arrianish > fun (a) -> a + 5
<function <anonymous>>
$ arrianish > var add_five = fun(a) -> a + 5
<function <anonymous>>
$ arrianish > add_five(10)
15
```

## strings

Strings in arrianish begin and end with double quotation marks. String concatenation is supported with the + operator, and string multiplication is done with the * operator.

```
$ arrianish > "hello world"
"hello world"
$ arrianish > "hello" + " world"
"hello world"
$ arrianish > "alright " * 3 
"alright alright alright "

```

Strings can be used in functions with no issues, as shown here:

```
$ arrianish > fun greet(name, emphasization) -> "hello, " * emphasization + name  
<function greet>
$ arrianish > greet("arrian", 3) 
"hello, hello, hello, arrian"
```

## lists

Lists in arrianish begin and end with square brackets. Elements can be added to lists with the + operator, and elements can be removed from a list with the - operator.

To retrieve an element from a list, use the / operator to return the element at a specific index. arrianish uses zero-based indexing, meaning the first element in a list will be at the index position 0, the next element will be at index position 1, etc.

```
$ arrianish > [1, 2, 3]    
[1, 2, 3]   
$ arrianish > [1, 2, 3] + 4 + 5
[1, 2, 3, 4, 5]
$ arrianish > [1, 2, 3, 4] / 2
3
```
In the event of an out-of-bounds index position being called, a runtime error will occur:

```
$ arrianish > [1, 2, 3, 4] / 99
traceback (most recent call last):
    file <stdin>, line 1, in <program>
runtime error: element at this index could not be retrieved from list because index is out of bounds

[1, 2, 3, 4] / 99
               ^^
```

Both while or for loops will return lists:

```
$ arrianish > for i = 1 to 10 then 2 ^ i
[2, 4, 8, 16, 32, 64, 128, 256, 512]
```

## built-in functions

arrianish has a range of functions that are pre-built into the language. The current list includes

| function|keyword|definition|
| :---|:----:|:----: |
| print| print()| prints output to console|
| print return| print_ret()| returns output to system|
| input| input()| saves user input|
| input integer| input_int()| saves user numeric input|
| clear| clear()| clears console|
| is number| is_num()|checks if input is a number|
| is string| is_str()|checks if input is a string|
| is list|is_list()|checks if input is a list|
| is function| is_fun()|checks if input is a function|
| append| append()| adds element to list|
| pop| pop()| removes last element from list|
| extend| extend()| adds elements input list to called upon list|

## multi-line support

Semi-colons (;) are used as a new line indicator for arrianish. 

```
$ arrianish > 1+2; 3-4; 5*6
[3, -1, 30]

$ arrianish > if 5 == 5 then; print("addition"); print("exists") else print("what is math")
addition
exists
0
```

## return, break, continue

The return keyword, when used inside a function, will both end the function call and returns the value of the expression inside the function.

Using the break keyword can be used inside a loop will allow you to exit the loop, whereas continue will allow a loop to skip to the next iterator. 

```
$ arrianish > fun test(); var foo = 5; return foo; end
$ arrianish > test()
> 5
```

```
$ arrianish > var a = []
> []

$ arrianish > for i = 0 to 10 then; if i == 4 then continue elif i == 8 then break; var a = a + i; end
>0

$ arrianish > a
>[0, 1, 2, 3, 5 ,6 ,7]
```

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

Traceback showing context of function in program:

```
$ arrianish > fun div_by_0(a) -> a / 0
<function div_by_0>
$ arrianish > div_by_0(5)
traceback (most recent call last):
    file <stdin>, line 1, in <program>
    file <stdin>, line 1, in div_by_0
runtime error: division by zero

fun div_by_0(a) -> a / 0
                       ^
```

## contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## license
The code in this project is licensed under the MIT license.