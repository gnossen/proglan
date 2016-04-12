# Author: Richard Belleville

import pytest
from ..environment.environment import *

def test_example7(capsys):
    # tests the return statement
    env = Environment(file="../../examples/example7.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "4\n2\n"

def test_example8(capsys):
    env = Environment(file="../../examples/example8.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\nHello world.\nHello world.\nHello world.\n"

def test_example12(capsys):
    env = Environment(file="../../examples/example12.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "3\n2\nnull\n"
