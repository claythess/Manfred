from Error import Error, Success
from Tokens import *
from Lexer import Token
from copy import deepcopy

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")

class ParseRegister:
    def __init__(self, token_list):
        self.token_list = token_list
        self.position = 0
    def current(self) -> Token:
        return self.token_list[self.position]
    
    def advance(self):
        self.position += 1
    def next(self) -> Token:
        return self.token_list[self.position + 1]

class AssignNode:
    def __init__(self, id_tok, value_node):
        self.id_tok = id_tok
        self.value_node = value_node
    def __repr__(self):
        return f"{self.id_tok.data} = {self.value_node}"

class OutputNode:
    def __init__(self, output_type,from_year, to_year, params, qualifier, num, sort_stat, comp_nodes):
        self.output_type = output_type
        self.from_year = from_year
        self.to_year = to_year
        self.params = params
        self.qualifier = qualifier
        self.num = num
        self.sort_stat = sort_stat
        self.comp_nodes=comp_nodes
    def __repr__(self):
        return f"[{self.from_year.data} - {self.to_year.data}] ({self.params}) {self.qualifier} {self.num}"

class ValueNode:
    def __init__(self, val_tok):
        self.val_tok = val_tok
    def __repr__(self):
        return f"{self.val_tok.data}"
class BinOpNode:
    def __init__(self, left, right, operation, paren):
        self.left = left
        self.right = right
        self.operation = operation
        self.paren = paren
    def order_operations(self):
        '''
        if self.operation.matches_any(TT_MUL, TT_DIV):
            if type(self.left) is BinOpNode:
                if (self.left.operation.matches_any(TT_ADD, TT_SUB)):
                    return "left"
                    
            elif type(self.right) is BinOpNode:
                if (self.right.operation.matches_any(TT_ADD, TT_SUB)):
                    return "right"
        '''
        if self.operation.matches_any(TT_MUL, TT_DIV):
            if type(self.right) is BinOpNode:
                if self.paren >= self.right.paren:
                    return "rotate"            
        if self.operation.matches_any(TT_ADD, TT_SUB):
            if type(self.right) is BinOpNode:
                if (self.right.operation.matches_any(TT_ADD, TT_SUB) and self.paren >= self.right.paren):
                        return "rotate"
        
    def __repr__(self):
        return f"[{self.left} {self.operation} {self.right}]"

class UnOpNode:
    def __init__(self, val_tok, op_tok):
        self.val_tok = val_tok
        self.op_tok = op_tok
    def __repr__(self):
        return f"[{self.val_tok.data} {self.op_tok}]"
        
class CompareNode:
    def __init__(self, id_tok, comp_tok, value_tok):
        self.id_tok = id_tok
        self.comp_tok = comp_tok
        self.value_tok = value_tok
    def __repr__(self):
        return f"({self.id_tok.data} {self.comp_tok} {self.value_tok.data})"

