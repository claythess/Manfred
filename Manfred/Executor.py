from Manfred.Error import Error, Success
from Manfred.Tokens import *
from Manfred.Parser import ValueNode, BinOpNode, UnOpNode, CompareNode
from Manfred.Lexer import Token

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")

from pybaseball import pitching_stats, batting_stats
from pybaseball import cache
cache.enable()

from colorama import init; init()
from colorama import Fore

COLOR_THEMES = {
    "default":[Fore.LIGHTWHITE_EX, Fore.LIGHTBLACK_EX],
    "eggshell":[Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX],
    "wine":[Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX],
    "oceanic":[Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.BLUE],
    "night":[Fore.LIGHTBLACK_EX, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA],
    "forest":[Fore.LIGHTGREEN_EX, Fore.GREEN, Fore.LIGHTBLACK_EX],
    "america":[Fore.LIGHTWHITE_EX, Fore.RED, Fore.LIGHTBLUE_EX]
}

def left_justify(text, length):
    if len(text) < length:
        return text + " " * (length - len(text))
    else:
        return text

class Visitor:
    def __init__(self, row, context):
        self.row = row
        self.context = context
    def visit(self, node):
        if type(node) is ValueNode:
            if node.val_tok.matches(TT_NUM):
                return node.val_tok.data
            if node.val_tok.matches(TT_ID):
                if node.val_tok.data in self.row.keys():
                    if node.val_tok.data == "Dollars":
                        return float(str(self.row[node.val_tok.data]).strip("$"))
                    else:    
                        return self.row[node.val_tok.data]
                else:
                    return self.visit(self.context[node.val_tok.data])
        elif type(node) is BinOpNode:
            if node.operation.matches(TT_ADD):
                return self.visit(node.left) + self.visit(node.right)
            if node.operation.matches(TT_SUB):
                return self.visit(node.left) - self.visit(node.right)
            if node.operation.matches(TT_MUL):
                return self.visit(node.left) * self.visit(node.right)
            if node.operation.matches(TT_DIV):
                return self.visit(node.left) / self.visit(node.right)
        elif type(node) is UnOpNode:
            
            if node.op_tok.matches(TT_RANG):
                qualifier  = "+"
            if node.op_tok.matches(TT_LANG):
                qualifier  = "-"
            if str(node.val_tok.data + qualifier) in self.row.keys():
                return self.row[str(node.val_tok.data + qualifier)]
            else:
                pass
                #logger.debug(str(node.val_tok.data + qualifier))
        elif type(node) is CompareNode:
            if node.id_tok.data in self.row.keys():
                left_value = self.row[node.id_tok.data]
            elif node.id_tok.data in self.context.keys():
                left_value = self.visit(self.context[node.id_tok.data])
            
            right_value = node.value_tok.data
            
            if node.comp_tok.matches(TT_RANG):
                return left_value > right_value
            elif node.comp_tok.matches(TT_LANG):
                return left_value < right_value
            elif node.comp_tok.matches(TT_EQ):
                return left_value == right_value
                
