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
                    Lexeme(Lexeme.NEWLINE, line=1, col=-1),
                    Lexeme(Lexeme.LAMBDA, line=1, col=4),
                    Lexeme(Lexeme.OPAREN, line=1, col=10),
                    Lexeme(Lexeme.IDENTIFIER, value="x", line=1, col=11),
                    Lexeme(Lexeme.CPAREN, line=1, col=12),
                    Lexeme(Lexeme.OBRACE, line=1, col=14),
                    Lexeme(Lexeme.IDENTIFIER, value="x", line=1, col=16),
                    Lexeme(Lexeme.TIMES, line=1, col=17),
                    Lexeme(Lexeme.IDENTIFIER, value="n", line=1, col=18),
                    Lexeme(Lexeme.CBRACE, line=1, col=20),
                    Lexeme(Lexeme.NEWLINE, line=2, col=-1),
                    Lexeme(Lexeme.CBRACE, line=2, col=0),
                    Lexeme(Lexeme.EOF, line=3, col=0)
               ]

    actual = Scanner(file="../../examples/example1.prog").scan()
    save_lex_stream("../../examples/example1-lexed.txt", actual)
    assert match_lexemes(actual, expected)

def test_example2():
    expected = [
                Lexeme(Lexeme.DEF, line=0, col=0),
                Lexeme(Lexeme.IDENTIFIER, value="printHello", line=0, col=4),
                Lexeme(Lexeme.OPAREN, line=0, col=14),
                Lexeme(Lexeme.CPAREN, line=0, col=15),
                Lexeme(Lexeme.OBRACE, line=0, col=17),
                Lexeme(Lexeme.NEWLINE, line=1, col=-1),
                Lexeme(Lexeme.LET, line=1, col=4),
                Lexeme(Lexeme.IDENTIFIER, value="hello", line=1, col=8),
                Lexeme(Lexeme.EQUAL, line=1, col=14),
                Lexeme(Lexeme.STRING, value="Hello", line=1, col=16),
                Lexeme(Lexeme.NEWLINE, line=2, col=-1),
                Lexeme(Lexeme.LET, line=2, col=4),
                Lexeme(Lexeme.IDENTIFIER, value="world", line=2, col=8),
                Lexeme(Lexeme.EQUAL, line=2, col=14),
                Lexeme(Lexeme.STRING, value="world", line=2, col=16),
                Lexeme(Lexeme.NEWLINE, line=3, col=-1),
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
                Lexeme(Lexeme.NEWLINE, line=5, col=-1),
                Lexeme(Lexeme.CBRACE, line=5, col=0),
                Lexeme(Lexeme.EOF, line=6, col=0)
               ]

    actual = Scanner(file="../../examples/example2.prog").scan()
    save_lex_stream("../../examples/example2-lexed.txt", actual)
    assert match_lexemes(actual, expected)

def test_example3():
    actual = Scanner(file="../../examples/example3.prog").scan()
    save_lex_stream("../../examples/example3-lexed.txt", actual)

def test_example4():
    expected = [
                Lexeme(Lexeme.LET, line=0, col=0),
                Lexeme(Lexeme.IDENTIFIER, value="v", line=0, col=4),
                Lexeme(Lexeme.EQUAL, line=0, col=6),
                Lexeme(Lexeme.NUMBER, value=0, line=0, col=8),
                Lexeme(Lexeme.AND, line=0, col=10),
                Lexeme(Lexeme.OPAREN, line=0, col=14),
                Lexeme(Lexeme.NUMBER, value=1, line=0, col=15),
                Lexeme(Lexeme.OR, line=0, col=17),
                Lexeme(Lexeme.STRING, value="0", line=0, col=20),
                Lexeme(Lexeme.CPAREN, line=0, col=23),
                Lexeme(Lexeme.XOR, line=0, col=25),
                Lexeme(Lexeme.NUMBER, value=2, line=0, col=29),
                Lexeme(Lexeme.NEWLINE, line=1, col=-1),
                Lexeme(Lexeme.IDENTIFIER, value="get_func", line=1, col=0),
                Lexeme(Lexeme.OPAREN, line=1, col=8),
                Lexeme(Lexeme.CPAREN, line=1, col=9),
                Lexeme(Lexeme.OPAREN, line=1, col=10),
                Lexeme(Lexeme.CPAREN, line=1, col=11),
                Lexeme(Lexeme.NEWLINE, line=2, col=-1),
                Lexeme(Lexeme.DEF, line=3, col=0),
                Lexeme(Lexeme.IDENTIFIER, value="return_stuff", line=3, col=4),
                Lexeme(Lexeme.OPAREN, line=3, col=16),
                Lexeme(Lexeme.CPAREN, line=3, col=17),
                Lexeme(Lexeme.OBRACE, line=3, col=19),
                Lexeme(Lexeme.NEWLINE, line=4, col=-1),
                Lexeme(Lexeme.RETURN, line=4, col=4),
                Lexeme(Lexeme.NUMBER, value=3, line=4, col=11),
                Lexeme(Lexeme.NEWLINE, line=5, col=-1),
                Lexeme(Lexeme.CBRACE, line=5, col=0),
                Lexeme(Lexeme.NEWLINE, line=6, col=-1),
                Lexeme(Lexeme.IDENTIFIER, value="v", line=7, col=0),
                Lexeme(Lexeme.EQUAL, line=7, col=2),
                Lexeme(Lexeme.NUMBER, value=0, line=7, col=4),
                Lexeme(Lexeme.BITWISE_AND, line=7, col=6),
                Lexeme(Lexeme.OPAREN, line=7, col=8),
                Lexeme(Lexeme.NUMBER, value=1, line=7, col=9),
                Lexeme(Lexeme.BITWISE_OR, line=7, col=11),
                Lexeme(Lexeme.NUMBER, value=0, line=7, col=13),
                Lexeme(Lexeme.CPAREN, line=7, col=14),
                Lexeme(Lexeme.BITWISE_XOR, line=7, col=16),
                Lexeme(Lexeme.NUMBER, value=2, line=7, col=18),
                Lexeme(Lexeme.EOF, line=8, col=0)
    ]

    actual = Scanner(file="../../examples/example4.prog").scan()
    save_lex_stream("../../examples/example4-lexed.txt", actual)
    assert match_lexemes(actual, expected)

