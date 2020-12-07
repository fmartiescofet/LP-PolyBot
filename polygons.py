import math
import random
from PIL import Image, ImageDraw, ImageColor


class WrongArgumentException(Exception):
    pass


class Point:
    def __init__(self, x, y):
        """
        Constructs a Point object from its x and y coordinates
        Input: x and y coordinates
        Complexity: Constant
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return format(self.x, ".3f") + " " + format(self.y, ".3f")

    def __repr__(self):
        return format(self.x, ".3f") + " " + format(self.y, ".3f")

    @staticmethod
    def left_of(p1, p2, p3):
        return (p2.x - p1.x) * (p3.y - p1.y) > (p2.y - p1.y) * (p3.x - p1.x)

    @staticmethod
    def ccw(p1, p2, p3):
        """>0 if ccw,<0 if cw, 0 if colinear"""
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


class ConvexPolygon:
    def __init__(self, points, color=None):
        self.points = points
        if color is not None:
            self.color = color
        else:
            self.color = (0, 0, 0)

    def __eq__(self, other):
        if isinstance(other, ConvexPolygon):
            return self.points == other.points
        return False

    def inside(self, point):
        n = len(self.points)
        if n == 0:
            return False
        if n == 1:
            return self.points[0] == point
        if n == 2:
            return Point.ccw(self.points[0], self.points[1], point) == 0
        for i in range(0, n):
            if Point.ccw(self.points[i], self.points[(i + 1) % n], point) > 0:
                return False
        return True

    def inside_polygon(self, polygon):
        for point in polygon.points:
            if not self.inside(point):
                return False
        return True

    def number_vertices(self):
        return len(self.points)

    def perimeter(self):
        sum = 0
        n = len(self.points)
        for i in range(0, n):
            sum += Point.distance(self.points[i], self.points[(i + 1) % n])
        return sum

    def area(self):
        area = 0
        n = len(self.points)
        for i in range(0, n):
            area += (self.points[i].x + self.points[(i + 1) % n].x) * \
                (self.points[i].y - self.points[(i + 1) % n].y)
        return abs(area / 2.0)

    def bounding_box(self):
        """
        TODO: Pensar que passa en cas llista buida
        """
        if len(self.points) == 0:
            return ConvexPolygon.build_from_points([])
        Xs = [p.x for p in self.points]
        Ys = [p.y for p in self.points]
        l = [
            Point(
                min(Xs), min(Ys)), Point(
                min(Xs), max(Ys)), Point(
                max(Xs), min(Ys)), Point(
                    max(Xs), max(Ys))]
        return ConvexPolygon.build_from_points(l, self.color)
        # return (min(Xs),max(Xs),min(Ys),max(Ys))

    def bounding_box_tuple(self):
        """
        TODO: Pensar que passa en cas llista buida
        """
        if len(self.points) == 0:
            return (0, 0, 0, 0)
        Xs = [p.x for p in self.points]
        Ys = [p.y for p in self.points]
        return (min(Xs), max(Xs), min(Ys), max(Ys))

    def centroid(self):
        """
        TODO: Pensar que passa en cas llista buida
        """
        n = len(self.points)
        if n == 0:
            return Point(0, 0)
        if n == 1:
            return self.points[0]
        if n == 2:
            x = (self.points[0].x + self.points[1].x) / 2.0
            y = (self.points[0].y + self.points[1].y) / 2.0
            return Point(x, y)
        det = 0
        centroidX = 0
        centroidY = 0
        n = len(self.points)
        for i in range(0, n):
            tmp = self.points[i].x * self.points[(i + 1) %
                                                 n].y - self.points[(i + 1) %
                                                                    n].x * self.points[i].y
            det += tmp
            centroidX += (self.points[i].x + self.points[(i + 1) % n].x) * tmp
            centroidY += (self.points[i].y + self.points[(i + 1) % n].y) * tmp

        return Point(centroidX / (3 * det), centroidY / (3 * det))

    def is_regular(self):
        """
        We assume that a polygon of 0, 1 or 2 vertexs is regular
        """
        n = len(self.points)
        if (n < 3):
            return True
        side = Point.distance(self.points[0], self.points[1])

        for i in range(1, n):
            if Point.distance(self.points[i],
                              self.points[(i + 1) % n]) != side:
                return False
        return True

    @staticmethod
    def random_polygon(n):
        l = []
        random.seed()
        for i in range(n):
            l.append(Point(random.uniform(0, 1), random.uniform(0, 1)))
        print(l)
        return ConvexPolygon.build_from_points(l)

    @staticmethod
    def union(polygon1, polygon2):
        return ConvexPolygon.build_from_points(
            polygon1.points + polygon2.points, polygon1.color)

    @staticmethod
    def intersection(polygon1, polygon2):
        """TODO"""
        return ConvexPolygon.build_from_points(
            polygon1.points + polygon2.points, polygon1.color)

    @staticmethod
    def draw_polygons(polygons, filename="image.png"):

        bboxes = [pol.bounding_box_tuple() for pol in polygons]
        x_min = min([b[0] for b in bboxes])
        x_max = max([b[1] for b in bboxes])
        y_min = min([b[2] for b in bboxes])
        y_max = max([b[3] for b in bboxes])
        if (x_max - x_min > y_max - y_min):
            add = x_max - x_min - (y_max - y_min)
            y_max += add / 2.0
            y_min -= add / 2.0
        elif (x_max - x_min < y_max - y_min):
            add = y_max - y_min - (x_max - x_min)
            x_max += add / 2.0
            x_min -= add / 2.0

        img = Image.new('RGB', (400, 400), 'White')
        dib = ImageDraw.Draw(img)
        for polygon in polygons:
            pol = [(1 + 397 * (p.x - x_min) / (x_max - x_min), 398 - 397 *
                    (p.y - y_min) / (y_max - y_min)) for p in polygon.points]
            if len(pol) == 1:
                dib.point(pol, fill=tuple([int(255 * x)
                                           for x in polygon.color]))
            elif len(pol) >= 2:
                dib.polygon(pol, outline=tuple(
                    [int(255 * x) for x in polygon.color]))

        img.save(filename)

    @staticmethod
    def build_from_points(points, color=None):
        if len(points) < 3:
            points.sort(key=lambda p: (p.x, p.y))
            return ConvexPolygon(points, color)

        # Leftest point, in case of tie the lowest one
        p1 = min(points, key=lambda p: (p.x, p.y))
        l = [p for p in points if p != p1]
        # print(p1,l)
        """for e in map(lambda p: ((p.y - p1.y) / (p.x - p1.x),
                                (p.y - p1.y)**2 + (p.x - p1.x)**2) if (p.x != p1.x) else (math.inf,
                                                                                          (p.y - p1.y)**2 + (p.x - p1.x)**2),
                     l):
            print(e)"""
        l.sort(reverse=True, key=lambda p: ((p.y - p1.y) / (p.x - p1.x), -(p.y - p1.y)**2 -
                                            (p.x - p1.x)**2) if p.x != p1.x else (math.inf, -(p.y - p1.y)**2 - (p.x - p1.x)**2))
        #print (l)

        q = [p1]
        for point in l:
            while len(q) > 1 and Point.ccw(q[-2], q[-1], point) >= 0:
                q.pop()
            q.append(point)

        return ConvexPolygon(q, color)


if __name__ == "__main__":
    #print(Point(0, 1) == Point(0, 1))
    """
    l = [Point(0, 1), Point(2, 3), Point(1, 1), Point(0, 4), Point(0, 3)]
    q = ConvexPolygon.build_from_points(l)

    print(q.inside(Point(0,3)))
    print(q.inside(Point(1,1.5)))
    print(q.inside(Point(0,0)))
    print(q.perimeter())
    print(q.area())
    print(q.bounding_box())
    print("Points: ",[(p.x,p.y) for p in q.points])
    l = [Point(0, 0), Point(0, 0.8), Point(1, 1), Point(0.2, 0.8)]
    pol2 = ConvexPolygon.build_from_points(l,(1,0,0))
    ConvexPolygon.draw_polygons([q,pol2])
    un = ConvexPolygon.union(q,pol2)
    print("Un:", [(p.x,p.y) for p in un.points])
    #ConvexPolygon.draw_polygons([un])"""

    """s = [(p.x+50,p.y+50) for p in q]
    print("S:",s)

    img = Image.new('RGB', (100, 100), 'White')
    dib = ImageDraw.Draw(img)
    dib.polygon(s,fill='Orange')
    img.save('prova.png')"""
    #l = [Point(0, 0), Point(0, 1), Point(1, 1), Point(0.2, 0.8)]
    # ConvexPolygon.build_from_points(l)

    l = [Point(0, 0), Point(0, 1), Point(1, 1), Point(0.2, 0.8)]
    pol2 = ConvexPolygon.build_from_points(l)
    print(pol2.points)
