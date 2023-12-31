#!/usr/bin/python3

from Manfred.Error import Error, Success
from Manfred.Lexer import Lexer
from Manfred.Parser import Parser, OutputNode, AssignNode
from Manfred.Executor import Executor

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")


from colorama import init; init()
from colorama import Fore


import argparse

class Environment:
    def __init__(self):
        self.context = {} # Dictionary of variables
    
    def evaluate_statement(self, statement, color):
        # Jerry Rig Comments
        if statement.startswith('#') or len(statement.strip()) == 0:
            return Success()
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
            out = executor.execute(self.context, color)
            if type(out) == Error:
                return out
        
        return Success()
        

def REPL(color):
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
        
        result = env.evaluate_statement(tmp, color)
        if type(result) is Error:
            success = False
            result.output()
        else:
            success = True
            # Output error type


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Manfred",description="Meta Analysis Network, Full Reference Esoteric Database")
    
    parser.add_argument("-r","--repl", action="store_true", help="Open REPL Shell")
    
    parser.add_argument('-f', "--file", action="store", help="File ")
    
    parser.add_argument('-d', "--debug", action="store_true", help="Debug Info")
    
    parser.add_argument('-c', "--color",nargs='?',default="", const="default", action="store", help="Output in color")
    
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        
    if args.repl:
        REPL(args.color)
    elif args.file:
        env = Environment()
        statements = open(args.file,'r').read().splitlines()
        for s in statements:
            result = env.evaluate_statement(s, args.color)
            if type(result) is Error:
                result.output()
                break