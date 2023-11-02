TT_NUM    = "NUM"
TT_ASSIGN = "ASSIGN" # 'let'
TT_OUTPUT = "OUTPUT" # 'show'
TT_TOP    = "TOP"
TT_BOT    = "BOT"
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

# List of built in variable names
BUILT_IN_FUNCTIONS = {
    "basic": {
        "batting": ["HR", "AVG", "OBP", "SLG", "OPS"],
        "pitching":["IP", "ERA", "SO", "G", "W", "L", "ERA"]
    },
    "statcast" : {
        "batting":["wRC+","wSB", "HR/FB%+", "xwOBA", "HardHit%", "BABIP+"],
        "pitching":["FIP","ERA-", "xFIP", "SIERA", "HR/FB%+", "Location+"]
    }
}