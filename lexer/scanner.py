import os
from lexer import *

class Scanner:
    def __init__(self, input=None, file=None):
        if input is not None:
            self.load_str(input)
        elif file is not None:
            self.load_file(file)
        else:
            self.input = None

    def load_file(self, filename):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(cur_dir, filename)
        with open(filepath, 'r') as f:
            self.input = f.read()

    def load_str(self, str):
        self.input = str

    def scan(self):
        if self.input is None:
            raise Exception("Attempting to scan with no input supplied.")
        else:
            lexer = Lexer(self.input)
            lexeme_list = []
            lexeme = lexer.lex()
            while not lexeme.is_type(Lexeme.EOF):
                lexeme_list.append(lexeme)
                lexeme = lexer.lex()

            lexeme_list.append(lexeme)
            return self.postprocess(lexeme_list)

    def postprocess(self, lexemes):
        # trims leading and trailing newlines
        # and removes repeated newlines
        new_lexes = []
        for i, lex in enumerate(lexemes):
            if not (lex.type == Lexeme.NEWLINE and \
                    len(new_lexes) != 0 and \
                    new_lexes[-1].type == Lexeme.NEWLINE) and \
               not (len(new_lexes) == 0 and lex.type == Lexeme.NEWLINE) and \
               not (lex.type == Lexeme.NEWLINE and i == len(lexemes) - 2):

                new_lexes.append(lex)

        return new_lexes

    def __str__(self):
        s = ""
        lexemes = self.scan()
        for i, lexeme in enumerate(lexemes):
            if i == len(lexemes) - 1:
                s += str(lexeme)
            else:
                s += str(lexeme) + "\n"

        return s
