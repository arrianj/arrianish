#################
#    IMPORTS
#################
from string_with_arrows import *

#################
#   CONSTANTS
#################

digits = '0123456789'

#################
#     ERRORS
#################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

#################
#    POSITION
#################

class Position:

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col += 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#################
#     TOKENS
#################

tt_int = 'int'
tt_float = 'float'
tt_plus = 'plus'
tt_minus = 'minus'
tt_mul = 'mul'
tt_div = 'div'
tt_lparen = 'lparen'
tt_rparen = 'rparen'
tt_eof = 'eof'

class Token:
    def __init__(self, type_, value = None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#################
#     LEXER
#################

class Lexer:

    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in digits:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(tt_plus, pos_start = self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(tt_minus, pos_start = self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(tt_mul, pos_start = self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(tt_div, pos_start = self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(tt_lparen, pos_start = self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(tt_rparen, pos_start = self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(tt_eof, pos_start=self.pos))
        return tokens, None
    
    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in digits + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(tt_int, int(num_str), pos_start, self.pos) 
        else:
            return Token(tt_float, float(num_str), pos_start, self.pos)

#################
#     NODES
#################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

class UnaryOpNode:
    # handles unary operations
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class BinOpNode:
    # handles binary operations (addition, subtraction, multiplication, and division)
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


#################
#  PARSE RESULT
#################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


#################
#    PARSER
#################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type!= tt_eof:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', or '/'"
                ))
        return res

#################
    
    def factor(self):
        res = ParseResult()
        tok =self.current_tok

        if tok.type in (tt_plus, tt_minus):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))


        elif tok.type in (tt_int, tt_float):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == tt_lparen:

            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == tt_rparen:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))



        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end, 
            'Expected int or float'
            ))

    def term(self):
        return self.bin_op(self.factor, (tt_mul, tt_div))

    def expr(self):
        return self.bin_op(self.term, (tt_plus, tt_minus))

#################

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

#################
#      RUN
#################

def run(fn, text):

    # generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # generate abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error