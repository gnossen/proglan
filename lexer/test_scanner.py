#Author: Richard Belleville

import pytest
from lexeme import *
from scanner import *
import os

def test_example1():
    expected = [
                    Lexeme(Lexeme.DEF, line=0, col=0),
                    Lexeme(Lexeme.IDENTIFIER, value="multn", line=0, col=4),
                    Lexeme(Lexeme.OPAREN, line=0, col=9),
                    Lexeme(Lexeme.IDENTIFIER, value="n", line=0, col=10),
                    Lexeme(Lexeme.CPAREN, line=0, col=11),
                    Lexeme(Lexeme.OBRACE, line=0, col=13),
                    Lexeme(Lexeme.LAMBDA, line=1, col=4),
                    Lexeme(Lexeme.OPAREN, line=1, col=10),
                    Lexeme(Lexeme.IDENTIFIER, value="x", line=1, col=11),
                    Lexeme(Lexeme.CPAREN, line=1, col=12),
                    Lexeme(Lexeme.OBRACE, line=1, col=14),
                    Lexeme(Lexeme.IDENTIFIER, value="x", line=1, col=16),
                    Lexeme(Lexeme.TIMES, line=1, col=17),
                    Lexeme(Lexeme.IDENTIFIER, value="n", line=1, col=18),
                    Lexeme(Lexeme.CBRACE, line=1, col=20),
                    Lexeme(Lexeme.CBRACE, line=2, col=0),
                    Lexeme(Lexeme.EOF, line=3, col=0)
               ]

    actual = Scanner(file="examples/example1.prog").scan()
    assert match_lexemes(actual, expected)

def test_example2():
    expected = [
                Lexeme(Lexeme.DEF, line=0, col=0),
                Lexeme(Lexeme.IDENTIFIER, value="printHello", line=0, col=4),
                Lexeme(Lexeme.OPAREN, line=0, col=14),
                Lexeme(Lexeme.CPAREN, line=0, col=15),
                Lexeme(Lexeme.OBRACE, line=0, col=17),
                Lexeme(Lexeme.LET, line=1, col=4),
                Lexeme(Lexeme.IDENTIFIER, value="hello", line=1, col=8),
                Lexeme(Lexeme.EQUAL, line=1, col=14),
                Lexeme(Lexeme.STRING, value="Hello", line=1, col=16),
                Lexeme(Lexeme.LET, line=2, col=4),
                Lexeme(Lexeme.IDENTIFIER, value="world", line=2, col=8),
                Lexeme(Lexeme.EQUAL, line=2, col=14),
                Lexeme(Lexeme.STRING, value="world", line=2, col=16),
                Lexeme(Lexeme.IDENTIFIER, value="print", line=4, col=4),
                Lexeme(Lexeme.OPAREN, line=4, col=9),
                Lexeme(Lexeme.IDENTIFIER, value="hello", line=4, col=10),
                Lexeme(Lexeme.PLUS, line=4, col=16),
                Lexeme(Lexeme.STRING, value=" ", line=4, col=18),
                Lexeme(Lexeme.PLUS, line=4, col=22),
                Lexeme(Lexeme.IDENTIFIER, value="world", line=4, col=24),
                Lexeme(Lexeme.PLUS, line=4, col=30),
                Lexeme(Lexeme.STRING, value="!", line=4, col=32),
                Lexeme(Lexeme.CPAREN, line=4, col=35),
                Lexeme(Lexeme.CBRACE, line=5, col=0),
                Lexeme(Lexeme.EOF, line=6, col=0)
               ]

    actual = Scanner(file="examples/example2.prog").scan()
    assert match_lexemes(actual, expected)
