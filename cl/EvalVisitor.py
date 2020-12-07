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
    def __init__(self, symbols={}):
        self.symbols = symbols

    # Visit a parse tree produced by PolyBotParser#root.
    def visitRoot(self, ctx:PolyBotParser.RootContext):
        lines = ctx.line()
        text = ""
        files = []
        for line in lines:
            aux = self.visit(line)
            if aux != '' and not aux.endswith('.png'): text += aux + "\n"
            elif aux.endswith('.png'): files.append(aux)
        if text != "": print (text)
        return self.symbols, text, files

    
    # Visit a parse tree produced by PolyBotParser#expr.
    def visitExpr(self, ctx:PolyBotParser.ExprContext):
        l = [n for n in ctx.getChildren()]
        if len(l) == 1:
            return self.visit(l[0])
        elif len(l) == 2:
            if l[0].getText() == '#':
                return self.visit(l[1]).bounding_box()
            elif l[0].getText() == '!':
                n = int(l[1].getText())
                if n < 0: 
                    raise WrongArgumentException("Negative integer")
                return ConvexPolygon.random_polygon(n)
        elif len(l) == 3:
            pol0 = self.visit(l[0])
            pol1 = self.visit(l[2])
            if l[1].getText() == '*':
                return ConvexPolygon.intersection(pol0,pol1)
            elif l[1].getText() == '+':
                return ConvexPolygon.union(pol0,pol1)
    
    # Visit a parse tree produced by PolyBotParser#pointlist.
    def visitPointlist(self, ctx:PolyBotParser.PointlistContext):
        l = []
        for point in ctx.point():
            l.append(self.visit(point))
        return ConvexPolygon.build_from_points(l)


    # Visit a parse tree produced by PolyBotParser#assign.
    def visitAssign(self, ctx:PolyBotParser.AssignContext):
        id = ctx.identifier().getText()
        self.symbols[id] = self.visit(ctx.expr())
        return ''
    
    # Visit a parse tree produced by PolyBotParser#equall.
    def visitEquall(self, ctx:PolyBotParser.EquallContext):
        pol0 = self.visit(ctx.expr(0))
        pol1 = self.visit(ctx.expr(1))
        if pol0 == pol1:
            return 'yes'
        else:
            return 'no'


    # Visit a parse tree produced by PolyBotParser#printl.
    def visitPrintl(self, ctx:PolyBotParser.PrintlContext):
        if ctx.expr():
            pol = self.visit(ctx.expr())
            return " ".join(map(str,pol.points))
        elif ctx.string():
            return self.visit(ctx.string())


    # Visit a parse tree produced by PolyBotParser#comment.
    def visitComment(self, ctx:PolyBotParser.CommentContext):
        return ''


    # Visit a parse tree produced by PolyBotParser#colorl.
    def visitColorl(self, ctx:PolyBotParser.ColorlContext):
        pol = self.visit(ctx.identifier())
        pol.color = self.visit(ctx.color())
        return ''

    # Visit a parse tree produced by PolyBotParser#areal.
    def visitAreal(self, ctx:PolyBotParser.ArealContext):
        pol = self.visit(ctx.expr())
        return format(pol.area(),".3f")

    # Visit a parse tree produced by PolyBotParser#perimeterl.
    def visitPerimeterl(self, ctx:PolyBotParser.PerimeterlContext):
        pol = self.visit(ctx.expr())
        return format(pol.perimeter(),".3f")
    
    # Visit a parse tree produced by PolyBotParser#verticesl.
    def visitVerticesl(self, ctx:PolyBotParser.VerticeslContext):
        pol = self.visit(ctx.expr())
        return str(pol.number_vertices())
    
    # Visit a parse tree produced by PolyBotParser#centroidl.
    def visitCentroidl(self, ctx:PolyBotParser.CentroidlContext):
        pol = self.visit(ctx.expr())
        return str(pol.centroid())
        
    # Visit a parse tree produced by PolyBotParser#regularl.
    def visitRegularl(self, ctx:PolyBotParser.RegularlContext):
        pol = self.visit(ctx.expr())
        if pol.is_regular():
            return 'yes'
        else:
            return 'no'
    

    # Visit a parse tree produced by PolyBotParser#insidel.
    def visitInsidel(self, ctx:PolyBotParser.InsidelContext):
        pol0 = self.visit(ctx.expr(0))
        pol1 = self.visit(ctx.expr(1))
        if pol1.inside_polygon(pol0):
            return 'yes'
        else:
            return 'no'


    # Visit a parse tree produced by PolyBotParser#drawl.
    def visitDrawl(self, ctx:PolyBotParser.DrawlContext):
        filename = self.visit(ctx.filename())
        l = []
        for elem in ctx.expr():
            l.append(self.visit(elem))
        ConvexPolygon.draw_polygons(l,filename)
        return filename


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
        id = ctx.getText()
        if id in self.symbols:
            return self.symbols[id]
        else:
            raise WrongArgumentException(id + " Not defined")
    
    # Visit a parse tree produced by PolyBotParser#filename.
    def visitFilename(self, ctx:PolyBotParser.FilenameContext):
        return ctx.getText()
    


del PolyBotParser