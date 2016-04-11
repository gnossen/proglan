# Author: Richard Belleville

import pytest
import uuid
import pydot
import os
from ..lexer.lexeme import *
from ..parser.parser import *

def test_example1():
    n2 = Lexeme(Lexeme.IDENTIFIER, value="n")
    times = Lexeme(Lexeme.TIMES)
    gen_purp2 = Lexeme(Lexeme.gen_purp, left=times, right=n2)
    x2 = Lexeme(Lexeme.IDENTIFIER, value="x")
    prim_expr1 = Lexeme(Lexeme.primExpr, left=x2, right=gen_purp2)
    anon_expr_list = Lexeme(Lexeme.exprList, left=prim_expr1)
    x = Lexeme(Lexeme.IDENTIFIER, value="x")
    anon_param = Lexeme(Lexeme.paramList, left=x)
    func_gen_purp2 = Lexeme(Lexeme.gen_purp, right=anon_expr_list)
    anon_func = Lexeme(Lexeme.anonFunc, left=anon_param, right=func_gen_purp2)
    func1_expr_list = Lexeme(Lexeme.exprList, left=anon_func)
    func_gen_purp =  Lexeme(Lexeme.gen_purp, right=func1_expr_list)
    n = Lexeme(Lexeme.IDENTIFIER, value="n")
    param_n = Lexeme(Lexeme.paramList, left=n)
    gen_purp1 = Lexeme(Lexeme.gen_purp, left=param_n, right=func_gen_purp)
    multn = Lexeme(Lexeme.IDENTIFIER, value="multn")
    func_def = Lexeme(Lexeme.funcDef, left=multn, right=gen_purp1)
    expected = Lexeme(Lexeme.exprList, left=func_def)

    parser = Parser(file="../../examples/example1.prog")

    ast = parser.parse()
    draw_tree(ast, get_filepath("../../examples/proglan-ast1.png"))
    draw_tree(expected, get_filepath("../../examples/expected-ast1.png"))
    assert lex_tree_equal(expected, ast)

def test_example2():
    startled_str = Lexeme(Lexeme.STRING, value="!")
    plus3 = Lexeme(Lexeme.PLUS)
    gen_purp5 = Lexeme(Lexeme.gen_purp, left=plus3, right=startled_str)
    world2 = Lexeme(Lexeme.IDENTIFIER, value="world")
    prim_expr3 = Lexeme(Lexeme.primExpr, left=world2, right=gen_purp5)
    plus2 = Lexeme(Lexeme.PLUS)
    gen_purp4 = Lexeme(Lexeme.gen_purp, left=plus2, right=prim_expr3)
    space_str = Lexeme(Lexeme.STRING, value=" ")
    prim_expr2 = Lexeme(Lexeme.primExpr, left=space_str, right=gen_purp4)
    plus1 = Lexeme(Lexeme.PLUS)
    gen_purp3 = Lexeme(Lexeme.gen_purp, left=plus1, right=prim_expr2)
    hello2 = Lexeme(Lexeme.IDENTIFIER, value="hello")
    prim_expr1 = Lexeme(Lexeme.primExpr, left=hello2, right=gen_purp3)
    arg_list1 = Lexeme(Lexeme.argList, left=prim_expr1)
    gen_purp2 = Lexeme(Lexeme.gen_purp, left=arg_list1)
    print1 = Lexeme(Lexeme.IDENTIFIER, value="print")
    func_call = Lexeme(Lexeme.funcCall, left=print1, right=gen_purp2)
    expr_list3 = Lexeme(Lexeme.exprList, left=func_call)
    world_str1 = Lexeme(Lexeme.STRING, value="world")
    world1 = Lexeme(Lexeme.IDENTIFIER, value="world")
    var_decl2 = Lexeme(Lexeme.varDecl, left=world1, right=world_str1)
    expr_list2 = Lexeme(Lexeme.exprList, left=var_decl2, right=expr_list3)
    hello_str1 = Lexeme(Lexeme.STRING, value="Hello")
    hello1 = Lexeme(Lexeme.IDENTIFIER, value="hello")
    var_decl1 = Lexeme(Lexeme.varDecl, left=hello1, right=hello_str1)
    expr_list1 = Lexeme(Lexeme.exprList, left=var_decl1, right=expr_list2)
    gen_purp1 = Lexeme(Lexeme.gen_purp, right=expr_list1)
    print_hello = Lexeme(Lexeme.IDENTIFIER, value="printHello")
    func_gen_purp = Lexeme(Lexeme.gen_purp, right=gen_purp1)
    func_def = Lexeme(Lexeme.funcDef, left=print_hello, right=func_gen_purp)
    expected = Lexeme(Lexeme.exprList, left=func_def) 

    parser = Parser(file="../../examples/example2.prog")
    ast = parser.parse()
    draw_tree(ast, get_filepath("../../examples/proglan-ast2.png"))
    assert lex_tree_equal(expected, ast)

