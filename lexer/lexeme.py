# Author: Richard Belleville

class Lexeme:
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

    def __init__(self, ltype, value=None): 
        self.type = ltype 
        self.value = value

    def is_type(self, ltype):
        return self.type == ltype

    def __str__(self):
        try:
            type_str = [key for key, value in Lexeme.__dict__.items() if value == self.type][0]
            if self.value is not None:
                return "%s: %s" % (type_str, str(self.value))
            else:
                return "%s" % type_str

        except:
            raise Exception("Tried to print lexeme of unknown type id: %d." % self.type)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

def match_lexemes(A, B):
    if len(A) != len(B):
        return False

    for a, b in zip(A, B):
       if a != b:
           return False

    return True