def test_example5():
    expected = [
                Lexeme(Lexeme.IDENTIFIER, value="v", line=0, col=0),
                Lexeme(Lexeme.EQUAL, line=0, col=2),
                Lexeme(Lexeme.NUMBER, value=1, line=0, col=4),
                Lexeme(Lexeme.PLUS, line=0, col=6),
                Lexeme(Lexeme.NUMBER, value=1, line=0, col=8),
                Lexeme(Lexeme.NEWLINE, line=1, col=-1),
                Lexeme(Lexeme.IDENTIFIER, value="y", line=2, col=0),
                Lexeme(Lexeme.EQUAL, line=2, col=2),
                Lexeme(Lexeme.NUMBER, value=1, line=2, col=4),
                Lexeme(Lexeme.PLUS, line=2, col=6),
                Lexeme(Lexeme.NUMBER, value=2, line=2, col=8),
                Lexeme(Lexeme.PLUS, line=3, col=4),
                Lexeme(Lexeme.NUMBER, value=3, line=3, col=6),
                Lexeme(Lexeme.EOF, line=4, col=0)
    ]

    actual = Scanner(file="../../examples/example5.prog").scan()
    save_lex_stream("../../examples/example5-lexed.txt", actual)
    assert match_lexemes(actual, expected)

def test_example6():
    expected = [
        Lexeme(Lexeme.LET, line=0, col=0),
        Lexeme(Lexeme.IDENTIFIER, value="a", line=0, col=4),
        Lexeme(Lexeme.EQUAL, line=0, col=6),
        Lexeme(Lexeme.BOOL, value=True, line=0, col=8),
        Lexeme(Lexeme.AND, line=0, col=13),
        Lexeme(Lexeme.BOOL, value=False, line=0, col=17),
        Lexeme(Lexeme.NEWLINE, line=1, col=-1),
        Lexeme(Lexeme.IF, line=1, col=0),
        Lexeme(Lexeme.OPAREN, line=1, col=3),
        Lexeme(Lexeme.IDENTIFIER, value="a", line=1, col=4),
        Lexeme(Lexeme.NEQ, line=1, col=6),
        Lexeme(Lexeme.BOOL, value=False, line=1, col=9),
        Lexeme(Lexeme.CPAREN, line=1, col=14),
        Lexeme(Lexeme.OBRACE, line=1, col=16),
        Lexeme(Lexeme.IDENTIFIER, value="a", line=1, col=18),
        Lexeme(Lexeme.EQUAL, line=1, col=20),
        Lexeme(Lexeme.NULL, line=1, col=22),
        Lexeme(Lexeme.SEMICOLON, line=1, col=26),
        Lexeme(Lexeme.IDENTIFIER, value="print", line=1, col=28),
        Lexeme(Lexeme.OPAREN, line=1, col=33),
        Lexeme(Lexeme.STRING, value="foo", line=1, col=34),
        Lexeme(Lexeme.CPAREN, line=1, col=39),
        Lexeme(Lexeme.CBRACE, line=1, col=41),
        Lexeme(Lexeme.NEWLINE, line=2, col=-1),
        Lexeme(Lexeme.WHILE, line=3, col=3),
        Lexeme(Lexeme.OPAREN, line=3, col=6),
        Lexeme(Lexeme.IDENTIFIER, value="a", line=3, col=7),
        Lexeme(Lexeme.LEQ, line=3, col=9),
        Lexeme(Lexeme.NUMBER, value=7, line=3, col=12),
        Lexeme(Lexeme.CPAREN, line=3, col=13),
        Lexeme(Lexeme.OBRACE, line=3, col=15),
        Lexeme(Lexeme.NEWLINE, line=4, col=-1),
        Lexeme(Lexeme.IDENTIFIER, value="a", line=4, col=4),
        Lexeme(Lexeme.EQUAL, line=4, col=6),
        Lexeme(Lexeme.IDENTIFIER, value="a", line=4, col=8),
        Lexeme(Lexeme.BITWISE_AND, line=4, col=10),
        Lexeme(Lexeme.BOOL, value=True, line=4, col=12),
        Lexeme(Lexeme.NEWLINE, line=5, col=-1),
        Lexeme(Lexeme.CBRACE, line=5, col=0),
        Lexeme(Lexeme.EOF, line=6, col=0)
    ]

    actual = Scanner(file="../../examples/example6.prog").scan()
    save_lex_stream("../../examples/example6-lexed.txt", actual)
    assert match_lexemes(actual, expected)

def save_lex_stream(filename, lexemes):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    realpath = os.path.join(cur_dir, filename)
    f = open(realpath, "w")

    for lex in lexemes:
        f.write("%s\n" % str(lex))

    f.close()
