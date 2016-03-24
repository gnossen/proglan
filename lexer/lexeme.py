# Author: Richard Belleville

class Lexeme:
    gen_purp =      -2
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
    WHILE =         13
    ELSE =          14
    PLUS =          15
    MINUS =         16
    TIMES =         17
    DIVIDE =        18
    LAMBDA =        19
    DOUBLE_EQUAL =  20
    GREATER_THAN =  21
    LESS_THAN =     22
    RETURN =        23
    AND =           24
    OR =            25
    XOR =           26
    BITWISE_AND =   27
    BITWISE_OR =    28
    BITWISE_XOR =   29

    funcDef =       30
    optParamlist =  31
    paramList =     32
    optExprList =   33
    exprList =      34
    expr =          35
    varDecl =       36
    varAssign =     37
    ifExpr =        38
    elseExpr =      39
    whileExpr =     40
    primary =       41
    operator =      42
    funcCall =      43
    optAnonArg =    44
    optArglist =    45
    argList =       46
    anonFunc =      47
    identExpr =     48
    primExpr =      49

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
