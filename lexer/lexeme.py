# Author: Richard Belleville

class Lexeme:
    GEN_PURP =      -2
    EOF =           -1
    UNKNOWN =       0
    NUMBER =        1
    STRING =        2
    IDENTIFIER =    3
    DEF =           4
    OPAREN =        5
    CPAREN =        6
    OBRACE =        7
    CBRACE =        8
    COMMA =         9
    LET =           10
    EQUAL =         11
    IF =            12
    ELSE =          13
    PLUS =          14
    MINUS =         15
    TIMES =         16
    DIVIDE =        17
    LAMBDA =        18
    DOUBLE_EQUAL =  19
    GREATER_THAN =  20
    LESS_THAN =     21

    funcDef =       22
    optParamlist =  23
    paramList =     24
    optExprList =   25
    exprList =      26
    expr =          27
    varDecl =       28
    varAssign =     29
    ifExpr =        30
    elseExpr =      31
    whileExpr =     32
    primary =       33
    operator =      34
    funcCall =      35
    optAnonArg =    36
    optArglist =    37
    argList =       38
    anonFunc =      39
    identExpr =     40
    primExpr =      41

    def __init__(self, ltype, value=None, line=None, col=None, left=None, right=None): 
        self.type = ltype 
        self.value = value
        self.line = line
        self.col = col

        self.left = left
        self.right = right

    def is_type(self, ltype):
        return self.type == ltype

    def get_type(self):
        try:
            return [key for key, value in Lexeme.__dict__.items() if value == self.type][0]
        except:
            raise Exception("Tried to get type of unknown lexeme id: %d." % self.type)

    def __str__(self):
        type_str = self.get_type() 
        if self.line is not None and self.col is not None:
            if self.value is not None:
                return "%s: %s (%d, %d)" % (type_str, str(self.value), self.line + 1, self.col + 1)
            else:
                return "%s (%d, %d)" % (type_str, self.line + 1, self.col + 1)
        else:
            if self.value is not None:
                return "%s: %s" % (type_str, str(self.value))
            else:
                return "%s" % type_str



    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

def match_lexemes(A, B):
    if len(A) != len(B):
        return False

    for a, b in zip(A, B):
       if a != b or a.line != b.line or a.col != b.col:
           return False

    return True
