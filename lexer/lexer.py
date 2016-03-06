# Author: Richard Belleville

from lexeme import *

class Lexer:

    def __init__(self, input):
        self.input = input
        self.line = 0
        self.col = 0
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
            if self.input[0] == '\n':
                self.line += 1
                self.col = 0
            else:
                self.col += 1

            self.input = self.input[1:]

    def lex(self):
        self.skip_whitespace()

        ch = self.read()
        if ch == None:
            return Lexeme(Lexeme.EOF, line=self.line, col=self.col)
        elif ch == "(":
            return Lexeme(Lexeme.OPAREN, line=self.line, col=self.col - 1)
        elif ch == ")":
            return Lexeme(Lexeme.CPAREN, line=self.line, col=self.col - 1)
        elif ch == "{":
            return Lexeme(Lexeme.OBRACE, line=self.line, col=self.col - 1)
        elif ch == "}":
            return Lexeme(Lexeme.CBRACE, line=self.line, col=self.col - 1)
        elif ch == ",":
            return Lexeme(Lexeme.COMMA, line=self.line, col=self.col - 1)
        elif ch == "+":
            return Lexeme(Lexeme.PLUS, line=self.line, col=self.col - 1)
        elif ch == "-":
            return Lexeme(Lexeme.MINUS, line=self.line, col=self.col - 1)
        elif ch == "*":
            return Lexeme(Lexeme.TIMES, line=self.line, col=self.col - 1)
        elif ch == "/":
            return Lexeme(Lexeme.DIVIDE, line=self.line, col=self.col - 1)
        elif ch == ">":
            return Lexeme(Lexeme.GREATER_THAN, line=self.line, col=self.col - 1)
        elif ch == "<":
            return Lexeme(Lexeme.LESS_THAN, line=self.line, col=self.col - 1)
        elif ch == "=":
            return self.lex_equal()
        elif ch in self.word_start_chars:
            word = self.lex_word(ch)
            if word == "def":
                return Lexeme(Lexeme.DEF, line=self.line, col=self.col - 3)
            elif word == "let":
                return Lexeme(Lexeme.LET, line=self.line, col=self.col - 3)
            elif word == "if":
                return Lexeme(Lexeme.IF, line=self.line, col=self.col - 2)
            elif word == "else":
                return Lexeme(Lexeme.ELSE, line=self.line, col=self.col - 4)
            elif word == "lambda":
                return Lexeme(Lexeme.LAMBDA, line=self.line, col=self.col - 6)
            else: 
                return Lexeme(Lexeme.IDENTIFIER, value=word, line=self.line, col=self.col - len(word))
        elif ch.isdigit():
            number = self.lex_number(ch)
            return Lexeme(Lexeme.NUMBER, value=int(number), line=self.line, col=self.col - len(number))
        else:
            raise Exception("Illegal character '%s'." % ch)
        
    def skip_whitespace(self):
        char = self.peek()
        while char is not None and char.isspace():
            self.advance()
            char = self.peek()

    def lex_equal(self):
        if self.peek() == "=":
            self.advance()
            return Lexeme(Lexeme.DOUBLE_EQUAL, line=self.line, col=self.col - 2)
        else:
            return Lexeme(Lexeme.EQUAL, line=self.line, col=self.col - 1)

    def lex_word(self, head):
        ch = self.peek()
        if ch is not None and ch in self.word_chars:
            self.advance()
            return self.lex_word(head + ch)
        else:
            return head

    def lex_number(self, head):
       ch = self.peek() 
       if ch is not None and ch.isdigit():
           self.advance()
           return self.lex_number(head + ch)
       else:
           return head
