# Author: Richard Belleville

import os
from ..lexer.lexeme import *
from ..lexer.scanner import *

class Parser:
    def __init__(self, input=None, file=None):
        if input is not None:
            self.load_str(input)
        elif file is not None:
            self.load_file(file)
        else:
            self.input = None

    def load_file(self, filename):
        filepath = filename
        if not os.path.isabs(filename):
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(cur_dir, filename)

        with open(filepath, 'r') as f:
            self.input = f.read()

    def load_str(self, str):
        self.input = str


    def current(self, skip=True):
        if skip == False:
            if len(self.input) != 0:
                return self.input[0]
            else:
                return None
        else:
            # skip over any newlines
            for lexeme in self.input:
                if lexeme.type != Lexeme.NEWLINE:
                    return lexeme
            else:
                return None

    def check(self, lexeme_type, skip=True):
        if lexeme_type == Lexeme.NEWLINE or skip == False:
            return self.current(skip=False).type == lexeme_type
        else:
            return self.current().type == lexeme_type

    def match(self, lexeme_type, skip=True):
        skip_newlines = True
        if lexeme_type == Lexeme.NEWLINE or skip == False:
            skip_newlines = False

        if not self.check(lexeme_type):
            typed_lexeme = Lexeme(lexeme_type)
            raise Exception("Syntax Error: Invalid token '%s'. Expected '%s'." % (str(self.current()), typed_lexeme.get_type()))
        else:
            return self.advance(skip=skip_newlines)

    def advance(self, skip=True):
        if skip == False:
            cur = self.current(skip=False)
            if cur is not None:
                self.input = self.input[1:]
                return cur
            else:
                return None
        else:
            while self.current(skip=False).type == Lexeme.NEWLINE:
                self.advance(skip=False)

            return self.advance(skip=False)

    def parse(self):
        self.input = Scanner(input=self.input).scan()
        return self.parse_optExprList()
    
    def parse_optParamList(self):
        if self.paramList_pending():
            return self.parse_paramList()
        else:
            return None

    def paramList_pending(self):
        return self.check(Lexeme.IDENTIFIER)

    def parse_paramList(self):
        param = self.match(Lexeme.IDENTIFIER)
        sublist = None

        if self.check(Lexeme.COMMA):
            self.advance()
            sublist = self.parse_paramList()

        return make_paramList(param, sublist)

    def parse_optExprList(self):
        if self.expr_pending():
            return self.parse_exprList()
        else:
            return None

    def parse_exprList(self):
        listcar = self.parse_expr()
        listcdr = None

        if self.check(Lexeme.NEWLINE):
            self.match(Lexeme.NEWLINE)
            listcdr = self.parse_optExprList()
        elif self.check(Lexeme.SEMICOLON):
            self.match(Lexeme.SEMICOLON)
            listcdr = self.parse_optExprList()

        return make_exprList(listcar, listcdr)

    def parse_binop_level(self, parse_next_level, level_ops):
        a = parse_next_level(self)
        for op in level_ops:
            if self.check(op):
                self.match(op)
                b = self.parse_binop_level(parse_next_level, level_ops)
                return make_primExpr(a, Lexeme(op), b)

        return a

    def expr_pending(self):
        return self.expr1_pending() or self.check(Lexeme.LET)

    def parse_expr(self):
        if self.check(Lexeme.LET):
            self.match(Lexeme.LET)
            var_name = self.match(Lexeme.IDENTIFIER)

            self.match(Lexeme.EQUAL)
            val = self.parse_expr1()
            return make_varDecl(var_name, val)

        expr = self.parse_expr1()
        if self.check(Lexeme.EQUAL):
            self.match(Lexeme.EQUAL)
            expr2 = self.parse_expr()
            return make_varAssign(expr, expr2)
        elif self.check(Lexeme.PLUS_EQUAL):
            self.match(Lexeme.PLUS_EQUAL)
            expr2 = self.parse_expr()
            return make_primExpr(expr, Lexeme(Lexeme.PLUS_EQUAL), expr2)
        elif self.check(Lexeme.MINUS_EQUAL):
            self.match(Lexeme.MINUS_EQUAL)
            expr2 = self.parse_expr()
            return make_primExpr(expr, Lexeme(Lexeme.MINUS_EQUAL), expr2)
        else:
            return expr

    def expr1_pending(self):
        return self.expr2_pending()

    def parse_expr1(self):
        level1_ops = [Lexeme.AND, Lexeme.OR, Lexeme.XOR]
        return self.parse_binop_level(Parser.parse_expr2, level1_ops)

    def expr2_pending(self):
        return self.expr3_pending()

    def parse_expr2(self):
        level2_ops = [Lexeme.DOUBLE_EQUAL, Lexeme.NEQ, Lexeme.GREATER_THAN, Lexeme.LESS_THAN,
                        Lexeme.LEQ, Lexeme.GEQ, Lexeme.TRIPLE_EQ, Lexeme.NOT_TRIPLE_EQ]
        return self.parse_binop_level(Parser.parse_expr3, level2_ops)

    def expr3_pending(self):
        return self.expr4_pending()

    def parse_expr3(self):
        level3_ops = [Lexeme.PLUS, Lexeme.MINUS]
        return self.parse_binop_level(Parser.parse_expr4, level3_ops)
   
    def expr4_pending(self):
        return self.expr5_pending()

    def parse_expr4(self):
        level4_ops = [Lexeme.TIMES, Lexeme.DIVIDE]
        return self.parse_binop_level(Parser.parse_expr5, level4_ops)

    def expr5_pending(self):
        return self.expr6_pending()
    
    def parse_expr5(self):
        level5_ops = [Lexeme.BITWISE_AND, Lexeme.BITWISE_OR, Lexeme.BITWISE_XOR]
        return self.parse_binop_level(Parser.parse_expr6, level5_ops)

    def expr6_pending(self):
        return self.expr7_pending()

    def parse_expr6(self):
        expr = self.parse_expr7()
        while self.check(Lexeme.OPAREN, skip=False) or \
                self.check(Lexeme.OSQBRACE, skip=False) or \
                self.check(Lexeme.DOT, skip=False):

            if self.check(Lexeme.OPAREN, skip=False):
                self.match(Lexeme.OPAREN)
                args = self.parse_optArgList()
                self.match(Lexeme.CPAREN)
                
                anon_arg = None
                if self.check(Lexeme.OBRACE):
                    self.match(Lexeme.OBRACE)
                    anon_arg = self.parse_optExprList()
                    self.match(Lexeme.CBRACE)

                expr = make_funcCall(expr, args, anon_arg)

            if self.check(Lexeme.OSQBRACE, skip=False):
                self.match(Lexeme.OSQBRACE)
                index_expr = self.parse_expr()
                self.match(Lexeme.CSQBRACE)
                expr = make_arrayAccess(expr, index_expr)

            while self.check(Lexeme.DOT, skip=False):
                self.match(Lexeme.DOT)
                attr = self.match(Lexeme.IDENTIFIER)
                expr = make_attribAccess(expr, attr)
            
        return expr

    def expr7_pending(self):
        return self.primary_pending() or \
                self.ifExpr_pending() or \
                self.whileExpr_pending() or \
                self.anonFunc_pending() or \
                self.funcDef_pending() or \
                self.arrayLiteral_pending() or \
                self.check(Lexeme.OPAREN) or \
                self.unaryOpExpr_pending()

    def parse_expr7(self):
        if self.primary_pending():
            return self.parse_primary()
        if self.check(Lexeme.DEF):
            self.match(Lexeme.DEF)
            if self.check(Lexeme.OPAREN):
                return self.parse_anonFunc()
            else:
                return self.parse_funcDef()
        elif self.ifExpr_pending():
            return self.parse_ifExpr()
        elif self.whileExpr_pending():
            return self.parse_whileExpr()
        elif self.arrayLiteral_pending():
            return self.parse_arrayLiteral()
        elif self.unaryOpExpr_pending():
            return self.parse_unaryOpExpr()
        else:
            self.match(Lexeme.OPAREN)
            expr = self.parse_expr()
            self.match(Lexeme.CPAREN)
            return expr

    def unaryOpExpr_pending(self):
        return self.check(Lexeme.RETURN) or \
                self.check(Lexeme.NOT) or \
                self.check(Lexeme.NEW) or \
                self.check(Lexeme.MINUS)

    def parse_unaryOpExpr(self):
        if self.check(Lexeme.RETURN):
            self.match(Lexeme.RETURN)
            expr = self.parse_expr()
            return make_returnExpr(expr)
        elif self.check(Lexeme.NOT):
            self.match(Lexeme.NOT)
            expr = self.parse_expr()
            return make_notExpr(expr)
        elif self.check(Lexeme.NEW):
            self.match(Lexeme.NEW)
            expr = self.parse_expr()
            return make_newExpr(expr)
        else:
            self.match(Lexeme.MINUS)
            expr = self.parse_expr()
            return make_minusExpr(expr)

    def varDecl_pending(self):
        return self.check(Lexeme.LET)

    def parse_varDecl(self):
        self.match(Lexeme.LET)
        var_name = self.match(Lexeme.IDENTIFIER)

        self.match(Lexeme.EQUAL)
        val = self.parse_expr()
        return make_varDecl(var_name, val)

    def ifExpr_pending(self):
        return self.check(Lexeme.IF)

    def parse_ifExpr(self):
        self.match(Lexeme.IF)
        self.match(Lexeme.OPAREN)
        condition = self.parse_expr()
        self.match(Lexeme.CPAREN)
        self.match(Lexeme.OBRACE)
        body = self.parse_exprList()
        self.match(Lexeme.CBRACE)

        else_clause = None
        if self.elseExpr_pending():
            else_clause = self.parse_elseExpr()

        return make_ifExpr(condition, body, else_clause)

    def elseExpr_pending(self):
        return self.check(Lexeme.ELSE)

    def parse_elseExpr(self):
        self.match(Lexeme.ELSE)
        if self.ifExpr_pending():
            if_expr = self.parse_ifExpr()
            return make_elseExpr(None, if_expr)
        else:
            self.match(Lexeme.OBRACE)
            expr_list = self.parse_exprList()
            self.match(Lexeme.CBRACE)
            return make_elseExpr(expr_list, None)

    def whileExpr_pending(self):
        return self.check(Lexeme.WHILE)

    def parse_whileExpr(self):
        self.match(Lexeme.WHILE)
        self.match(Lexeme.OPAREN)
        condition = self.parse_expr()
        self.match(Lexeme.CPAREN)
        self.match(Lexeme.OBRACE)
        expr_list = self.parse_exprList()
        self.match(Lexeme.CBRACE)

        return make_whileExpr(condition, expr_list)

    def anonFunc_pending(self):
        return self.check(Lexeme.LAMBDA)

    def parse_anonFunc(self):
        self.match(Lexeme.OPAREN)
        param_list = self.parse_optParamList()
        self.match(Lexeme.CPAREN)

        func_param = None
        if self.funcParam_pending():
            func_param = self.parse_funcParam()

        self.match(Lexeme.OBRACE)
        body = self.parse_optExprList()
        self.match(Lexeme.CBRACE)

        return make_anonFunc(param_list, func_param, body)

    def arrayLiteral_pending(self):
        return self.check(Lexeme.OSQBRACE)

    def parse_arrayLiteral(self):
        self.match(Lexeme.OSQBRACE)
        members = self.parse_optCommaExprList()
        self.match(Lexeme.CSQBRACE)
        return make_arrayLiteral(members)

    def parse_optCommaExprList(self):
        if self.expr_pending():
            return self.parse_commaExprList()
        else:
            return None

    def parse_commaExprList(self):
        car = self.parse_expr()
        cdr = None
        if self.check(Lexeme.COMMA):
            self.match(Lexeme.COMMA)
            cdr = self.parse_commaExprList()

        return make_list(car, cdr)

    def funcDef_pending(self):
        return self.check(Lexeme.DEF)

    def parse_funcDef(self):
        func_name = self.match(Lexeme.IDENTIFIER)
        self.match(Lexeme.OPAREN)
        param_list = self.parse_optParamList()
        self.match(Lexeme.CPAREN)

        func_param = None
        if self.funcParam_pending():
            func_param = self.parse_funcParam()

        self.match(Lexeme.OBRACE)
        expr_list = self.parse_optExprList()
        self.match(Lexeme.CBRACE)

        return make_funcDef(func_name, param_list, func_param, expr_list)

    def funcParam_pending(self):
        return self.check(Lexeme.OPAREN)

    def parse_funcParam(self):
        self.match(Lexeme.OPAREN)
        name = self.match(Lexeme.IDENTIFIER)
        
        params = None
        if self.check(Lexeme.COLON):
            self.match(Lexeme.COLON)
            params = self.parse_paramList()

        self.match(Lexeme.CPAREN)
        return make_funcParam(name, params)

    def primary_pending(self):
        return self.check(Lexeme.NUMBER) or \
                self.check(Lexeme.STRING) or \
                self.check(Lexeme.IDENTIFIER) or \
                self.check(Lexeme.BOOL) or \
                self.check(Lexeme.NULL)
    
    def parse_primary(self):
        if self.check(Lexeme.NUMBER):
            return self.match(Lexeme.NUMBER)
        elif self.check(Lexeme.STRING):
            return self.match(Lexeme.STRING)
        elif self.check(Lexeme.BOOL):
            return self.match(Lexeme.BOOL)
        elif self.check(Lexeme.NULL):
            return self.match(Lexeme.NULL)
        else:
            return self.match(Lexeme.IDENTIFIER)

    def parse_optArgList(self):
        if self.argList_pending():
            return self.parse_argList()
        else:
            return None

    def argList_pending(self):
        return self.expr_pending()

    def parse_argList(self):
        arg = self.parse_expr()
        
        sublist = None
        if self.check(Lexeme.COMMA):
            self.advance()
            sublist = self.parse_argList()

        return make_argList(arg, sublist)