class Parser:
    def __init__(self, token_list, statement):
        self.statement = statement
        self.register = ParseRegister(token_list)
    
    def visit_statement(self):
        if self.register.current().matches(TT_ASSIGN):
            self.register.advance()
            out = self.visit_assign()
            if type(out) is AssignNode:
                if type(out.value_node) is BinOpNode:
                    logger.debug("FIX BINOP")
                    tmp = self.pemdas(out.value_node)
                    out.value_node = tmp
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
        if id_tok.data in BUILT_IN_FUNCTIONS.keys():
            return Error("PARSER ERROR", self.register.statement,
                         f"{id_tok.data} exists as Built-In variable", self.register.place())
        self.register.advance()
        
        if not self.register.current().matches(TT_EQ):
            return Error("SYNTAX ERROR", self.statement, "Expected '='",
                         self.register.current().position)
        self.register.advance()
        
        expr = self.visit_expr()
        if not self.register.current().matches(TT_END):
            logger.warn("Expected End of line token")
        if type(expr) is Error:
            return expr
        
        return AssignNode(id_tok, expr)
    
    def visit_expr(self, paren = 0):
        logger.debug("Enter w Paren " + str(paren))
        if self.register.current().matches(TT_END):
            return Error("PARSER ERROR", self.statement, "Unexpected end of statement", self.register.current().position)
        if self.register.current().matches(TT_LPAREN):
            logger.debug("Create Parentheses")
            self.register.advance()
            out = self.visit_expr(paren = paren + 1)
            
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
                         f"Unexpected character", self.register.current().position)
        if self.register.next().matches_any(TT_END, TT_RPAREN):
                self.register.advance()
                return node1
                
        self.register.advance()
        
        if self.register.current().matches_any(TT_ADD, TT_SUB, TT_MUL, TT_DIV):
            op = self.register.current()
            self.register.advance()
            node2 = self.visit_expr(paren=paren)
            
            if type(node2) is Error:
                return node2
            logger.debug("Create binop w paren" + str(paren))
            out = BinOpNode(node1, node2, op, paren)
            
            return out
                
            
            
        return Error("SYNTAX ERROR", self.statement,
                        "Unexpected token", self.register.current().position)
    def pemdas(self, node):
        '''
        Recursively rotate nodes to implement pemdas
        still fiddly, but mostly works
        TODO
        fix let x = (1 * 2) + 3 / 4 - 5
        '''
        
        if type(node.right) is BinOpNode:
            node.right = self.pemdas(node.right)
        if type(node.left) is BinOpNode:
            node.left = self.pemdas(node.left)
        
        
        #logger.debug("L -> " +  node.left.__repr__())
        #logger.debug("R -> "+  node.right.__repr__())
        op = node.order_operations()
        
        out = node
            
        while op == "rotate":
            # 5 * [1 + 2]  --> [5 * 1] + 2
            
            #logger.debug("Before -> " + node.__repr__())
            #logger.debug("Rotate")
            #logger.debug(out.right)
            lnode = deepcopy(node.left)
            r_lnode = deepcopy(node.right.left)
            r_rnode = deepcopy(node.right.right)
            #logger.debug("L -> " + lnode.__repr__())
            #logger.debug("RL -> " + r_lnode.__repr__())
            #logger.debug("RR -> " + r_rnode.__repr__())
            op = deepcopy(node.operation)
            r_op = deepcopy(node.right.operation)
            #logger.debug("OP -> " + op.__repr__())
            #logger.debug("ROP -> " + r_op.__repr__())
            out = BinOpNode(BinOpNode(lnode, r_lnode, op, node.paren), r_rnode, r_op, node.right.paren)
            if type(out.right) is BinOpNode:
                out.right = self.pemdas(out.right)
            if type(out.left) is BinOpNode:
                out.left = self.pemdas(out.left)
            op = out.order_operations()
            if op == "rotate":
                logger.debug("REROTATE")
        #logger.debug(out)
        return out
    
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
            
            # Bit of a jerryrig, maybe I'll come back and add Nodes later
            p_tmp = self.register.current()                
            if self.register.next().matches(TT_LANG):
                p_tmp.data+="-"
                self.register.advance()
            elif self.register.next().matches(TT_RANG):
                p_tmp.data+="+"
                self.register.advance()
                
            params.append(p_tmp)
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
        comp_nodes = []
        if self.register.current().matches(TT_ID):
            
            while self.register.current().matches(TT_ID):
                name_tok = self.register.current()
                self.register.advance()
                
                if not self.register.current().matches_any(TT_EQ, TT_RANG, TT_LANG):
                    return Error("SYNTAX ERROR", self.statement, 
                            "Expected '='", self.register.current().position)
                op_tok = self.register.current()
                self.register.advance()
                if not self.register.current().matches_any(TT_ID, TT_NUM):
                    return Error("SYNTAX ERROR", self.statement, 
                            "Expected Number or ID", self.register.current().position)
                value_tok = self.register.current()
                self.register.advance()
                if not self.register.current().matches(TT_COMMA):
                    return Error("SYNTAX ERROR", self.statement, 
                            "Expected ','", self.register.current().position)
                self.register.advance()
                
                comp_nodes.append(CompareNode(name_tok, op_tok, value_tok))
            
        
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
        return OutputNode(output_type,from_year,to_year,params,qualifier,num, sort_stat, comp_nodes)