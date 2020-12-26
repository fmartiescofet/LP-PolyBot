import math
import random
from PIL import Image, ImageDraw, ImageColor


class WrongArgumentException(Exception):
    pass


class Point:
    def __init__(self, x, y):
        """
        Constructs a Point object from its x and y coordinates, rounded to three decimal to avoid precision problems
        Input: x and y coordinates
        Complexity: Constant
        """
        self.x = round(x,3)
        self.y = round(y,3)

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
    def ccw(p1, p2, p3):
        """
        Returns >0 if p1,p2,p3 build a ccw turn, <0 if cw, 0 if colinear
        Input: Points p1,p2,p3
        Complexity: Constant
        """
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    @staticmethod
    def inline(p1,p2,p3):
        """
        Returns True if p3 is inside the line segment p1-p2
        Input: Points p1,p2,p3
        Complexity: Constant
        """
        cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        if cross != 0: return False
        if abs(p2.x - p1.x) >= abs(p2.y - p1.y):
            if p2.x - p1.x > 0:
                return p1.x <= p3.x and p3.x <= p2.x
            else:
                return p2.x <= p3.x and p3.x <= p1.x
        else:
            if p2.y - p1.y > 0:
                return p1.y <= p3.y and p3.y <= p2.y
            else:
                return p2.y <= p3.y and p3.y <= p1.y

    

    @staticmethod
    def distance(p1, p2):
        """
        Computes distance between p1 and p2
        Input: Points p1,p2
        Complexity: Constant
        """
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    @staticmethod
    def line_intersection(p0, p1, p2, p3):
        """
        Computes the intersection of line segments p0-p1 and p2-p3
        Returns an empty list if they don't intersect, with one point if they only cross in one point or with two representing the line segment of the intersection
        Complexity: Constant
        """
        slope0 = (p1.y-p0.y)/(p1.x-p0.x) if p1.x != p0.x else math.inf
        slope1 = (p3.y-p2.y)/(p3.x-p2.x) if p3.x != p2.x else math.inf

        def filter_unique(a,b):
            if a != b:
                return [a,b]
            return [a]

        """Parallel lines"""
        if slope0 == slope1:
            if Point.ccw(p0,p1,p2) == 0:
                if Point.inline(p0,p1,p2) and Point.inline(p0,p1,p3):
                    return filter_unique(p2,p3)
                elif Point.inline(p0,p1,p2) and not Point.inline(p0,p1,p3):
                    if Point.inline(p2,p3,p0):
                        return filter_unique(p0,p2)
                    elif Point.inline(p2,p3,p1):
                        return filter_unique(p1,p2)
                elif not Point.inline(p0,p1,p2) and Point.inline(p0,p1,p3):
                    if Point.inline(p2,p3,p0):
                        return filter_unique(p0,p3)
                    elif Point.inline(p2,p3,p1):
                        return filter_unique(p1,p3)
                elif not Point.inline(p0,p1,p2) and not Point.inline(p0,p1,p3):
                    return []
            else:
                 return []


        if slope0 == math.inf:
            intercept1= p2.y - slope1*p2.x
            x = p0.x
            y = slope1*x + intercept1
            return [Point(x,y)]

        if slope1 == math.inf:
            intercept0 = p0.y - slope0*p0.x
            x = p2.x
            y = slope0*x + intercept0
            return [Point(x,y)]

        slope0 = (p1.y-p0.y)/(p1.x-p0.x)
        slope1 = (p3.y-p2.y)/(p3.x-p2.x)

        intercept0 = p0.y - slope0*p0.x
        intercept1= p2.y - slope1*p2.x

        x = (intercept1-intercept0)/(slope0-slope1)
        y = slope0*x + intercept0

        return [Point(x, y)]


