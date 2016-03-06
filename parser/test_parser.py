# Author: Richard Belleville

import pytest
from ..lexer.lexeme import *
import pydot
from PIL import Image

def test_trees():
    graph = pydot.Dot(graph_type='graph')
    A = pydot.Node("Root")
    B = pydot.Node("Subject")
    C = pydot.Node("Verb Phrase")
    graph.add_node(A)
    graph.add_node(B)
    graph.add_node(C)
    graph.add_edge(pydot.Edge(A, B))
    graph.add_edge(pydot.Edge(A, C))

    file = "/tmp/proglan_graph.png"
    graph.write_png(file)
    Image.open(file).show()
