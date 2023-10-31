from Error import Error, Success
import logging
import logging
logging.basicConfig()
logger = logging.getLogger("manfred")


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
NUMBERS  = "1234567890"
ALPHABET_SECONDARY = NUMBERS + "%"

from Tokens import *

symbol_table = {'[':TT_LBRACK,
                ']':TT_RBRACK,
                '<':TT_LANG,
                '>':TT_RANG,
                '(':TT_LPAREN,
                ')':TT_RPAREN,
                ',':TT_COMMA,
                '=':TT_EQ,
                '+':TT_ADD,
                '-':TT_SUB,
                '*':TT_MUL,
                '/':TT_DIV
                }

class Token:
    def __init__(self, token_type, position = 0, data = ""):
        self.token_type = token_type
        self.data = data
        self.position = position
    def __repr__(self):
        if self.data:
            return f"<{self.token_type} : {self.data}>"
        else:
            return f"<{self.token_type}>"
    def matches(self, other_type, other_data=""):
        if other_data:
            return self.token_type == other_type and self.data == other_data
        else:
            return self.token_type == other_type
    def matches_any(self, *args):
        return self.token_type in args

class LexRegister:
    def __init__(self, statement):
        self.position = 0
        self.statement = statement
    
    def advance(self):
        self.position += 1
    
    def current(self):
        return self.statement[self.position]
    
    def eof(self):
        return self.position >= len(self.statement)
    def place(self):
        return self.position
        
class Lexer:
    def __init__(self):
        self.tokens = []
    
    def lex(self, statement):
        self.register = LexRegister(statement)
        while True:
            if self.register.eof():
                self.tokens.append(Token(TT_END, self.register.place()))
                break
            elif self.register.current() in NUMBERS:
                result = self.make_num()
                if type(result) is Error:
                    return result
            elif self.register.current() in ALPHABET:
                result = self.make_string()
                if type(result) is Error:
                    return result
            elif self.register.current() == '"':
                result = self.make_abs_string()
                if type(result) is Error:
                    return result
            elif self.register.current() in symbol_table.keys():
                self.tokens.append(Token(symbol_table[self.register.current()], self.register.place()))
                self.register.advance()
            elif self.register.current() == " ":
                self.register.advance()
            else:
                return Error("SYNTAX ERROR",self.register.statement, 
                             f"Unexpected character: {self.register.current()}",self.register.position)
        return Success()
    
    def make_num(self):
        tmp = self.register.current()
        pos = self.register.place()
        is_float = False
        while True:
            self.register.advance()
            if self.register.eof():
                break
            if self.register.current() in NUMBERS:
                tmp += self.register.current()
            
            elif self.register.current() == '.':
                if not is_float:
                    tmp += self.register.current()
                    is_float = True
                else:
                    return Error("SYNTAX ERROR", self.register.statement,
                             "Unexpected '.'", self.register.position)
            else:
                break
        if tmp.endswith('.'):
            return Error("SYNTAX ERROR", self.register.statement,
                             "Float cannot end with '.'", self.register.position)
        self.tokens.append(Token(TT_NUM, pos, float(tmp)))
        return Success()
    
    def make_string(self):
        tmp = self.register.current()
        pos = self.register.place()
        while True:
            self.register.advance()
            if self.register.eof():
                break
            if self.register.current() in ALPHABET + ALPHABET_SECONDARY:
                tmp += self.register.current()
            else:
                break
        if tmp == "let":
            self.tokens.append(Token(TT_ASSIGN, pos))
        elif tmp == "show":
            self.tokens.append(Token(TT_OUTPUT, pos))
        elif tmp == "top":
            self.tokens.append(Token(TT_TOP, pos))
        elif tmp == "bot":
            self.tokens.append(Token(TT_BOT, pos))
        else:
            self.tokens.append(Token(TT_ID, pos, tmp))
        return Success()
    def make_abs_string(self):
        self.register.advance()
        pos = self.register.place()
        tmp = ""
        while self.register.current() != '"':
            tmp += self.register.current()
            self.register.advance()
            if self.register.eof():
                return Error("SYNTAX ERROR", self.register.statement, "Unexpected eof", self.register.place())
        self.tokens.append(Token(TT_ID, pos, tmp))
        self.register.advance()
        return Success()