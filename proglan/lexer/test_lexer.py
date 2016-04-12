#Author: Richard Belleville

import pytest
from lexeme import *
from lexer import *

def test_basic_lexemes():
    lex = Lexer("(")
    assert lex.lex().is_type(Lexeme.OPAREN)

    lex = Lexer(")")
    assert lex.lex().is_type(Lexeme.CPAREN)

    lex = Lexer("{")
    assert lex.lex().is_type(Lexeme.OBRACE)

    lex = Lexer("}")
    assert lex.lex().is_type(Lexeme.CBRACE)

    lex = Lexer(",")
    assert lex.lex().is_type(Lexeme.COMMA)

    lex = Lexer("+")
    assert lex.lex().is_type(Lexeme.PLUS)

    lex = Lexer("-")
    assert lex.lex().is_type(Lexeme.MINUS)

    lex = Lexer("*")
    assert lex.lex().is_type(Lexeme.TIMES)

    lex = Lexer("/")
    assert lex.lex().is_type(Lexeme.DIVIDE)

    lex = Lexer(">")
    assert lex.lex().is_type(Lexeme.GREATER_THAN)

    lex = Lexer("<")
    assert lex.lex().is_type(Lexeme.LESS_THAN)

    lex = Lexer("<")
    assert lex.lex().is_type(Lexeme.LESS_THAN)

    lex = Lexer("=")
    assert lex.lex().is_type(Lexeme.EQUAL)

    lex = Lexer("==")
    assert lex.lex().is_type(Lexeme.DOUBLE_EQUAL)

def test_word_lexemes():
    lex = Lexer("def")
    assert lex.lex().is_type(Lexeme.DEF)

    lex = Lexer("let")
    assert lex.lex().is_type(Lexeme.LET)

    lex = Lexer("if")
    assert lex.lex().is_type(Lexeme.IF)

    lex = Lexer("else")
    assert lex.lex().is_type(Lexeme.ELSE)

    lex = Lexer("lambda")
    assert lex.lex().is_type(Lexeme.LAMBDA)

def test_identifiers():
    lex = Lexer("abcd123")
    assert lex.lex() == Lexeme(Lexeme.IDENTIFIER, value="abcd123")

    lex = Lexer("abcd_123")
    assert lex.lex() == Lexeme(Lexeme.IDENTIFIER, value="abcd_123")

    with pytest.raises(Exception):
        Lexer("~asdf").lex()

def test_numbers():
    lex = Lexer("12345")
    assert lex.lex() == Lexeme(Lexeme.NUMBER, value=12345)

def test_string():
    lex = Lexer("\"Hello world!\"")
    assert lex.lex() == Lexeme(Lexeme.STRING, value="Hello world!")