class ConvexPolygon:
    def __init__(self, points, color=None):
        """
        Construct a polygon from it's processed points
        Input: List with processed points and color (optional)
        Complexity: Constant
        """
        self.points = points
        if color is not None:
            self.color = color
        else:
            self.color = (0, 0, 0)

    def __eq__(self, other):
        """
        Overrides the default equal implementation
        Only checks for points, not color
        Complexity: Linear
        """
        if isinstance(other, ConvexPolygon):
            return self.points == other.points
        return False

    def inside(self, point):
        """
        Checks if point is inside a polygon
        Input: A point
        Complexity: Linear in the number of points of self
        """
        n = len(self.points)
        if n == 0:
            return False
        if n == 1:
            return self.points[0] == point
        if n == 2:
            return Point.inline(self.points[0], self.points[1], point) == 0
        for i in range(0, n):
            if Point.ccw(self.points[i], self.points[(i + 1) % n], point) > 0:
                return False
        return True

    def inside_polygon(self, polygon):
        """
        Checks if polygon is inside self
        Input: A polygon
        Complexity: n1*n2 where n1 is the number of points of self and n2 the number of points of polygon
        """
        for point in polygon.points:
            if not self.inside(point):
                return False
        return True

    def number_vertices(self):
        """
        Returns the number of vertices of self
        Complexity: Constant
        """
        return len(self.points)

    def perimeter(self):
        """
        Returns the perimeter of self
        Complexity: Linear in the number of points of self
        """
        sum = 0
        n = len(self.points)
        for i in range(n):
            sum += Point.distance(self.points[i], self.points[(i + 1) % n])
        return sum

    def area(self):
        """
        Returns the area of self
        Complexity: Linear in the number of points of self
        """
        area = 0
        n = len(self.points)
        for i in range(n):
            area += (self.points[i].x + self.points[(i + 1) % n].x) * \
                (self.points[i].y - self.points[(i + 1) % n].y)
        return abs(area / 2.0)

    def bounding_box(self):
        """
        Returns a polygon that is the bounding box of self
        Complexity: Linear in the number of points of self
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
        Returns a tuple with the bounding box of self
        Complexity: Linear in the number of points of self
        """
        if len(self.points) == 0:
            return None
        Xs = [p.x for p in self.points]
        Ys = [p.y for p in self.points]
        return (min(Xs), max(Xs), min(Ys), max(Ys))

    def centroid(self):
        """
        Returns the centroid of self
        Complexity: Linear in the number of points of self
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
        for i in range(n):
            tmp = self.points[i].x * self.points[(i + 1) %
                                                 n].y - self.points[(i + 1) %
                                                                    n].x * self.points[i].y
            det += tmp
            centroidX += (self.points[i].x + self.points[(i + 1) % n].x) * tmp
            centroidY += (self.points[i].y + self.points[(i + 1) % n].y) * tmp

        return Point(centroidX / (3 * det), centroidY / (3 * det))

    def is_regular(self):
        """
        Checks if self is a regular polygon
        We assume that a polygon of 0, 1 or 2 vertexs is regular
        Complexity: Linear in the number of points of self
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
        """
        Builds a polygons made with n points drawn at random in the unit square [0,1]^2
        Input: n a Natural number
        Complexity: n*log(n)
        """
        l = []
        random.seed()
        for i in range(n):
            l.append(Point(random.uniform(0, 1), random.uniform(0, 1)))
        return ConvexPolygon.build_from_points(l)

    @staticmethod
    def union(polygon1, polygon2):
        """
        Builds the union of two convex polygons by computing the convex hull of both polygons
        Input: Two convex polygons
        Complexity: (n1+n2)*log(n1+n2) where ni is the number of points of polygon i
        """
        return ConvexPolygon.build_from_points(
            polygon1.points + polygon2.points, polygon1.color)

    @staticmethod
    def intersection(polygon1, polygon2):
        """
        Computes the intersection of two polygons
        Input: Two convex polygons
        Complexity: n1*n2 where ni is the number of points of polygon i
        """
        
        n1 = len(polygon1.points)
        n2 = len(polygon2.points)
        if n1 == 0 or n2 == 0: return ConvexPolygon.build_from_points([], polygon1.color)
        if n1 == 1:
            if polygon2.inside_polygon(polygon1): return ConvexPolygon.build_from_points(polygon1.points, polygon1.color)
            else: return ConvexPolygon.build_from_points([], polygon1.color)
        if n2 == 1:
            if polygon1.inside_polygon(polygon2): return ConvexPolygon.build_from_points(polygon2.points, polygon1.color)
            else: return ConvexPolygon.build_from_points([], polygon1.color)
        if n1 == 2 and n2 == 2:
            intersection = Point.line_intersection(polygon1.points[0],polygon1.points[1],polygon2.points[0],polygon2.points[1])
            return ConvexPolygon.build_from_points(intersection, polygon1.color)
        if polygon2.inside_polygon(polygon1): 
            return ConvexPolygon.build_from_points(polygon1.points,polygon1.color)

        if polygon1.inside_polygon(polygon2): 
            return ConvexPolygon.build_from_points(polygon2.points,polygon2.color)

        # points1 >=3 and points2 >=3
        l2 = polygon2.points

        for i in range(n1):
            C = []
            n2 = len(l2)
            for j in range(n2):
                if Point.ccw(polygon1.points[i],polygon1.points[(i+1)%n1],l2[j]) <= 0 and Point.ccw(polygon1.points[i],polygon1.points[(i+1)%n1],l2[(j+1)%n2]) > 0:
                    C.append(l2[j])
                    X = Point.line_intersection(polygon1.points[i],polygon1.points[(i+1)%n1],l2[j],l2[(j+1)%n2])
                    C += X
                elif Point.ccw(polygon1.points[i],polygon1.points[(i+1)%n1],l2[j]) > 0 and Point.ccw(polygon1.points[i],polygon1.points[(i+1)%n1],l2[(j+1)%n2]) > 0:
                    pass
                elif Point.ccw(polygon1.points[i],polygon1.points[(i+1)%n1],l2[j]) > 0 and Point.ccw(polygon1.points[i],polygon1.points[(i+1)%n1],l2[(j+1)%n2]) <= 0:
                    X = Point.line_intersection(polygon1.points[i],polygon1.points[(i+1)%n1],l2[j],l2[(j+1)%n2])
                    C += X
                else:
                    C.append(l2[j])
            l2 = C
            
        return ConvexPolygon.build_from_points(l2, polygon1.color)

    @staticmethod
    def draw_polygons(polygons, filename="image.png"):
        """
        Draws a list of polygons in a file
        Input: List of polygons, filename (optional)
        Complexity: Linear in the number of polygons and number of points
        """

        bboxes = [pol.bounding_box_tuple() for pol in polygons if pol.points]
        x_min = min([b[0] for b in bboxes if b])
        x_max = max([b[1] for b in bboxes if b])
        y_min = min([b[2] for b in bboxes if b])
        y_max = max([b[3] for b in bboxes if b])
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

        if x_max == x_min and y_max == y_min:
            x_max += 0.5
            x_min -= 0.5
            y_max += 0.5
            y_min -= 0.5
        
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
        """
        Builds a convex polygon from a list of points using the Graham Scan algorithm
        The list of points is the convex hull o fthe polygon ordered clockwise and taking the leftest point as reference
        Input: List of points inside a convex polygon, color (Optional)
        Complexity: n*log(n) where n is the length of the point list
        """
        if len(points) < 3:
            points.sort(key=lambda p: (p.x, p.y))
            if len(points) == 2 and points[0] == points[1]:
                return ConvexPolygon([points[0]], color)
            return ConvexPolygon(points, color)

        # Leftest point, in case of tie the lowest one
        p1 = min(points, key=lambda p: (p.x, p.y))
        l = [p for p in points if p != p1]
        
        l.sort(reverse=True, key=lambda p: ((p.y - p1.y) / (p.x - p1.x), -(p.y - p1.y)**2 -
                                            (p.x - p1.x)**2) if p.x != p1.x else (math.inf, -(p.y - p1.y)**2 - (p.x - p1.x)**2))

        q = [p1]
        for point in l:
            while len(q) > 1 and Point.ccw(q[-2], q[-1], point) >= 0:
                q.pop()
            q.append(point)

        return ConvexPolygon(q, color)


