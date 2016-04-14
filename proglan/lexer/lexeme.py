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
    DOT =           40
    TRIPLE_EQ =     41
    NOT_TRIPLE_EQ = 42

    funcDef =       43
    optParamlist =  44
    paramList =     45
    optExprList =   46
    exprList =      47
    expr =          48
    varDecl =       49
    varAssign =     50
    ifExpr =        51
    elseExpr =      52
    whileExpr =     53
    primary =       54
    operator =      55
    funcCall =      56
    optAnonArg =    57
    optArglist =    58
    argList =       59
    anonFunc =      60
    identExpr =     61
    primExpr =      62
    arrayAccess =   63
    arrayLiteral =  64
    env =           65
    function =      66
    array =         67
    returnExpr =    68
    builtIn =       69
    funcParam =     70
    cons =          71
    attribAccess =  72

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
