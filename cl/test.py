import sys
from antlr4 import *
from PolyBotLexer import PolyBotLexer
from PolyBotParser import PolyBotParser
from EvalVisitor import EvalVisitor

input_stream = FileStream("script3.txt")

lexer = PolyBotLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PolyBotParser(token_stream)
tree = parser.root()
t = tree.toStringTree(recog=parser)
print(t.replace("\\n",'\n'))

evalV = EvalVisitor()
evalV.visit(tree)