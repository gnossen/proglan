from ..lexer.lexeme import *

def make_tab(n):
    return "    " * n

def tab(func):
    def wrapper(pt, tab):
        tab_str = make_tab(tab)
        res = func(pt)
        lines = res.split("\n")
        tabbed = ""
        for i, line in enumerate(lines):
            tabbed += tab_str + line

            if i != len(lines) - 1:
                tabbed += "\n"

        return tabbed

    return wrapper

def pretty_print(pt):
    return _pretty_print(pt, 0)

def _pretty_print(pt, tab):
    if pt.type == Lexeme.NUMBER:
        return print_number(pt, tab)
    elif pt.type == Lexeme.STRING:
        return print_string(pt, tab)
    elif pt.type == Lexeme.IDENTIFIER:
        return print_identifier(pt, tab)
    elif pt.type == Lexeme.BOOL:
        return print_boolean(pt, tab)
    elif pt.type == Lexeme.NULL:
        return print_null(pt, tab)
    elif pt.type == Lexeme.exprList:
        return print_exprList(pt, tab)
    elif pt.type == Lexeme.funcDef:
        return print_funcDef(pt, tab)
    elif pt.type == Lexeme.funcCall:
        return print_funcCall(pt, tab)
    elif pt.type == Lexeme.function:
        return print_function(pt, tab)
    elif pt.type == Lexeme.varDecl:
        return print_varDecl(pt, tab)
    elif pt.type == Lexeme.varAssign:
        return print_varAssign(pt, tab)
    elif pt.type == Lexeme.ifExpr:
        return print_ifExpr(pt, tab)
    elif pt.type == Lexeme.whileExpr:
        return print_whileExpr(pt, tab)
    elif pt.type == Lexeme.anonFunc:
        return print_anonFunc(pt, tab)
    elif pt.type == Lexeme.primExpr:
        return print_primExpr(pt, tab)
    elif pt.type == Lexeme.arrayLiteral:
        return print_arrayLiteral(pt, tab)
    elif pt.type == Lexeme.arrayAccess:
        return print_arrayAccess(pt, tab)
    elif pt.type == Lexeme.returnExpr:
        return print_returnExpr(pt, tab)
    elif pt.type == Lexeme.attribAccess:
        return print_attribAccess(pt, tab)
    elif pt.type == Lexeme.notExpr:
        return print_notExpr(pt, tab)
    elif pt.type == Lexeme.newExpr:
        return print_newExpr(pt, tab)
    else:
        return print_unknown(pt, tab)

@tab
def print_unknown(pt):
    return str(pt)

@tab
def print_number(pt):
    return str(pt.value)

@tab
def print_string(pt):
    return "\"%s\"" % pt.value

@tab
def print_boolean(pt):
    if pt.value == True:
        return "true"
    else:
        return "false"
@tab
def print_null(pt):
    return "null"

@tab
def print_identifier(pt):
    return pt.value

def list_len(pt):
    pass

def get_func_def_part(func_name, param_list):
    return "def %s(%s)" % (print_identifier(func_name, 0), print_comma_list(param_list, 0))

def get_anon_def_part(param_list):
    return "def(%s)" % print_comma_list(param_list, 0)

def list_len(l):
    if l is None:
        return 0
    else:
        return 1 + list_len(l.right)

def get_body(body):
    length = list_len(body)
    if length == 0:
        return " { }"
    else:
        return " {\n%s\n}" % (print_exprList(body, 1))

def get_func_param_part(func_param):
    if func_param is None:
        return ""
    else:
        name = func_param.left
        params = func_param.right

        if params is not None:
            return "(%s: %s)" % (print_identifier(name, 0), print_comma_list(params, 0))
        else:
            return "(%s)" % print_identifier(name, 0)

@tab
def print_funcDef(pt):
    func_name = pt.left
    param_list = pt.right.left
    func_param = pt.right.right.left
    body = pt.right.right.right

    def_part = get_func_def_part(func_name, param_list)
    func_param_part = get_func_param_part(func_param)
    body_part =  get_body(body)

    return "%s%s%s" % (def_part, func_param_part, body_part)

@tab
def print_anonFunc(pt):
    param_list = pt.left
    func_param = pt.right.left
    body = pt.right.right

    def_part = get_anon_def_part(param_list)
    func_param_part = get_func_param_part(func_param)
    body_part = get_body(body)

    return "%s%s%s" % (def_part, func_param_part, body_part)

@tab
def print_function(pt):
    param_list = pt.left
    func_param = pt.right.left
    body = pt.right.right.left

    def_part = get_anon_def_part(param_list)
    func_param_part = get_func_param_part(func_param)
    body_part = get_body(body)

    return "%s%s%s" % (def_part, func_param_part, body_part)

