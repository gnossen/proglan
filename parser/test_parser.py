# Author: Richard Belleville

import pytest
import uuid
import pydot
import os
from ..lexer.lexeme import *
from ..parser.parser import *

def test_parser1():
    parser = Parser(file="../examples/example1.prog")
    draw_tree(parser.parse(), get_filepath("../examples/proglan-ast1.png"))

def test_parser2():
    parser = Parser(file="../examples/example2.prog")
    draw_tree(parser.parse(), get_filepath("../examples/proglan-ast2.png"))

def test_parser3():
    parser = Parser(file="../examples/example3.prog")
    draw_tree(parser.parse(), get_filepath("../examples/proglan-ast3.png"))

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

