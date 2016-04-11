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
    OSQBRACE =      9
    CSQBRACE =      10
    COMMA =         11
    LET =           12
    EQUAL =         13
    IF =            14
    WHILE =         15
    ELSE =          16
    PLUS =          17
    MINUS =         18
    TIMES =         19
    DIVIDE =        20
    LAMBDA =        21
    DOUBLE_EQUAL =  22
    GREATER_THAN =  23
    LESS_THAN =     24
    RETURN =        25
    AND =           26
    OR =            27
    XOR =           28
    BITWISE_AND =   29
    BITWISE_OR =    30
    BITWISE_XOR =   31
    NEWLINE =       32
    SEMICOLON =     33
    BOOL =          34
    NULL =          35
    LEQ =           36
    GEQ =           37
    NEQ =           38
    COLON =         39

    funcDef =       40
    optParamlist =  41
    paramList =     42
    optExprList =   43
    exprList =      44
    expr =          45
    varDecl =       46
    varAssign =     47
    ifExpr =        48
    elseExpr =      49
    whileExpr =     50
    primary =       51
    operator =      52
    funcCall =      53
    optAnonArg =    54
    optArglist =    55
    argList =       56
    anonFunc =      57
    identExpr =     58
    primExpr =      59
    arrayAccess =   60
    arrayLiteral =  61
    env =           62
    function =      63
    array =         64
    returnExpr =    65
    builtIn =       66
    funcParam =     67

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
    for a, b in zip(A, B):
       if a != b or a.line != b.line or a.col != b.col:
           raise Exception("%s != %s" % (str(a), str(b)))

    if len(A) != len(B):
        raise Exception("Lengths do not match.")

    return True