@tab
def print_comma_list(pt):
    if pt is None:
        return ""
    else:
        cur_elem = _pretty_print(pt.left, 0)
        if pt.right is None:
            return cur_elem
        else:
            return "%s, %s" % (cur_elem, print_comma_list(pt.right, 0))

@tab
def print_exprList(pt):
    if pt is None or pt.left is None:
        return ""
    else:
        cur_elem = _pretty_print(pt.left, 0)
        if pt.right is None:
            return cur_elem
        else:
            return "%s\n%s" % (cur_elem, print_exprList(pt.right, 0))

@tab
def print_funcCall(pt):
    func_name = pt.left
    arg_list = pt.right.left
    func_arg = pt.right.right

    main_part = "%s(%s)" % (_pretty_print(func_name, 0), print_comma_list(arg_list, 0))
    if func_arg is None:
        return main_part
    else:
        return "%s%s" % (main_part, get_body(func_arg))

@tab
def print_varDecl(pt):
    var_name = pt.left
    value = pt.right
    
    return "let %s = %s" % (print_identifier(var_name, 0), _pretty_print(value, 0))

@tab
def print_varAssign(pt):
    var_name = pt.left
    value = pt.right
    
    return "%s = %s" % (_pretty_print(var_name, 0), _pretty_print(value, 0))

@tab
def print_ifExpr(pt):
    cond = pt.left
    body = pt.right.left
    else_expr = pt.right.right
    else_space = " "
    if list_len(body) <= 1:
        else_space = "\n"

    return "if (%s)%s%s%s" % (_pretty_print(cond, 0), get_body(body), else_space, print_elseExpr(else_expr, 0))

@tab
def print_elseExpr(pt):
    if pt is None:
        return ""

    body = pt.left
    ifExpr = pt.right

    if body is None:
        return "else %s" % print_ifExpr(ifExpr, 0)
    else:
        return "else %s" % get_body(body)

@tab
def print_whileExpr(pt):
    cond = pt.left
    body = pt.right

    return "while (%s)%s" % (_pretty_print(cond, 0), get_body(body))

def get_operator(op):
    if op.type == Lexeme.PLUS:
        return "+"
    elif op.type == Lexeme.MINUS:
        return "-"
    elif op.type == Lexeme.TIMES:
        return "*"
    elif op.type == Lexeme.DIVIDE:
        return "/"
    elif op.type == Lexeme.DOUBLE_EQUAL:
        return "=="
    elif op.type == Lexeme.GREATER_THAN:
        return ">"
    elif op.type == Lexeme.LESS_THAN:
        return "<"
    elif op.type == Lexeme.AND:
        return "and"
    elif op.type == Lexeme.OR:
        return "or"
    elif op.type == Lexeme.XOR:
        return "xor"
    elif op.type == Lexeme.BITWISE_AND:
        return "&"
    elif op.type == Lexeme.BITWISE_OR:
        return "|"
    elif op.type == Lexeme.BITWISE_XOR:
        return "^"
    elif op.type == Lexeme.LEQ:
        return "<="
    elif op.type == Lexeme.GEQ:
        return ">="
    elif op.type == Lexeme.NEQ:
        return "!="
    elif op.type == Lexeme.TRIPLE_EQ:
        return "==="
    elif op.type == Lexeme.NOT_TRIPLE_EQ:
        return "!=="
    else:
        return "?"

@tab
def print_primExpr(pt):
    left = pt.left
    op = pt.right.left
    expr = pt.right.right

    return "%s %s %s" % (_pretty_print(left, 0), get_operator(op), _pretty_print(expr, 0))

@tab
def print_arrayLiteral(pt):
    members = pt.left
    return "[%s]" % print_comma_list(members, 0)

@tab
def print_arrayAccess(pt):
    array_expr = pt.left 
    index = pt.right

    return "%s[%s]" % (_pretty_print(array_expr, 0), _pretty_print(index, 0))

@tab
def print_returnExpr(pt):
    expr = pt.left

    return "return %s" % _pretty_print(expr, 0)

@tab
def print_attribAccess(pt):
    obj = pt.left
    attrib = pt.right

    return "%s.%s" % (_pretty_print(obj, 0), print_identifier(attrib, 0))

@tab
def print_notExpr(pt):
    expr = pt.left

    return "not %s" % _pretty_print(expr, 0)

@tab
def print_newExpr(pt):
    expr = pt.left

    return "new %s" % _pretty_print(expr, 0)
