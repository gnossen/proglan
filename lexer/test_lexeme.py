# Author: Richard Belleville

import pytest
from lexeme import *

def test_lexeme_constructor():
   lex = Lexeme(Lexeme.NUMBER) 
   assert lex.type == Lexeme.NUMBER
   assert lex.value == None

   lex2 = Lexeme(Lexeme.STRING, "Hello world.")
   assert lex2.type == Lexeme.STRING
   assert lex2.value == "Hello world."

def test_lexeme_is_type():
   lex = Lexeme(Lexeme.STRING, "Hello world.")
   assert lex.is_type(Lexeme.STRING)

def test_lexeme_str():
   lex = Lexeme(Lexeme.STRING, "Hello world.")
   assert str(lex) == "STRING: Hello world."

   lex2 = Lexeme(-27)
   with pytest.raises(Exception):
       str(lex2)
