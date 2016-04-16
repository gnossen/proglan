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
    NOT =           29
    BITWISE_AND =   30
    BITWISE_OR =    31
    BITWISE_XOR =   32
    NEWLINE =       33
    SEMICOLON =     34
    BOOL =          35
    NULL =          36
    LEQ =           37
    GEQ =           38
    NEQ =           39
    COLON =         40
    DOT =           41
    TRIPLE_EQ =     42
    NOT_TRIPLE_EQ = 43

    funcDef =       44
    optParamlist =  45
    paramList =     46
    optExprList =   47
    exprList =      48
    expr =          49
    varDecl =       50
    varAssign =     51
    ifExpr =        52
    elseExpr =      53
    whileExpr =     54
    primary =       55
    operator =      56
    funcCall =      57
    optAnonArg =    58
    optArglist =    59
    argList =       60
    anonFunc =      61
    identExpr =     62
    primExpr =      63
    arrayAccess =   64
    arrayLiteral =  65
    env =           66
    function =      67
    array =         68
    returnExpr =    69
    builtIn =       70
    funcParam =     71
    cons =          72
    attribAccess =  73
    notExpr =       74

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
