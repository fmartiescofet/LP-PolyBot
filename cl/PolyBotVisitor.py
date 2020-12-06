# Generated from PolyBot.g by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PolyBotParser import PolyBotParser
else:
    from PolyBotParser import PolyBotParser

# This class defines a complete generic visitor for a parse tree produced by PolyBotParser.

class PolyBotVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PolyBotParser#root.
    def visitRoot(self, ctx:PolyBotParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#line.
    def visitLine(self, ctx:PolyBotParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#expr.
    def visitExpr(self, ctx:PolyBotParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#assign.
    def visitAssign(self, ctx:PolyBotParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#printl.
    def visitPrintl(self, ctx:PolyBotParser.PrintlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#comment.
    def visitComment(self, ctx:PolyBotParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#colorl.
    def visitColorl(self, ctx:PolyBotParser.ColorlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#areal.
    def visitAreal(self, ctx:PolyBotParser.ArealContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#perimeterl.
    def visitPerimeterl(self, ctx:PolyBotParser.PerimeterlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#verticesl.
    def visitVerticesl(self, ctx:PolyBotParser.VerticeslContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#insidel.
    def visitInsidel(self, ctx:PolyBotParser.InsidelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#drawl.
    def visitDrawl(self, ctx:PolyBotParser.DrawlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#regularl.
    def visitRegularl(self, ctx:PolyBotParser.RegularlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#point.
    def visitPoint(self, ctx:PolyBotParser.PointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#color.
    def visitColor(self, ctx:PolyBotParser.ColorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#string.
    def visitString(self, ctx:PolyBotParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#filename.
    def visitFilename(self, ctx:PolyBotParser.FilenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#identifier.
    def visitIdentifier(self, ctx:PolyBotParser.IdentifierContext):
        return self.visitChildren(ctx)



del PolyBotParser