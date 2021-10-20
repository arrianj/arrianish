# arrianish

>An interpreted programming language written in Python 3

arrianish is built on a recursive descent parser, written with the goal of learning more about compilers and programming languages in general. After building this project, I have a much better understanding on the specifics of how higher level languages interpret and execute code. arrianish is influenced by the Pascal language, including some design choices such as the language being entirely lowercase. I plan on expanding arrianish to include more unique defining features in the future.

## compiler

[This article, 'A crash course in compilers' ](https://increment.com/programming-languages/crash-course-in-compilers/ )by 
Ramsey Nasser is an excellent resource in a briefer on compiler theory, but to boil down how arrianish works:

The scanner will analyze the code input, tokenize the input if no errors are detected, and pass the tokens onto the parser. The parser reads the tokens, and if no errors are found at this stage, generates an abstract syntax tree of nodes for the interpreter to have an order of operations.

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