if __name__ == "__main__":
    """
    Some test cases
    """
    
    l = [Point(0, 1), Point(2, 3), Point(1, 1), Point(0, 4), Point(0, 3),Point(-1,2)]
    q = ConvexPolygon.build_from_points(l)

    print(q.inside(Point(0,3)))
    print(q.inside(Point(1,1.5)))
    print(q.inside(Point(0,0)))
    print(q.perimeter())
    print(q.area())
    print(q.bounding_box().points)
    print(q.points)
    l = [Point(0, 0), Point(0, 0.8), Point(1, 1), Point(0.2, 0.9)]
    pol2 = ConvexPolygon.build_from_points(l,(1,0,0))
    ConvexPolygon.draw_polygons([q,pol2],"q_pol2.png")
    un = ConvexPolygon.union(q,pol2)
    print("Union:", un.points)
    ConvexPolygon.draw_polygons([un],"union.png")
    intersection = ConvexPolygon.intersection(q,pol2)
    print("Intersection:", intersection.points)
    ConvexPolygon.draw_polygons([intersection],"intersection.png")

    


    p1 = ConvexPolygon.build_from_points([])
    l1 = [Point(1, 1), Point(1, 2), Point(2, 1.5)]
    p2 = ConvexPolygon.build_from_points(l1)
    ConvexPolygon.draw_polygons([p1,p2])
    
    
    l1 = [Point(0, 0), Point(0, 1), Point(1, 0.5)]
    p1 = ConvexPolygon.build_from_points(l1)
    l2 = [Point(1, 0), Point(1, 1), Point(0, 0.5)]
    p2 = ConvexPolygon.build_from_points(l2)
    print("p1: ",p1.points)
    print("p2: ", p2.points)
    p1.color=(0,1,0)
    p2.color=(1,0,0)
    ConvexPolygon.draw_polygons([p1,p2],"p1p2.png")
    
    intersection = ConvexPolygon.intersection(p1,p2)
    ConvexPolygon.draw_polygons([intersection],"intersection2.png")
    print("Intersection: ", intersection.points)

    p1 = ConvexPolygon.random_polygon(5)
    p2 = ConvexPolygon.random_polygon(5)

    p1.color=(0,1,0)
    p2.color=(1,0,0)
    ConvexPolygon.draw_polygons([p1,p2],"random.png")
    inte = ConvexPolygon.intersection(p1,p2)
    ConvexPolygon.draw_polygons([inte],"intersection3.png")
