# Author: Richard Belleville

import pytest
import uuid
import pydot
from PIL import Image
from ..lexer.lexeme import *
from ..parser.parser import *

def test_parser():
    parser = Parser(file="../lexer/examples/example2.prog")
    draw_tree(parser.parse())

def draw_tree(root_lexeme):
    def _draw_tree(lex):
        node = pydot.Node(str(uuid.uuid1()), label='"%s"' % str(lex))
        graph.add_node(node)

        if lex.left is not None:
            left = _draw_tree(lex.left)
            graph.add_edge(pydot.Edge(node, left))

        if lex.right is not None:
            right = _draw_tree(lex.right)
            graph.add_edge(pydot.Edge(node, right))

        return node

    graph = pydot.Dot(graph_type='digraph')
    _draw_tree(root_lexeme)

    file = "/tmp/proglan_graph.png"
    graph.write_png(file)
    # Image.open(file).show()

