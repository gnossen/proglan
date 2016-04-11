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
        self.skip_inconsequential()

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
        elif ch == "[":
            return Lexeme(Lexeme.OSQBRACE, line=self.line, col=self.col - 1)
        elif ch == "]":
            return Lexeme(Lexeme.CSQBRACE, line=self.line, col=self.col - 1)
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
            if self.peek() == "=":
                self.advance()
                return Lexeme(Lexeme.GEQ, line=self.line, col=self.col - 2)
            else:
                return Lexeme(Lexeme.GREATER_THAN, line=self.line, col=self.col - 1)
        elif ch == "<":
            if self.peek() == "=":
                self.advance()
                return Lexeme(Lexeme.LEQ, line=self.line, col=self.col - 2)
            else:
                return Lexeme(Lexeme.LESS_THAN, line=self.line, col=self.col - 1)
        elif ch == "!" and self.peek() == "=":
            self.advance()
            return Lexeme(Lexeme.NEQ, line=self.line, col=self.col - 2)
        elif ch == ";":
            return Lexeme(Lexeme.SEMICOLON, line=self.line, col=self.col - 1)
        elif ch == "&":
            return Lexeme(Lexeme.BITWISE_AND, line=self.line, col=self.col - 1)
        elif ch == "|":
            return Lexeme(Lexeme.BITWISE_OR, line=self.line, col=self.col - 1)
        elif ch == "^":
            return Lexeme(Lexeme.BITWISE_XOR, line=self.line, col=self.col - 1)
        elif ch == "\n":
            return Lexeme(Lexeme.NEWLINE, line=self.line, col=self.col - 1)
        elif ch == "\\":
            if self.peek() == "\n":
                self.advance()
                return self.lex()
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
            elif word == "while":
                return Lexeme(Lexeme.WHILE, line=self.line, col=self.col - 2)
            elif word == "else":
                return Lexeme(Lexeme.ELSE, line=self.line, col=self.col - 4)
            elif word == "lambda":
                return Lexeme(Lexeme.LAMBDA, line=self.line, col=self.col - 6)
            elif word == "return":
                return Lexeme(Lexeme.RETURN, line=self.line, col=self.col - 6)
            elif word == "and":
                return Lexeme(Lexeme.AND, line=self.line, col=self.col - 3)
            elif word == "or":
                return Lexeme(Lexeme.OR, line=self.line, col=self.col - 2)
            elif word == "xor":
                return Lexeme(Lexeme.XOR, line=self.line, col=self.col - 3)
            elif word == "true":
                return Lexeme(Lexeme.BOOL, value=True, line=self.line, col=self.col - 4)
            elif word == "false":
                return Lexeme(Lexeme.BOOL, value=False, line=self.line, col=self.col - 5)
            elif word == "null":
                return Lexeme(Lexeme.NULL, line=self.line, col=self.col - 4)
            else: 
                return Lexeme(Lexeme.IDENTIFIER, value=word, line=self.line, col=self.col - len(word))
        elif ch.isdigit():
            number = self.lex_number(ch)
            return Lexeme(Lexeme.NUMBER, value=int(number), line=self.line, col=self.col - len(number))
        elif ch == '"':
            string = self.lex_string("")
            return Lexeme(Lexeme.STRING, value=string.decode("string-escape"), line=self.line, col=self.col - len(string) - 2)
        else:
            raise Exception("Illegal character '%s' at (%d, %d)." % (ch, self.line + 1, self.col + 1))

    def skip_inconsequential(self):
        last_line = None
        last_col = None
        while last_line != self.line or last_col != self.col:
            last_line = self.line
            last_col = self.col
            self.skip_whitespace()
            self.skip_comment()
        
    def skip_whitespace(self):
        char = self.peek()
        while char is not None and char != "\n" and char.isspace():
            self.advance()
            char = self.peek()

    def skip_comment(self):
        char = self.peek()
        if char == "#":
            while char is not None and char != "\n":
                self.advance()
                char = self.peek()

            if char is not None:
                self.advance()

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

    def lex_string(self, head):
        ch = self.peek()
        if ch is None:
            raise Exception("Encountered EOF before end of string.")
        elif ch != '"':
            self.advance()
            return self.lex_string(head + ch)
        else:
            self.advance()
            return head
