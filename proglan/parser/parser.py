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

    def expr_pending(self):
        return self.primary_pending() or \
                self.ifExpr_pending() or \
                self.whileExpr_pending() or \
                self.varDecl_pending() or \
                self.anonFunc_pending() or \
                self.funcDef_pending() or \
                self.arrayLiteral_pending() or \
                self.check(Lexeme.OPAREN) or \
                self.check(Lexeme.RETURN) or \
                self.check(Lexeme.NOT)

    def parse_expr(self):
        if self.primary_pending():
            prim = self.parse_primary()
            return self.parse_metaExpr(prim)
        if self.check(Lexeme.DEF):
            self.match(Lexeme.DEF)
            if self.check(Lexeme.OPAREN):
                return self.parse_metaExpr(self.parse_anonFunc())
            else:
                return self.parse_metaExpr(self.parse_funcDef())
        elif self.ifExpr_pending():
            ifExpr = self.parse_ifExpr()
            return self.parse_metaExpr(ifExpr)
        elif self.whileExpr_pending():
            whileExpr = self.parse_whileExpr()
            return self.parse_metaExpr(whileExpr)
        elif self.varDecl_pending():
            varDecl = self.parse_varDecl()
            return self.parse_metaExpr(varDecl)
        elif self.arrayLiteral_pending():
            arrayLiteral = self.parse_arrayLiteral()
            return self.parse_metaExpr(arrayLiteral)
        elif self.check(Lexeme.RETURN):
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
            self.match(Lexeme.OPAREN)
            expr = self.parse_expr()
            self.match(Lexeme.CPAREN)
            return self.parse_metaExpr(expr)

    def parse_metaExpr(self, expr):
        if self.check(Lexeme.EQUAL):
            self.match(Lexeme.EQUAL)
            new_val = self.parse_expr()
            return make_varAssign(expr, new_val)
        elif self.check(Lexeme.DOT, skip=False):
            self.match(Lexeme.DOT)
            attr = self.match(Lexeme.IDENTIFIER)
            return self.parse_metaExpr(make_attribAccess(expr, attr))
        elif self.check(Lexeme.OPAREN, skip=False):
            self.match(Lexeme.OPAREN)
            args = self.parse_optArgList()
            self.match(Lexeme.CPAREN)
            
            anon_arg = None
            if self.check(Lexeme.OBRACE):
                self.match(Lexeme.OBRACE)
                anon_arg = self.parse_optExprList()
                self.match(Lexeme.CBRACE)

            return self.parse_metaExpr(make_funcCall(expr, args, anon_arg))
        elif self.check(Lexeme.OSQBRACE, skip=False):
            self.match(Lexeme.OSQBRACE)
            index_expr = self.parse_expr()
            self.match(Lexeme.CSQBRACE)
            return self.parse_metaExpr(make_arrayAccess(expr, index_expr))
        elif self.operator_pending():
            operator = self.parse_operator()
            right_expr = self.parse_expr()
            return make_primExpr(expr, operator, right_expr)
        else:
            return expr

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

    def operator_pending(self):
        return self.check(Lexeme.PLUS) or \
                self.check(Lexeme.MINUS) or \
                self.check(Lexeme.TIMES) or \
                self.check(Lexeme.DIVIDE) or \
                self.check(Lexeme.DOUBLE_EQUAL) or \
                self.check(Lexeme.GREATER_THAN) or \
                self.check(Lexeme.LESS_THAN) or \
                self.check(Lexeme.AND) or \
                self.check(Lexeme.OR) or \
                self.check(Lexeme.XOR) or \
                self.check(Lexeme.BITWISE_AND) or \
                self.check(Lexeme.BITWISE_OR) or \
                self.check(Lexeme.BITWISE_XOR) or \
                self.check(Lexeme.LEQ) or \
                self.check(Lexeme.GEQ) or \
                self.check(Lexeme.NEQ) or \
                self.check(Lexeme.TRIPLE_EQ) or \
                self.check(Lexeme.NOT_TRIPLE_EQ)

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
        elif self.check(Lexeme.LESS_THAN):
            return self.match(Lexeme.LESS_THAN)
        elif self.check(Lexeme.AND):
            return self.match(Lexeme.AND)
        elif self.check(Lexeme.OR):
            return self.match(Lexeme.OR)
        elif self.check(Lexeme.XOR):
            return self.match(Lexeme.XOR)
        elif self.check(Lexeme.BITWISE_AND):
            return self.match(Lexeme.BITWISE_AND)
        elif self.check(Lexeme.BITWISE_OR):
            return self.match(Lexeme.BITWISE_OR)
        elif self.check(Lexeme.BITWISE_XOR):
            return self.match(Lexeme.BITWISE_XOR)
        elif self.check(Lexeme.LEQ):
            return self.match(Lexeme.LEQ)
        elif self.check(Lexeme.GEQ):
            return self.match(Lexeme.GEQ)
        elif self.check(Lexeme.NEQ):
            return self.match(Lexeme.NEQ)
        elif self.check(Lexeme.TRIPLE_EQ):
            return self.match(Lexeme.TRIPLE_EQ)
        else:
            return self.match(Lexeme.NOT_TRIPLE_EQ)

    def parse_varAssign(self, identifier):
        self.match(Lexeme.EQUAL)
        val = self.parse_expr()
        return make_varAssign(identifier, val)

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
