import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import math

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

    def getLen(self):
        return self.line

    def get_middle_point(self):
        return self.middle_point


def cul_length_angle(point_set,edges):
    pi=3.1415926535
    b=180/pi
    angle_set = []
    # angle=[]
    for i in range(0, len(edges)):
        P1 = Point(point_set[edges[i][0]][0], point_set[edges[i][0]][1])
        P2 = Point(point_set[edges[i][1]][0], point_set[edges[i][1]][1])
        x1=P1.x
        y1=P1.y
        x2=P2.x
        y2=P2.y
        if ((x2<x1) and (y2<y1)):
            angle=270-math.atan(abs(y1 - y2) / abs(x1 - x2))*b
        elif((x2>x1) and (y2<y1)):
            angle = 90+math.atan(abs(y1 - y2) / abs(x2 - x1))*b
        elif((x2<x1) and (y2>y1)):
            angle = 360 - math.atan(abs(x1 - x2) / abs(y2 - y1))*b
        else:
            angle = math.atan(abs(x2 - x1) / abs(y2 - y1))*b
        angle_set.append(angle)

    angle_set = np.array(angle_set)
    last_list = angle_set * (1 / 360)  # normalization

    return last_list

ao=[[2.1,2.9],[0.9,3],[0.89,1],[2,1.11]]
edge_ao=[[0,1],[1,2],[2,3]]

Z=[[3.1,2.9],[2,2.97],[2.1,1.11],[0.98,1.05]]
edge_Z=[[0,1],[1,2],[2,3]]

aaa=cul_length_angle(ao,edge_ao)
print("---------",aaa)
bbb=cul_length_angle(Z,edge_Z)
print("---------",bbb)
