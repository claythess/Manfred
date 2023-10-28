from Error import Error, Success
from Tokens import *

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")

class ParseRegister:
    def __init__(self, token_list):
        self.token_list = token_list
        self.position = 0
    def current(self):
        return self.token_list[self.position]
    
    def advance(self):
        self.position += 1
    def next(self):
        return self.token_list[self.position + 1]

class AssignNode:
    def __init__(self, id_tok, value_node):
        self.id_tok = id_tok
        self.value_node = value_node
    def __repr__(self):
        return f"{self.id_tok.data} = {self.value_node}"

class OutputNode:
    def __init__(self, output_type,from_year, to_year, params, qualifier, num, sort_stat):
        self.output_type = output_type
        self.from_year = from_year
        self.to_year = to_year
        self.params = params
        self.qualifier = qualifier
        self.num = num
        self.sort_stat = sort_stat
    def __repr__(self):
        return f"[{self.from_year.data} - {self.to_year.data}] ({self.params}) {self.qualifier} {self.num}"

class ValueNode:
    def __init__(self, val_tok):
        self.val_tok = val_tok
    def __repr__(self):
        return f"{self.val_tok.data}"
class BinOpNode:
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation
        
    def __repr__(self):
        return f"[{self.left} {self.operation} {self.right}]"

class UnOpNode:
    def __init__(self, val_tok, op_tok):
        self.val_tok = val_tok
        self.op_tok = op_tok
    def __repr__(self):
        return f"[{self.val_tok.data} {self.op_tok}]"
        

class Parser:
    def __init__(self, token_list, statement):
        self.statement = statement
        self.register = ParseRegister(token_list)
    
    def visit_statement(self):
        if self.register.current().matches(TT_ASSIGN):
            self.register.advance()
            out = self.visit_assign()
            return out
        elif self.register.current().matches(TT_OUTPUT):
            self.register.advance()
            out = self.visit_output()
            return out
        else:
            return Error("SYNTAX ERROR", self.statement, 
                         "Expected 'let' or 'show'", self.register.current().position)
            
    def visit_assign(self):
        if not self.register.current().matches(TT_ID):
            return Error("SYNTAX ERROR", self.statement, "Expected Variable ID",
                         self.register.current().position)
        id_tok = self.register.current()
        self.register.advance()
        
        if not self.register.current().matches(TT_EQ):
            return Error("SYNTAX ERROR", self.statement, "Expected '='",
                         self.register.current().position)
        self.register.advance()
        
        expr = self.visit_expr()
        if type(expr) is Error:
            return expr
        
        return AssignNode(id_tok, expr)
    
    def visit_expr(self):
        if self.register.current().matches(TT_END):
            return Error("PARSER ERROR", self.statement, "Unexpected end of statement", self.register.current().position)
        if self.register.current().matches(TT_LPAREN):
            logger.debug("Create Parentheses")
            self.register.advance()
            out = self.visit_expr()
            
            if type(out) is Error:
                return out
            
            if not self.register.current().matches(TT_RPAREN):
                return Error("SYNTAX ERROR", self.statement, "Expected ')'",
                             self.register.current().position)
            node1 = out
        elif self.register.current().matches_any(TT_NUM, TT_ID):
            tok1 = self.register.current()
            
            if self.register.next().matches_any(TT_LANG,TT_RANG):
                if not tok1.matches(TT_ID):
                    return Error("SYNTAX ERROR", self.statement, 
                                 "Unexpected angle bracket on number type", self.register.next().position)
                self.register.advance()
                node1 = UnOpNode(tok1, self.register.current())
            else:
                node1 = ValueNode(tok1)
        else:
            return Error("SYNTAX ERROR", self.statement, 
                         "Unexpected Error", self.register.current().position)
        if self.register.next().matches_any(TT_END, TT_RPAREN):
                self.register.advance()
                return node1
                
        self.register.advance()
        
        if self.register.current().matches_any(TT_ADD, TT_SUB, TT_MUL, TT_DIV):
            op = self.register.current()
            self.register.advance()
            node2 = self.visit_expr()
            
            if type(node2) is Error:
                return node2
            return BinOpNode(node1, node2, op)
                
            
            
        return Error("SYNTAX ERROR", self.statement,
                        "Unexpected token", self.register.current().position)
    
    def visit_output(self):
        if not self.register.current().matches(TT_ID):
            if not self.register.current().data in ("pitching", "batting"):
                return Error("SYNTAX ERROR", self.statement,
                             "Expected 'pitching' or 'batting'", self.register.current().position)
        output_type = self.register.current()
        self.register.advance()
        if not self.register.current().matches(TT_LBRACK):
            return Error("SYNTAX ERROR", self.statement, 
                         "Exected '[", self.register.current().position)
        self.register.advance()
        if not self.register.current().matches(TT_NUM):
            return Error("SYNTAX ERROR", self.statement, 
                         "Exected Number", self.register.current().position)
        from_year = self.register.current()
        self.register.advance()
        if self.register.current().matches(TT_RBRACK):
            to_year = from_year
            self.register.advance()
        elif self.register.current().matches(TT_COMMA):
            self.register.advance()
            if not self.register.current().matches(TT_NUM):
                return Error("SYNTAX ERROR", self.statement, 
                            "Exected Number", self.register.current().position)
            to_year = self.register.current()
            self.register.advance()
            if not self.register.current().matches(TT_RBRACK):
                return Error("SYNTAX ERROR", self.statement, 
                            "Exected ']'", self.register.current().position)
            self.register.advance()
        else:
            return Error("SYNTAX ERROR", self.statement, 
                        "Exected Number or ']'", self.register.current().position)
        
        if not self.register.current().matches(TT_LPAREN):
            return Error("SYNTAX ERROR", self.statement, 
                        "Exected '('", self.register.current().position)
        self.register.advance()
        params = []
        while True:
            if not self.register.current().matches(TT_ID):
                return Error("SYNTAX ERROR", self.statement, 
                            "Expected ID", self.register.current().position)
            params.append(self.register.current())
            self.register.advance()
            if self.register.current().matches(TT_COMMA):
                self.register.advance()
                continue
            elif self.register.current().matches(TT_RPAREN):
                break
            else:
                return Error("SYNTAX ERROR", self.statement, 
                            "Unexpected Token", self.register.current().position)
        
        
        
        self.register.advance()
        
        if not self.register.current().matches_any(TT_TOP, TT_BOT):
            return Error("SYNTAX ERROR", self.statement, 
                        "Exected 'top' or 'bot'", self.register.current().position)
        qualifier = self.register.current()
        self.register.advance()
        
        if not self.register.current().matches(TT_NUM):
            return Error("SYNTAX ERROR", self.statement, 
                        "Exected Number", self.register.current().position)    
        num = self.register.current() 
        
        self.register.advance()
        if not self.register.current().matches(TT_ID):
            return Error("SYNTAX ERROR", self.statement, 
                        "Exected ID", self.register.current().position)
        sort_stat = self.register.current()
        return OutputNode(output_type,from_year,to_year,params,qualifier,num, sort_stat)