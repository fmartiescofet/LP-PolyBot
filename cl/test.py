import sys
from antlr4 import *
from PolyBotLexer import PolyBotLexer
from PolyBotParser import PolyBotParser
from EvalVisitor import EvalVisitor
#input_stream = InputStream(input('? '))
#input_stream = StdinStream()
#input_stream = InputStream('p23 := [ 0 0 ]\nprint "hola"')
#input_stream = InputStream('p23 := [ -1 0 0.5 1]\nprint "hola"\nprint p23\ncolor p23, {1 0 0}\ndraw "im.png", p23\n')

input_stream = FileStream("script3.txt")

lexer = PolyBotLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PolyBotParser(token_stream)
tree = parser.root()
t = tree.toStringTree(recog=parser)
print(t.replace("\\n",'\n'))

evalV = EvalVisitor()
evalV.visit(tree)