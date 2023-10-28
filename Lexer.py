from Error import Error, Success

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
NUMBERS  = "1234567890"

TT_NUM    = "NUM"
TT_ASSIGN = "ASSIGN" # 'let'
TT_OUTPUT = "OUTPUT" # 'show'
TT_ID     = "ID"     # Variable name, could be AVG, OPS, or made up
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRACK = "LBRACK"
TT_RBRACK = "RBRACK"
TT_LANG   = "LANG"   # '<'
TT_RANG   = "RANG"   # '>'
TT_COMMA  = "COMMA"
TT_DOT    = "DOT"    # '.'
TT_EQ     = "EQ"
TT_ADD    = "ADD"
TT_SUB    = "SUB"
TT_MUL    = "MUL"
TT_DIV    = "DIV"
TT_END    = "END"

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
    def __init__(self, token_type, data = ""):
        self.token_type = token_type
        self.data = data
    def __repr__(self):
        if self.data:
            return f"<{self.token_type} : {self.data}>"
        else:
            return f"<{self.token_type}>"
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
        
class Lexer:
    def __init__(self):
        self.tokens = []
    
    def lex(self, statement):
        self.register = LexRegister(statement)
        
        while True:
            if self.register.eof():
                self.tokens.append(Token(TT_END))
                break
            elif self.register.current() in NUMBERS:
                result = self.make_num()
                if type(result) is Error:
                    return result
            elif self.register.current() in ALPHABET:
                result = self.make_string()
                if type(result) is Error:
                    return result
            elif self.register.current() in symbol_table.keys():
                self.tokens.append(Token(symbol_table[self.register.current()]))
                self.register.advance()
            elif self.register.current() == " ":
                self.register.advance()
            else:
                return Error("SYNTAX ERROR",self.register.statement, 
                             f"Unexpected character: {self.register.current()}",self.register.position)
        return Success()
    
    def make_num(self):
        tmp = self.register.current()
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
        self.tokens.append(Token(TT_NUM, float(tmp)))
        return Success()
    
    def make_string(self):
        tmp = self.register.current()
        while True:
            self.register.advance()
            if self.register.eof():
                break
            if self.register.current() in ALPHABET:
                tmp += self.register.current()
            else:
                break
        if tmp == "let":
            self.tokens.append(Token(TT_ASSIGN))
        elif tmp == "show":
            self.tokens.append(Token(TT_OUTPUT))
        else:
            self.tokens.append(Token(TT_ID, tmp))
        return Success()