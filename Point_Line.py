
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coor=[x,y]

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def point_coor(self):
        return self.coor

class Line:
    def __init__(self, p1, p2):
        self.x = p1.getX() - p2.getX()
        self.y = p1.getY() - p2.getY()
        self.coor = [[p1.getX(), p1.getY()], [p2.getX(), p2.getY()]]                  #[[x1,y1],[x2,y2]]
        self.line = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
        self.middle_point = [(p1.getX() + p2.getX())/2, (p1.getY() + p2.getY())/2]
        self.start=p1.point_coor                                                       #[x1,y1]
        self.end=p2.point_coor                                                         #[x2,y2]

    def getLen(self):
        return self.line

    def get_middle_point(self):
        return self.middle_point

