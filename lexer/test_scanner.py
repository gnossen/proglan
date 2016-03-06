#Author: Richard Belleville

import pytest
from lexeme import *
from scanner import *
import os

def test_example1():
    expected = [
                    Lexeme(Lexeme.DEF),
                    Lexeme(Lexeme.IDENTIFIER, value="multn"),
                    Lexeme(Lexeme.OPAREN),
                    Lexeme(Lexeme.IDENTIFIER, value="n"),
                    Lexeme(Lexeme.CPAREN),
                    Lexeme(Lexeme.OBRACE),
                    Lexeme(Lexeme.LAMBDA),
                    Lexeme(Lexeme.OPAREN),
                    Lexeme(Lexeme.IDENTIFIER, value="x"),
                    Lexeme(Lexeme.CPAREN),
                    Lexeme(Lexeme.OBRACE),
                    Lexeme(Lexeme.IDENTIFIER, value="x"),
                    Lexeme(Lexeme.TIMES),
                    Lexeme(Lexeme.IDENTIFIER, value="n"),
                    Lexeme(Lexeme.CBRACE),
                    Lexeme(Lexeme.CBRACE),
                    Lexeme(Lexeme.EOF)
               ]

    actual = Scanner(file="examples/example1.prog").scan()
    assert match_lexemes(actual, expected)
