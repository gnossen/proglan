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

def test_example14(capsys):
    env = Environment(file="../../examples/example14.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "Rover\nBark!\nSpot\n"

def test_example15(capsys):
    env = Environment(file="../../examples/example15.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "3\n0\n"

def test_example17(capsys):
    env = Environment(file="../../examples/example17.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "0\n1\n2\n3\n4\n2\n3\n"


def test_example18(capsys):
    env = Environment(file="../../examples/example18.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "Meow!\nGarfield\nSeymour\n"

def test_wires(capsys):
    env = Environment(file="../../examples/wire-test.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "1 + 1 = 10\n1 + 0 = 01\n0 + 1 = 01\n0 + 0 = 00\n"


def test_dictionary(capsys):
    env = Environment(file="../../examples/dictionary-test.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "Two is: 2\nFour is: 4\nSeven is: 7\n"

def test_example22(capsys):
    env = Environment(file="../../examples/example22.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "3\n5\n2\n"