def make_funcDef(func_name, param_list, func_param, expr_list):
    gen_purp2 = Lexeme(Lexeme.gen_purp, left=func_param, right=expr_list)
    gen_purp1 = Lexeme(Lexeme.gen_purp, left=param_list, right=gen_purp2)
    return Lexeme(Lexeme.funcDef, left=func_name, right=gen_purp1)

def make_paramList(param, sublist):
    return Lexeme(Lexeme.paramList, left=param, right=sublist)

def make_argList(arg, sublist):
    return Lexeme(Lexeme.argList, left=arg, right=sublist)

def make_exprList(expr, sublist):
    return Lexeme(Lexeme.exprList, left=expr, right=sublist)

def make_varDecl(var_name, value):
    return Lexeme(Lexeme.varDecl, left=var_name, right=value)

def make_ifExpr(condition, body, else_clause):
    gen_purp = Lexeme(Lexeme.gen_purp, left=body, right=else_clause)
    if_statement = Lexeme(Lexeme.ifExpr, left=condition, right=gen_purp)
    return if_statement

def make_elseExpr(body, if_expr):
    return Lexeme(Lexeme.elseExpr, left=body, right=if_expr)

def make_whileExpr(condition, expr_list):
    return Lexeme(Lexeme.whileExpr, left=condition, right=expr_list)

