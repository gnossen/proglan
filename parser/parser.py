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
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(cur_dir, filename)
        with open(filepath, 'r') as f:
            self.input = f.read()

    def load_str(self, str):
        self.input = str


    def current(self):
        if len(self.input) != 0:
            return self.input[0]
        else:
            return None

    def check(self, lexeme_type, offset=None):
        if offset is None:
            return self.current().type == lexeme_type
        else:
            if len(self.input) < (offset + 1):
                return False
            else:
                return self.input[offset].type == lexeme_type

    def match(self, lexeme_type):
        if not self.check(lexeme_type):
            raise Exception("Syntax Error: Invalid token '%s'.", str(self.current()))
        else:
            return self.advance()

    def advance(self):
        cur = self.current()
        if cur is not None:
            self.input = self.input[1:]
            return cur
        else:
            return None

    def parse(self):
        self.input = Scanner(input=self.input).scan()
        return self.parse_optExprList()
    
    def parse_optParamList(self):
        if self.paramList_pending():
            return self.parse_paramList()
        else:
            return make_paramList(None, None)

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
            return make_exprList(None, None)

    def parse_exprList(self):
        expr = self.parse_expr()
        sublist = None

        if self.expr_pending():
            sublist = self.parse_exprList()

        return make_exprList(expr, sublist)

    def expr_pending(self):
        return self.check(Lexeme.OPAREN) or \
                self.ifExpr_pending() or \
                self.varDecl_pending() or \
                self.funcDef_pending() or \
                self.primary_pending() or \
                self.anonFunc_pending() or \
                self.funcCall_pending() or \
                self.primExpr_pending() or \
                self.identExpr_pending() or \
                self.whileExpr_pending()

    def parse_expr(self):
        if self.varDecl_pending():
            return self.parse_varDecl()
        elif self.ifExpr_pending():
            return self.parse_ifExpr()
        elif self.whileExpr_pending():
            return self.parse_whileExpr()
        elif self.anonFunc_pending():
            return self.parse_anonFunc()
        elif self.funcDef_pending():
            return self.parse_funcDef()
        elif self.check(Lexeme.OPAREN):
            self.match(Lexeme.OPAREN)
            expr = self.parse_expr()
            self.match(Lexeme.CPAREN)
            return expr
        elif self.identExpr_pending():
            return self.parse_identExpr()
        else:
            return self.parse_primExpr()

    def varDecl_pending(self):
        return self.check(Lexeme.LET)

    def parse_varDecl(self):
        self.match(Lexeme.LET)
        var_name = self.match(Lexeme.IDENTIFIER)

        if self.check(Lexeme.EQUAL):
            self.advance()
            val = self.parse_expr()
            return make_varDecl(var_name, val)
        else:
            return make_varDecl(var_name, None)

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
            else_clause = self.parse_else()

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
        self.match(Lexeme.LAMBDA)
        self.match(Lexeme.OPAREN)
        param_list = self.parse_optParamList()
        self.match(Lexeme.CPAREN)
        self.match(Lexeme.OBRACE)
        body = self.parse_optExprList()
        self.match(Lexeme.CBRACE)

        return make_anonFunc(param_list, body)

    def funcDef_pending(self):
        return self.check(Lexeme.DEF)

    def parse_funcDef(self):
        self.match(Lexeme.DEF)
        func_name = self.match(Lexeme.IDENTIFIER)
        self.match(Lexeme.OPAREN)
        param_list = self.parse_optParamList()
        self.match(Lexeme.CPAREN)
        self.match(Lexeme.OBRACE)
        expr_list = self.parse_optExprList()
        self.match(Lexeme.CBRACE)

        return make_funcDef(func_name, param_list, expr_list)

    def primExpr_pending(self):
        return self.primary_pending()
    
    def parse_primExpr(self):
        prim = self.parse_primary()

        if self.check_operator():
            op = self.parse_operator()
            expr = self.parse_expr()
            return make_primExpr(prim, op, expr)
        else:
            return prim

    def primary_pending(self):
        return self.check(Lexeme.NUMBER) or \
                self.check(Lexeme.STRING) or \
                (self.check(Lexeme.IDENTIFIER) and \
                 not self.check(Lexeme.EQUAL, offset=1) and \
                 not self.check(Lexeme.OPAREN, offset=1))
    
    def parse_primary(self):
        if self.check(Lexeme.NUMBER):
            return self.match(Lexeme.NUMBER)
        elif self.check(Lexeme.STRING):
            return self.match(Lexeme.STRING)
        else:
            return self.match(Lexeme.IDENTIFIER)

    def check_operator(self):
        return self.check(Lexeme.PLUS) or \
                self.check(Lexeme.MINUS) or \
                self.check(Lexeme.TIMES) or \
                self.check(Lexeme.DIVIDE) or \
                self.check(Lexeme.DOUBLE_EQUAL) or \
                self.check(Lexeme.GREATER_THAN) or \
                self.check(Lexeme.LESS_THAN)

    def parse_operator(self):
        if self.check(Lexeme.PLUS):
            return self.match(Lexeme.PLUS)
        elif self.check(Lexeme.MINUS):
            return self.match(Lexeme.MINUS)
        elif self.check(Lexeme.TIMES):
            return self.match(Lexeme.TIMES)
        elif self.check(Lexeme.DIVIDE):
            return self.match(Lexeme.DIVIDE)
        elif self.check(Lexeme.DOUBLE_EQUAL):
            return self.match(Lexeme.DOUBLE_EQUAL)
        elif self.check(Lexeme.GREATER_THAN):
            return self.match(Lexeme.GREATER_THAN)
        else:
            return self.match(Lexeme.LESS_THAN)

    def identExpr_pending(self):
        return self.check(Lexeme.IDENTIFIER) and \
                (self.check(Lexeme.EQUAL, offset=1) or \
                 self.check(Lexeme.OPAREN, offset=1))

    def parse_identExpr(self):
        identifier = self.match(Lexeme.IDENTIFIER) 
        if self.varAssign_pending():
            return self.parse_varAssign(identifier)
        else:
            return self.parse_funcCall(identifier)

    def varAssign_pending(self):
        return self.check(Lexeme.EQUAL) 

    def parse_varAssign(self, identifier):
        self.match(Lexeme.EQUAL)
        val = self.parse_expr()
        return make_varAssign(identifier, val)

    def funcCall_pending(self):
        return self.check(Lexeme.OPAREN) 

    def parse_funcCall(self, identifier):
        self.match(Lexeme.OPAREN)
        arg_list = self.parse_optArgList()
        self.match(Lexeme.CPAREN)

        anon_arg = None
        if self.optAnonArg_pending():
            anon_arg = self.parse_optAnonArg()

        return make_funcCall(identifier, arg_list, anon_arg)

    def parse_optArgList(self):
        if self.argList_pending():
            return self.parse_argList()
        else:
            return make_argList(None, None)

    def argList_pending(self):
        return self.expr_pending()

    def parse_argList(self):
        arg = self.parse_expr()
        
        sublist = None
        if self.check(Lexeme.COMMA):
            self.advance()
            sublist = self.parse_argList()

        return make_argList(arg, sublist)

    def optAnonArg_pending(self):
        return self.check(Lexeme.OBRACE)

    def parse_optAnonArg(self):
        self.match(LEXEME.OBRACE)
        expr_list = self.parse_exprList()
        self.match(LEXEME.CBRACE)
        return expr_list

def make_funcDef(func_name, param_list, expr_list):
    gen_purp = Lexeme(Lexeme.gen_purp, left=param_list, right=expr_list)
    return Lexeme(Lexeme.funcDef, left=func_name, right=gen_purp)

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

def make_anonFunc(param_list, body):
    return Lexeme(Lexeme.anonFunc, left=param_list, right=body)

def make_varAssign(var_name, value):
    return Lexeme(Lexeme.varAssign, left=var_name, right=value)