def test_example3():
    gen_purp7 = Lexeme(Lexeme.gen_purp)
    fib2 = Lexeme(Lexeme.IDENTIFIER, value="fib")
    func_call4 = Lexeme(Lexeme.funcCall, left=fib2, right=gen_purp7)
    expr_list1 = Lexeme(Lexeme.exprList, left=func_call4)
    one1 = Lexeme(Lexeme.NUMBER, value=1)
    arg_list5 = Lexeme(Lexeme.argList, left=one1)
    zero1 = Lexeme(Lexeme.NUMBER, value=0)
    arg_list4 = Lexeme(Lexeme.argList, left=zero1, right=arg_list5)
    gen_purp6 = Lexeme(Lexeme.gen_purp, left=arg_list4)
    next_fib3 = Lexeme(Lexeme.IDENTIFIER, value="next_fib")
    func_call3 = Lexeme(Lexeme.funcCall, left=next_fib3, right=gen_purp6)
    expr_list7 = Lexeme(Lexeme.exprList, left=func_call3)
    func_gen_purp4 = Lexeme(Lexeme.gen_purp, right=expr_list7)
    anon_func2 = Lexeme(Lexeme.anonFunc, right=func_gen_purp4)
    expr_list3 = Lexeme(Lexeme.exprList, left=anon_func2)
    cur4 = Lexeme(Lexeme.IDENTIFIER, value="cur")
    plus1 = Lexeme(Lexeme.PLUS)
    gen_purp5 = Lexeme(Lexeme.gen_purp, left=plus1, right=cur4)
    prev2 = Lexeme(Lexeme.IDENTIFIER, value="prev")
    prim_expr1 = Lexeme(Lexeme.primExpr, left=prev2, right=gen_purp5)
    arg_list3 = Lexeme(Lexeme.argList, left=prim_expr1)
    cur3 = Lexeme(Lexeme.IDENTIFIER, value="cur")
    arg_list2 = Lexeme(Lexeme.argList, left=cur3, right=arg_list3)
    gen_purp4 = Lexeme(Lexeme.gen_purp, left=arg_list2)
    next_fib2 = Lexeme(Lexeme.IDENTIFIER, value="next_fib")
    func_call2 = Lexeme(Lexeme.funcCall, left=next_fib2, right=gen_purp4)
    expr_list6 = Lexeme(Lexeme.exprList, left=func_call2)
    func_gen_purp3 = Lexeme(Lexeme.gen_purp, right=expr_list6)
    anon_func1 = Lexeme(Lexeme.anonFunc, right=func_gen_purp3)
    expr_list5 = Lexeme(Lexeme.exprList, left=anon_func1)
    cur2 = Lexeme(Lexeme.IDENTIFIER, value="cur")
    arg_list1 = Lexeme(Lexeme.argList, left=cur2)
    gen_purp3 = Lexeme(Lexeme.gen_purp, left=arg_list1)
    print1 = Lexeme(Lexeme.IDENTIFIER, value="print")
    func_call1 = Lexeme(Lexeme.funcCall, left=print1, right=gen_purp3)
    expr_list4 = Lexeme(Lexeme.exprList, left=func_call1, right=expr_list5)
    cur1 = Lexeme(Lexeme.IDENTIFIER, value="cur")
    param_list3 = Lexeme(Lexeme.paramList, left=cur1)
    prev1 = Lexeme(Lexeme.IDENTIFIER, value="prev")
    param_list2 = Lexeme(Lexeme.paramList, left=prev1, right=param_list3)
    gen_purp2 = Lexeme(Lexeme.gen_purp, right=expr_list4)
    next_fib = Lexeme(Lexeme.IDENTIFIER, value="next_fib")
    func_gen_purp2 = Lexeme(Lexeme.gen_purp, left=param_list2, right=gen_purp2)
    func_def2 = Lexeme(Lexeme.funcDef, left=next_fib, right=func_gen_purp2)
    expr_list2 = Lexeme(Lexeme.exprList, left=func_def2, right=expr_list3)
    gen_purp1 = Lexeme(Lexeme.gen_purp, right=expr_list2)
    fib1 = Lexeme(Lexeme.IDENTIFIER, value="fib")
    func_gen_purp = Lexeme(Lexeme.gen_purp, right=gen_purp1)
    func_def = Lexeme(Lexeme.funcDef, left=fib1, right=func_gen_purp)
    expected = Lexeme(Lexeme.exprList, left=func_def, right=expr_list1)

    parser = Parser(file="../../examples/example3.prog")

    ast = parser.parse()
    draw_tree(ast, get_filepath("../../examples/proglan-ast3.png"))
    draw_tree(expected, get_filepath("../../examples/expected-ast3.png"))
    assert lex_tree_equal(expected, ast)

def test_example6():
    parser = Parser(file="../../examples/example6.prog")
    ast = parser.parse()
    draw_tree(ast, get_filepath("../../examples/proglan-ast6.png"))

def test_example8():
    parser = Parser(file="../../examples/example8.prog")
    ast = parser.parse()
    draw_tree(ast, get_filepath("../../examples/proglan-ast8.png"))

def get_cur_dir():
    return os.path.dirname(os.path.realpath(__file__))

def get_filepath(filename):
    return os.path.join(get_cur_dir(), filename)

def draw_tree(root_lexeme, filename):
    def _draw_tree(lex):
        node = pydot.Node(str(uuid.uuid1()), label='"%s"' % str(lex))
        graph.add_node(node)

        if not(lex.left is None and lex.right is None):
            if lex.left is not None:
                left = _draw_tree(lex.left)
            else:
                left = pydot.Node(str(uuid.uuid1()), label='NULL')
                graph.add_node(left)
            
            graph.add_edge(pydot.Edge(node, left))

            if lex.right is not None:
                right = _draw_tree(lex.right)
            else:
                right = pydot.Node(str(uuid.uuid1()), label='NULL')
                graph.add_node(right)

            graph.add_edge(pydot.Edge(node, right))

        return node

    graph = pydot.Dot(graph_type='digraph')
    _draw_tree(root_lexeme)
    graph.write_png(filename)


def lex_tree_equal(a, b):
    if a is None and b is None:
        return True

    if a is None or b is None:
        raise Exception("a: %s, b: %s" % (str(a), str(b)))

    if a != b:
        raise Exception(str(a) + " != " + str(b))

    return lex_tree_equal(a.left, b.left) and \
            lex_tree_equal(a.right, b.right)

