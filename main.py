from Error import Error, Success
from Lexer import Lexer

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")

logger.setLevel(logging.DEBUG)


class Environment:
    def __init__(self):
        self.context = {} # Dictionary of variables
    
    def evaluate_statement(self, statement):
        lex = Lexer()
        out = lex.lex(statement)
        logger.debug(lex.tokens)
        return out
        


if __name__ == "__main__":
    env = Environment()
    success = True
    while True:
        if success:
            tmp = input("manfred $> ")
        else:
            tmp = input("manfred !> ")
        
        if tmp == "q":
            break
        
        result = env.evaluate_statement(tmp)
        if type(result) is Error:
            success = False
            result.output()
        else:
            success = True
            # Output error type
        
        