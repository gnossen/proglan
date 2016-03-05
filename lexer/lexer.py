# Author: Richard Belleville

from lexeme import *

class Lexer:

    def __init__(self, input):
        self.input = input
        self.word_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        self.word_start_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

    def peek(self):
        try:
            return self.input[0]
        except:
            return None

    def read(self):
        val = self.peek()
        self.advance()
        return val

    def advance(self):
        if len(self.input) != 0:
            self.input = self.input[1:]

    def lex(self):
        self.skip_whitespace()

        ch = self.read()
        if ch == None:
            return Lexeme(Lexeme.EOF)
        elif ch == "(":
            return Lexeme(Lexeme.OPAREN)
        elif ch == ")":
            return Lexeme(Lexeme.CPAREN)
        elif ch == "{":
            return Lexeme(Lexeme.OBRACE)
        elif ch == "}":
            return Lexeme(Lexeme.CBRACE)
        elif ch == ",":
            return Lexeme(Lexeme.COMMA)
        elif ch == "+":
            return Lexeme(Lexeme.PLUS)
        elif ch == "-":
            return Lexeme(Lexeme.MINUS)
        elif ch == "*":
            return Lexeme(Lexeme.TIMES)
        elif ch == "/":
            return Lexeme(Lexeme.DIVIDE)
        elif ch == ">":
            return Lexeme(Lexeme.GREATER_THAN)
        elif ch == "<":
            return Lexeme(Lexeme.LESS_THAN)
        elif ch == "=":
            return self.lex_equal()
        elif ch in self.word_start_chars:
            word = self.lex_word(ch)
            if word == "def":
                return Lexeme(Lexeme.DEF)
            elif word == "let":
                return Lexeme(Lexeme.LET)
            elif word == "if":
                return Lexeme(Lexeme.IF)
            elif word == "else":
                return Lexeme(Lexeme.ELSE)
            elif word == "lambda":
                return Lexeme(Lexeme.LAMBDA)
            else: 
                return Lexeme(Lexeme.IDENTIFIER, value=word)
        
    def skip_whitespace(self):
        char = self.peek()
        while char is not None and char.isspace():
            self.advance()
            char = self.peek()

    def lex_equal(self):
        if self.peek() == "=":
            self.advance()
            return Lexeme(Lexeme.DOUBLE_EQUAL)
        else:
            return Lexeme(Lexeme.EQUAL)

    def lex_word(self, head):
        ch = self.peek()
        if ch in self.word_chars:
            self.advance()
            return self.lex_word(head + ch)
        else:
            return head