def make_primExpr(prim, op, expr):
    gen_purp = Lexeme(Lexeme.gen_purp, left=op, right=expr)
    return Lexeme(Lexeme.primExpr, left=prim, right=gen_purp)

def make_funcCall(func_name, arg_list, anon_arg):
    gen_purp = Lexeme(Lexeme.gen_purp, left=arg_list, right=anon_arg)
    return Lexeme(Lexeme.funcCall, left=func_name, right=gen_purp)

def make_anonFunc(param_list, func_param, body):
    gen_purp = Lexeme(Lexeme.gen_purp, left=func_param, right=body)
    return Lexeme(Lexeme.anonFunc, left=param_list, right=gen_purp)

def make_varAssign(var_name, value):
    return Lexeme(Lexeme.varAssign, left=var_name, right=value)

def make_arrayAccess(array_expr, index_expr):
    return Lexeme(Lexeme.arrayAccess, left=array_expr, right=index_expr)

def make_arrayLiteral(members):
    return Lexeme(Lexeme.arrayLiteral, left=members)

def make_list(car, cdr):
    return Lexeme(Lexeme.gen_purp, left=car, right=cdr)

def make_returnExpr(expr):
    return Lexeme(Lexeme.returnExpr, left=expr)

def make_funcParam(name, params):
    return Lexeme(Lexeme.funcParam, left=name, right=params)

def make_attribAccess(obj, attr):
    return Lexeme(Lexeme.attribAccess, left=obj, right=attr)

def make_notExpr(expr):
    return Lexeme(Lexeme.notExpr, left=expr)

def make_newExpr(expr):
    return Lexeme(Lexeme.newExpr, left=expr)

def make_minusExpr(expr):
    return Lexeme(Lexeme.minusExpr, left=expr)
