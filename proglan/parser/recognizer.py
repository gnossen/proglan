# Author: Richard Belleville

from ..lexer.lexeme import lexeme
from ..lexer.scanner import scanner

class Recognizer:
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

    def recognize(self):
        if self.input is None:
            raise Exception("Attempting to parse with no input supplied.")
        else:
            lexemes = Scanner(input=self.input).scan()
            parser = Parser(lexemes)
            try:
                parser.parse()
                return True
            except:
                return False
