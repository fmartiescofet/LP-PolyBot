from antlr4 import *
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from polygons import Point, ConvexPolygon, WrongArgumentException

if __name__ is not None and "." in __name__:
    from .PolyBotParser import PolyBotParser
else:
    from PolyBotParser import PolyBotParser


class EvalVisitor(ParseTreeVisitor):
    def __init__(self):
        self.symbols = {}

    # Visit a parse tree produced by PolyBotParser#root.
    def visitRoot(self, ctx:PolyBotParser.RootContext):
        lines = [n for n in ctx.getChildren()]
        for line in lines:
            self.visit(line)


    # Visit a parse tree produced by PolyBotParser#assign.
    def visitAssign(self, ctx:PolyBotParser.AssignContext):
        id = self.visit(ctx.identifier())
        l = []
        for point in ctx.point():
            l.append(self.visit(point))
        self.symbols[id] = ConvexPolygon.build_from_points(l)


    # Visit a parse tree produced by PolyBotParser#printl.
    def visitPrintl(self, ctx:PolyBotParser.PrintlContext):
        if ctx.identifier():
            id = self.visit(ctx.identifier())
            if id in self.symbols:
                print (" ".join(map(str,self.symbols[id].points)))
            else:
                raise WrongArgumentException(id + " Not defined")

        elif ctx.string():
            print(self.visit(ctx.string()))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyBotParser#comment.
    def visitComment(self, ctx:PolyBotParser.CommentContext):
        return None


    # Visit a parse tree produced by PolyBotParser#colorl.
    def visitColorl(self, ctx:PolyBotParser.ColorlContext):
        id = self.visit(ctx.identifier())
        if id in self.symbols:
            self.symbols[id].color = self.visit(ctx.color())
        else:
            raise WrongArgumentException(id + " Not defined")


    # Visit a parse tree produced by PolyBotParser#areal.
    def visitAreal(self, ctx:PolyBotParser.ArealContext):
        id = self.visit(ctx.identifier())
        if id in self.symbols:
            print (format(self.symbols[id].area(),".3f"))
        else:
            raise WrongArgumentException(id + " Not defined")


    # Visit a parse tree produced by PolyBotParser#perimeterl.
    def visitPerimeterl(self, ctx:PolyBotParser.PerimeterlContext):
        id = self.visit(ctx.identifier())
        if id in self.symbols:
            print (format(self.symbols[id].perimeter(),".3f"))
        else:
            raise WrongArgumentException(id + " Not defined")


    # Visit a parse tree produced by PolyBotParser#verticesl.
    def visitVerticesl(self, ctx:PolyBotParser.VerticeslContext):
        id = self.visit(ctx.identifier())
        if id in self.symbols:
            print (self.symbols[id].number_vertices())
        else:
            raise WrongArgumentException(id + " Not defined")
        
    # Visit a parse tree produced by PolyBotParser#regularl.
    def visitRegularl(self, ctx:PolyBotParser.RegularlContext):
        id = self.visit(ctx.identifier())
        if id in self.symbols:
            if self.symbols[id].is_regular():
                print ('yes')
            else:
                print ('no')
        else:
            raise WrongArgumentException(id + " Not defined")


    # Visit a parse tree produced by PolyBotParser#insidel.
    def visitInsidel(self, ctx:PolyBotParser.InsidelContext):
        id0 = self.visit(ctx.identifier(0))
        id1 = self.visit(ctx.identifier(1))
        if id0 in self.symbols and id1 in self.symbols:
            if self.symbols[id1].inside_polygon(self.symbols[id0]):
                print ('yes')
            else:
                print ('no')
        elif id0 not in self.symbols:
            raise WrongArgumentException(id0 + " Not defined")
        else:
            raise WrongArgumentException(id1 + " Not defined")


    # Visit a parse tree produced by PolyBotParser#drawl.
    def visitDrawl(self, ctx:PolyBotParser.DrawlContext):
        filename = self.visit(ctx.filename())
        l = []
        for elem in ctx.identifier():
            id = self.visit(elem)
            if id in self.symbols:
                l.append(self.symbols[id])
            else:
                raise WrongArgumentException(id + " Not defined")
        ConvexPolygon.draw_polygons(l,filename)


    # Visit a parse tree produced by PolyBotParser#point.
    def visitPoint(self, ctx:PolyBotParser.PointContext):
        l = [n for n in ctx.getChildren()]
        return Point(float(l[0].getText()),float(l[1].getText()))


    # Visit a parse tree produced by PolyBotParser#color.
    def visitColor(self, ctx:PolyBotParser.ColorContext):
        l = [n for n in ctx.getChildren()]
        return (float(l[0].getText()), float(l[1].getText()), float(l[2].getText()))


    # Visit a parse tree produced by PolyBotParser#string.
    def visitString(self, ctx:PolyBotParser.StringContext):
        return ctx.getText()


    # Visit a parse tree produced by PolyBotParser#identifier.
    def visitIdentifier(self, ctx:PolyBotParser.IdentifierContext):
        return ctx.getText()
    
    # Visit a parse tree produced by PolyBotParser#filename.
    def visitFilename(self, ctx:PolyBotParser.FilenameContext):
        return ctx.getText()



del PolyBotParser