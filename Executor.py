from Error import Error, Success
from Tokens import *
from Parser import ValueNode, BinOpNode, UnOpNode

import logging
logging.basicConfig()
logger = logging.getLogger("manfred")

from pybaseball import pitching_stats, batting_stats
from pybaseball import cache
cache.enable()

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
            if str(node.val_tok.data + qualifier) in row.keys():
                return self.row[str(node.val_tok.data + qualifier)]
            else:
                pass
                #logger.debug(str(node.val_tok.data + qualifier))
class Executor:
    def __init__(self, output_node, statement):
        self.output_node = output_node
        self.statement = statement
    def execute(self, context):
        from_y = int(self.output_node.from_year.data)
        to_y   = int(self.output_node.to_year.data)
        if self.output_node.output_type.data == "batting":
            data=batting_stats(from_y, to_y)
        if self.output_node.output_type.data == "pitching":
            data=pitching_stats(from_y,to_y)
        
        #print(data.columns)
        for p in self.output_node.params:
            if not (p.data in (data.columns) or p.data in context.keys()):
                return Error("SYNTAX ERROR", self.statement, f"ID {p.data} does not exist", p.position)
        
        if not (self.output_node.sort_stat.data in (data.columns) or self.output_node.sort_stat.data in context.keys()):
                return Error("SYNTAX ERROR", self.statement, f"ID {self.output_node.sort_stat.data} does not exist", self.output_node.sort_stat.position)
        
        out_data=[]
        for idx, r in data.iterrows():
            tmp = {}
            for p in self.output_node.params:
                if p.data in data.columns:
                    tmp[p.data] = r[p.data]
                elif p.data in context.keys():
                    v = Visitor(r, context)
                    val = v.visit(context[p.data])
                    if type(val) is float:
                        val = round(val, 4)
                    tmp[p.data] = val
            out_data.append(tmp)
        
        
            
        #print(out_data[0])
        key_len = []
        for key in out_data[0].keys():
            max_len = max([len(str(i[key])) for i in out_data])
            key_len.append(max(max_len, len(key)))
            print(left_justify(key, key_len[-1]),end=" | ")
        print()
        
        reverse = self.output_node.qualifier.matches(TT_TOP)
        out_data.sort(key=lambda x: x[self.output_node.sort_stat.data], reverse=reverse)
        
        for i in range(int(self.output_node.num.data)):
            stats = out_data[i]
            for k, i in zip(key_len, stats.values()):
                print(left_justify(str(i), k), end = " | ")
            print()
            
                
        
if __name__ == "__main__":
    tmp = pitching_stats(2023,2023)
    open("PitchingCommands.txt","w").write("\n".join(tmp.columns))
    tmp = batting_stats(2023,2023)
    open("BattingCommands.txt","w").write("\n".join(tmp.columns))