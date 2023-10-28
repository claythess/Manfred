from Error import Error, Success
from Lexer import Lexer
from Parser import Parser, OutputNode, AssignNode
from Executor import Executor

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")
logger.setLevel(logging.INFO)

from colorama import init; init()
from colorama import Fore

class Environment:
    def __init__(self):
        self.context = {} # Dictionary of variables
    
    def evaluate_statement(self, statement):
        lex = Lexer()
        out = lex.lex(statement)
        logger.debug(lex.tokens)
        if type(out) == Error:
            return out
        
        parse = Parser(lex.tokens, statement)
        out = parse.visit_statement()
        if type(out) == Error:
            return out
        logger.debug(out)
        if type(out) is AssignNode:
            self.context[out.id_tok.data] = out.value_node
        if type(out) is OutputNode:
            executor = Executor(out, statement)
            out = executor.execute(self.context)
            if type(out) == Error:
                return out
        
        return Success()
        


if __name__ == "__main__":
    env = Environment()
    success = True
    while True:
        if success:
            print("manfred " + Fore.GREEN + "$" + Fore.RESET, end="")
            tmp = input("> ")
        else:
            print("manfred " + Fore.RED + "!" + Fore.RESET, end="")
            tmp = input("> ")
        
        if tmp == "q":
            break
        
        result = env.evaluate_statement(tmp)
        if type(result) is Error:
            success = False
            result.output()
        else:
            success = True
            # Output error type
        
        