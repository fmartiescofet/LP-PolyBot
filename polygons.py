import math
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
    
    @staticmethod
    def left_of(p1,p2,p3):
        return (p2.x - p1.x)*(p3.y - p1.y) > (p2.y - p1.y)*(p3.x - p1.x)


class ConvexPolygon:
    def __init__(self,points):
        self.points = points
    

    
    @staticmethod
    def build_from_points(points):
        if len(points) < 3: return points
        
        p1 = min(points, key = lambda p: (p.y,p.x)) #Lowest most point, in case of tie the leftest one
        print (p1.x,p1.y)
        l = [p for p in points if p != p1]
        for e in map(lambda p: ((p.y-p1.y) / (p.x-p1.x), (p.y-p1.y)**2 + (p.x-p1.x)**2) if (p.x != p1.x) else (math.inf,(p.y-p1.y)**2 + (p.x-p1.x)**2),l):
            print(e)
        l.sort(reverse=True, key = lambda p: ((p.y-p1.y) / (p.x-p1.x), (p.y-p1.y)**2 + (p.x-p1.x)**2) if p.x != p1.x else (math.inf,(p.y-p1.y)**2 + (p.x-p1.x)**2))
        for elem in l: print (elem.x,elem.y)

        q = [p1]
        for point in l:
            while len(q)>1 and Point.left_of(q[-2],q[-1],point): q.pop()
            q.append(point)

        
        
        print("Q:")
        for e in q:
            print(e.x,e.y)
        return q

if __name__ == "__main__":
    print (Point(0,1) == Point(0,1))
    l = [Point(0,1),Point(2,3),Point(1,1),Point(0,4),Point(0,3)]
    ConvexPolygon.build_from_points(l)

    l = [Point(0,0),Point(0,1),Point(1,1),Point(0.2,0.8)]
    ConvexPolygon.build_from_points(l)