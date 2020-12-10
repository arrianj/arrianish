#################
#    IMPORTS
#################

import string

from string_with_arrows import *

#################
#   CONSTANTS
#################

digits = '0123456789'
letters = string.ascii_letters
letters_digits = letters + digits

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

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result += f'    File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

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
tt_pow = 'pow'
tt_identifier = 'identifier'
tt_keyword = 'keyword'
tt_eq = 'eq'
tt_eof = 'eof'

keywords = [
    'var'
]
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

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
            elif self.current_char in letters:
                tokens.append(self.make_identifier())
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
            elif self.current_char == '^':
                tokens.append(Token(tt_pow, pos_start = self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(tt_eq, pos_start = self.pos))
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

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in letters_digits + '_':
            id_str += self.current_char
            self.advance()

        tok_type = tt_keyword if id_str in keywords else tt_identifier
        return Token(tok_type, id_str, pos_start, self.pos)

#################
#     NODES
#################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'{self.tok}'

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class UnaryOpNode:
    # handles unary operations
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class BinOpNode:
    # handles binary operations (addition, subtraction, multiplication, and division)
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_start
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

#################
#  PARSE RESULT
#################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1
    
    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
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
                "Expected '+', '-', '*', '/', or '^'"
                ))
        return res

#################    
    def atom(self):
        res = ParseResult()
        tok =self.current_tok

        if tok.type in (tt_int, tt_float):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == tt_identifier:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == tt_lparen:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == tt_rparen:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end, 
            "Expected int, float, identifier, '+','-', or '("
            ))

    def power(self):
        return self.bin_op(self.atom, (tt_pow, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok =self.current_tok

        if tok.type in (tt_plus, tt_minus):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (tt_mul, tt_div, tt_pow))

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(tt_keyword, 'var'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != tt_identifier:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected identifier'
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != tt_eq:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))
            
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.term, (tt_plus, tt_minus)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'var', int, float, identifier, '+', '-', or'('"
            ))        
            
        return res.success(node)
#################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

#################
# RUNTIME RESULT
#################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
    
    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

#################
#    VALUES
#################

class Number:
    # this class can store numbers and operates on them with other numbers
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def powered_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

#################
#    CONTEXT
#################

class Context: 
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

#################
#  SYMBOL TABLE
#################

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

#################
#  INTERPRETER
#################

class Interpreter:
    # will visit each node
    def visit(self, node, context):
        # if it runs into binary operator node, it'll write 'visit_BinOpNode'
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defines.')

    #################
    def visit_NumberNode(self, node, context):
        return RTResult().success(
        Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
            node.pos_start, node.pos_end,
            f"'{var_name}' is not defined",
            context
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == tt_plus:
            result, error = left.added_to(right)
        if node.op_tok.type == tt_minus:
            result, error = left.subtracted_by(right)
        if node.op_tok.type == tt_mul:
            result, error = left.multiplied_by(right)
        if node.op_tok.type == tt_div:
            result, error = left.divided_by(right)
        if node.op_tok.type == tt_pow:
            result, error = left.powered_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == tt_minus:
            number, error = number.multiplied_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
    #################
        
#################
#      RUN
#################

global_symbol_table = SymbolTable()
global_symbol_table.set('null', Number(0))

def run(fn, text):

    # generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # generate abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # run interpreter
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error