class Executor:
    def __init__(self, output_node, statement):
        self.output_node = output_node
        self.statement = statement
    
    def execute(self, context, output_color):
        logger.debug("OUT COLOR " + str(output_color))
        if output_color:
            if output_color in COLOR_THEMES.keys():
                output_color = COLOR_THEMES[output_color]
            else:
                output_color = COLOR_THEMES["default"]
        from_y = int(self.output_node.from_year.data)
        to_y   = int(self.output_node.to_year.data)
        
        if self.output_node.output_type.data == "batting":
            data=batting_stats(from_y, to_y, qual = 1)
        elif self.output_node.output_type.data == "qbatting":
            data=batting_stats(from_y, to_y)
        elif self.output_node.output_type.data == "abatting":
            data=batting_stats(from_y, to_y, ind = 0)
        elif self.output_node.output_type.data == "pitching":
            data=pitching_stats(from_y,to_y, qual = 1)
        elif self.output_node.output_type.data == "qpitching":
            data=pitching_stats(from_y,to_y)
        elif self.output_node.output_type.data == "apitching":
            data=pitching_stats(from_y,to_y, ind = 0)
        else:
            return Error("SYNTAX ERROR",self.statement, f"Unrecognized output type {self.output_node.output_type.data}",self.output_node.output_type.position)
        
    
        p_pos = 0
        # iterate by while loop, since size of arr is variable
        while p_pos < len(self.output_node.params):
            for name, values in BUILT_IN_FUNCTIONS.items():
                if not self.output_node.params[p_pos].data == name: continue
                old_tok = self.output_node.params.pop(p_pos)
                if  "pitching" in self.output_node.output_type.data:
                    new_stats = [Token(TT_ID, old_tok.position, i) for i in values["pitching"]]
                elif  "batting" in self.output_node.output_type.data:
                    new_stats = [Token(TT_ID, old_tok.position, i) for i in values["batting"]]
                for i in range(len(new_stats)):
                    self.output_node.params.insert(i + p_pos, new_stats[i])
            p_pos += 1
        logger.debug("Parameters")
        logger.debug(self.output_node.params)
        
        # Check that all parametes actually exist before visiting them
        for p in self.output_node.params:
            if not (p.data in (data.columns) or p.data in context.keys()):
                logger.debug("Syntax error " + str(p))
                return Error("SYNTAX ERROR", self.statement, f"ID {p.data} does not exist", p.position)
            
                
        
        for p in self.output_node.comp_nodes:
            if not (p.id_tok.data in (data.columns) or p.id_tok.data in context.keys()):
                return Error("SYNTAX ERROR", self.statement, f"ID {p.id_tok.data} does not exist", p.id_tok.position)
        
        if not (self.output_node.sort_stat.data in (data.columns) or self.output_node.sort_stat.data in context.keys()):
                return Error("SYNTAX ERROR", self.statement, f"ID {self.output_node.sort_stat.data} does not exist", self.output_node.sort_stat.position)
        
        out_data=[]
        count=0
        
        for idx, r in data.iterrows():
            tmp = {}
            v = Visitor(r, context)
            if len(self.output_node.comp_nodes) > 0:
                pass_comparisons = True
                for comparison in self.output_node.comp_nodes:
                    if not v.visit(comparison):
                        pass_comparisons = False
                        break
                if not pass_comparisons:
                    continue
            count+=1
            for p in self.output_node.params:
                if p.data in data.columns:
                    tmp[p.data] = r[p.data]
                elif p.data in context.keys():
                    # Coding gods forgive me for using a try statement
                    try:
                        val = v.visit(context[p.data])
                    except KeyError:
                        return Error("EXECUTION ERROR", self.statement,
                                     f"Invalid result for {p.data}, check if parameters exist", p.position)
                    if type(val) is float:
                        val = round(val, 4)
                    tmp[p.data] = val
            out_data.append(tmp)
        
        logger.debug(count)

        # Generate lengths for each column, and output headers
        color_idx = 0
        if output_color: print(output_color[0], end="")
            
        key_len = []
        for key in out_data[0].keys():
            max_len = 0
            for i in out_data:
                j = i[key]
                if type(j) is float:
                    j = round(j, 4)
                max_len = max(max_len, len(str(j)))
                
            key_len.append(max(max_len, len(key)))
            print(left_justify(key, key_len[-1]),end=" | ")
        print()
        
        
        for i in range(len(out_data[0].keys())):
            print("-" * key_len[i],end="-|-")
            
        if output_color: print(Fore.RESET, end="")
        print()
        logger.debug(key_len)
        
        # Sort Stats
        reverse = self.output_node.qualifier.matches(TT_TOP)
        logger.debug(out_data[0])
        logger.debug(self.output_node.sort_stat.data)
        out_data.sort(key=lambda x: x[self.output_node.sort_stat.data], reverse=reverse)
        logger.debug(len(out_data))
        # Outuput Actual data
        
        for i in range(int(self.output_node.num.data)):
            if i >= len(out_data):
                break
            
            
            if output_color: 
                color_idx += 1
                color_idx = color_idx % len(output_color)
                print(output_color[color_idx], end="")
            
            stats = out_data[i]
            for k, i in zip(key_len, stats.values()):
                if type(i) is float:
                    i = round(i, 4)
                print(left_justify(str(i), k), end = " | ")
            print()
            if output_color: print(Fore.RESET, end="")
            
if __name__ == "__main__":
    tmp = pitching_stats(2023,2023)
    open("PitchingCommands.txt","w").write("\n".join(tmp.columns))
    tmp = batting_stats(2023,2023)
    open("BattingCommands.txt","w").write("\n".join(tmp.columns))