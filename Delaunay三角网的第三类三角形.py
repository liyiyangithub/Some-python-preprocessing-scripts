import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import math
from  Get_Coor_from_Json import process_data
#----------------------
#needing:1.polygon-coor-list

def get_main_direction(point_set):
    # 对点集分离横纵坐标
    x = []
    y = []
    for i in range(len(point_set)):
        x.append(point_set[i][0])
        y.append(point_set[i][1])

    angle = []
    l = []

    n = len(x)                      # 点集的长度n
    for i in range(n - 1):
        # 找出第i条边的两个端点(x1, y1), (x2, y2)
        x1 = x[i]
        y1 = y[i]
        x2 = x[i + 1]
        y2 = y[i + 1]

        # 求解第i个线段的模
        l.append(distance([x1, y1], [x2, y2]))
        # 求解第i个线段的角度
        if (x1 == x2):
            angle.append(-90)
        else:
            angle.append(math.atan((y2 - y1) / (x2 - x1)) / (2 * 3.1415926) * 360)

    # 规定步长为1°
    step = 1
    # 规定偏差系数alpha
    alpha = 10
    # 初始化最大的加权和       ？？？？？
    max_sum = -1
    # 初始化主方向
    main_direction = -1
    for base_angle in np.arange(0, 90, step):
        sum = 0.0
        for i in range(n - 1):
            # 当前边在[base-alpha, base+alpha]范围内
            if (base_angle - alpha <= angle[i] and angle[i] <= base_angle + alpha):
                sum = sum + (alpha - abs(base_angle - angle[i])) / alpha * l[i]
            # 当前边的垂边在[base-alpha, base+alpha]范围内
            elif (base_angle - alpha <= angle[i] + 90 and angle[i] + 90 <= base_angle + alpha):
                sum = sum + (alpha - abs(base_angle - (angle[i] + 90))) / alpha * l[i]
            # 当前边在[base-alpha, base+alpha]范围内
            elif (base_angle - alpha <= angle[i] + 180 and angle[i] + 180 <= base_angle + alpha):
                sum = sum + (alpha - abs(base_angle - (angle[i] + 180))) / alpha * l[i]
        if (sum > max_sum):
            max_sum = sum
            main_direction = base_angle

    return main_direction

def ChangeSingleToList(X,Y):
    WholeList=[]
    for i in range(0,len(X)):
        WholeList.append([X[i],Y[i]])
    return WholeList

def is_in_poly(p, poly):     #-------------------------------用射线法判断点是否在多边形里面---------------------------------
    """
    :param p: [x, y]
    :param poly: [[], [], [], [], ...]
    :return:
    """
    px, py = p
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = not is_in
    return is_in

def GetEveryMidPoint(x,y):     #一个三角形的坐标为[[x0,x1,x2,x0],[y0,y1,y2,y0]]
    """input:线段数据输入如果有一条边的中点在图形内（或者边上）的话，退出循环并且保留此三角形，如果有一条边不在图形内的话，退出循环并删除此三角形。
    output:输出该线段的中点(x0,y0)
    """
    mid_x = []
    mid_y = []
    mid_x.append((x[0] + x[1]) / 2)
    mid_x.append((x[1] + x[2]) / 2)
    mid_x.append((x[0] + x[2]) / 2)

    mid_y.append((y[0] + y[1]) / 2)
    mid_y.append((y[1] + y[2]) / 2)
    mid_y.append((y[0] + y[2]) / 2)

    return mid_x,mid_y

# def getCircle(x1,y1,x2,y2,x3,y3):                          #已知三点坐标，求外接圆的圆心和半径。(x1,y1),(x2,y2),(x3,y3)
#     """
#     :return:  x0 and y0 is center of a circle, r is radius of a circle
#     """
#     a = x1 - x2
#     b = y1 - y2
#     c = x1 - x3
#     d = y1 - y3
#     a1 = ((x1 * x1 - x2 * x2) + (y1 * y1 - y2 * y2)) / 2.0
#     a2 = ((x1 * x1 - x3 * x3) + (y1 * y1 - y3 * y3)) / 2.0
#     theta = b * c - a * d
#     if (abs(theta) < 1e-9):
#         # raise RuntimeError('There should be three different x & y !')
#         # raise RuntimeError([[x1,y1],[x2,y2],[x3,y3]])
#         return False
#     x0 = (b * a2 - d * a1) / theta
#     y0 = (c * a1 - a * a2) / theta
#     # r = np.sqrt(pow((x1 - x0), 2) + pow((y1 - y0), 2))
#     return x0, y0

def cul_dis(x1,y1,x2,y2):
    return math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))

def get_inner_circle(x1,y1,x2,y2,x3,y3):
    #A=(x1,y1)
    #B=(x2,y2)
    #C=(x3,y3)
    a=cul_dis(x2, y2, x3, y3)
    b=cul_dis(x1, y1, x3, y3)
    c=cul_dis(x1, y1, x2, y2)
    # dis(B,C)=a
    # dis(A,C)=b
    # dis(A,B)=c
    #
    in_x=(a*x1+b*x2+c*x3)/(a+b+c)
    in_y=(a*y1+b*y2+c*y3)/(a+b+c)

    return in_x,in_y

def Get_tri_net(tri,poly):
    """input:输入delaunay的所有三角形，格式大概为[[[x1,x2,x3,x1],[y1,y2,y3,y1]],[[x1,x2,x3,x1],[y1,y2,y3,y1]]....]
       output:输出完整的“图形内”三角网
    """
    circle_x0=[]
    circle_y0=[]
    circle_r=[]
    TheLastIndex=[]
    for i in range(0,len(tri)):
        x_1=tri[i][0][0]
        y_1=tri[i][1][0]
        x_2=tri[i][0][1]
        y_2=tri[i][1][1]
        x_3=tri[i][0][2]
        y_3=tri[i][1][2]
        # print("------------begin-----------")
        # print("x",x_1,x_2,x_3,"y",y_1,y_2,y_3)
        # if(getCircle(x_1,y_1,x_2,y_2,x_3,y_3)==False):
        #     continue
        # else:
        x0,y0=get_inner_circle(x_1,y_1,x_2,y_2,x_3,y_3)       # temp_triangles[i1][0][0],temp_triangles[i1][0][1],temp_triangles[i1][0][2],第 i 个三角形的 x 值的第1，2，3点
        circle_x0.append(x0)
        circle_y0.append(y0)
        # circle_r.append(r)
    for i1 in range(0,len(circle_x0)):
        if is_in_poly([circle_x0[i1],circle_y0[i1]], poly) is False:
            TheLastIndex.append(i1)
    # print("TheLastIndex:",TheLastIndex)
    TheLastIndex=set(TheLastIndex)
    a=[i for i in range(0,len(tri))]
    a=set(a)
    b=list(a - TheLastIndex)
    tri=[tri[i] for i in b]

    return tri

def GetTrianglesXY(numberArray,pointX,pointY):#---------------------根据三角形的编号确定三角形的坐标点------------------------
    triangles=[]
    for i in range(0,len(numberArray)):
        triangles.append([[pointX[numberArray[i][0]],pointX[numberArray[i][1]],pointX[numberArray[i][2]],pointX[numberArray[i][0]]],[pointY[numberArray[i][0]],pointY[numberArray[i][1]],pointY[numberArray[i][2]],pointY[numberArray[i][0]]]])
    return triangles
                                                                                                  #---------------------
# def JiaMiNode(X,Y,value):
#     new_x=[]
#     new_y=[]
#     for i in range (0,len(X)-1):
#         if ((X[i] < X[i + 1]) and (Y[i] < Y[i + 1])):
#             "CASE1"
#             dis=math.sqrt(pow((X[i+1]-X[i]),2)+pow((Y[i+1]-Y[i]),2))
#             cos_angle=(X[i+1]-X[i])/dis
#             sin_angle=(Y[i+1]-Y[i])/dis
#             n=dis/value    #取步长为2进行逐个选取
#             n = int(n)
#             for i0 in range(0,n):
#                 new_x.append(X[i]+value*cos_angle*i0)
#                 new_y.append(Y[i]+value*sin_angle*i0)
#         elif ((X[i] < X[i + 1]) and (Y[i] > Y[i + 1])):
#             "CASE2"
#             dis = math.sqrt(pow((X[i + 1] - X[i]), 2) + pow((Y[i] - Y[i+1]), 2))
#             cos_angle = (X[i+1] - X[i]) / dis
#             sin_angle = (Y[i] - Y[i+1]) / dis
#             n = dis / value   # 取步长为2进行逐个选取
#             n=int(n)
#             for i1 in range(0, n):
#                 new_x.append(X[i] + value  * cos_angle * i1)
#                 new_y.append(Y[i] - value  * sin_angle * i1)
#
#         elif ((X[i] > X[i + 1]) and (Y[i] < Y[i + 1])):
#             "CASE3"
#             dis = math.sqrt(pow((X[i] - X[i+1]), 2) + pow((Y[i+1] - Y[i]), 2))
#             cos_angle = (X[i] - X[i+1]) / dis
#             sin_angle = (Y[i+1] - Y[i]) / dis
#             n = dis / value   # 取步长为2进行逐个选取
#             n = int(n)
#             for i2 in range(0, n):
#                 new_x.append(X[i] - value  * cos_angle * i2)
#                 new_y.append(Y[i] + value  * sin_angle * i2)
#
#         elif ((X[i] > X[i + 1]) and (Y[i] > Y[i + 1])):
#             "CASE4"
#             dis = math.sqrt(pow((X[i] - X[i + 1]), 2) + pow((Y[i] - Y[i + 1]), 2))
#             cos_angle = (X[i] - X[i + 1]) / dis
#             sin_angle = (Y[i] - Y[i + 1]) / dis
#             n = dis / value   # 取步长为2进行逐个选取
#             n = int(n)
#             for i3 in range(0, n):
#                 new_x.append(X[i] - value  * cos_angle * i3)
#                 new_y.append(Y[i] - value  * sin_angle * i3)
#
#     return new_x,new_y

def JiaMiNode(X, Y, value):
    new_x = []
    new_y = []
    start_dis = 0
    for i in range(0, len(X) - 1):
        if ((X[i] < X[i + 1]) and (Y[i] < Y[i + 1])):
            "CASE1"
            dis = math.sqrt(pow((X[i + 1] - X[i]), 2) + pow((Y[i + 1] - Y[i]), 2))
            cos_angle = (X[i + 1] - X[i]) / dis
            sin_angle = (Y[i + 1] - Y[i]) / dis  # 角度计算
            current_x = X[i] + start_dis * cos_angle
            current_y = Y[i] + start_dis * sin_angle

            while ((current_x < X[i + 1]) and (current_y < Y[i + 1])):  # 如果超过线段的另一个端点
                new_x.append(current_x)
                new_y.append(current_y)
                current_x = current_x + value * cos_angle
                current_y = current_y + value * sin_angle
            new_x.append(X[i + 1])
            new_y.append(Y[i + 1])
            start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))
        # -----------------------------------------------------------------------------------------------------------------------
        elif ((X[i] < X[i + 1]) and (Y[i] > Y[i + 1])):
            "CASE2"
            dis = math.sqrt(pow((X[i + 1] - X[i]), 2) + pow((Y[i] - Y[i + 1]), 2))
            cos_angle = (X[i + 1] - X[i]) / dis
            sin_angle = (Y[i] - Y[i + 1]) / dis
            current_x = X[i] + start_dis * cos_angle
            current_y = Y[i] - start_dis * sin_angle

            while ((current_x < X[i + 1]) and (current_y > Y[i + 1])):  # 如果超过线段的另一个端点
                new_x.append(current_x)
                new_y.append(current_y)
                current_x = current_x + value * cos_angle
                current_y = current_y - value * sin_angle
            new_x.append(X[i + 1])
            new_y.append(Y[i + 1])
            start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))
        # -----------------------------------------------------------------------------------------------------------------------
        elif ((X[i] > X[i + 1]) and (Y[i] < Y[i + 1])):
            "CASE3"
            dis = math.sqrt(pow((X[i] - X[i + 1]), 2) + pow((Y[i + 1] - Y[i]), 2))
            cos_angle = (X[i] - X[i + 1]) / dis
            sin_angle = (Y[i + 1] - Y[i]) / dis
            current_x = X[i] - value * cos_angle
            current_y = Y[i] + value * sin_angle

            while ((current_x > X[i + 1]) and (current_y < Y[i + 1])):  # 如果没有超过线段的另一个端点
                new_x.append(current_x)
                new_y.append(current_y)
                current_x = current_x - value * cos_angle
                current_y = current_y + value * sin_angle
            new_x.append(X[i + 1])
            new_y.append(Y[i + 1])
            start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))
        # -----------------------------------------------------------------------------------------------------------------------
        elif ((X[i] > X[i + 1]) and (Y[i] > Y[i + 1])):
            "CASE4"
            dis = math.sqrt(pow((X[i] - X[i + 1]), 2) + pow((Y[i] - Y[i + 1]), 2))
            cos_angle = (X[i] - X[i + 1]) / dis
            sin_angle = (Y[i] - Y[i + 1]) / dis
            current_x = X[i] - value * cos_angle
            current_y = Y[i] - value * sin_angle

            while ((current_x > X[i + 1]) and (current_y > Y[i + 1])):  # 如果没有超过线段的另一个端点
                new_x.append(current_x)
                new_y.append(current_y)
                current_x = current_x - value * cos_angle
                current_y = current_y - value * sin_angle
            new_x.append(X[i + 1])
            new_y.append(Y[i + 1])
            start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))

    return new_x, new_y

#-------------------------------------------------------得出正确的三角形---------------------------------------------------
def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

def get_net_in_circle(x1,y1,x2,y2,x3,y3):
    A=distance(x2,y2,x3,y3)
    B=distance(x1,y1,x3,y3)
    C=distance(x1,y1,x2,y2)
    S=A+B+C
    x=(A*x1+B*x2+C*x3)/S
    y=(A*y1+B*y2+C*y3)/S
    return x,y

def ZeroLaterSix(Strlist):
    """
    :param Strlist: [x1,x2,x3,x4....]  小数点后位数 > 6   List
    :return: [x1,x2,x3,x4]  (小数点后六位)  List
    """
    n=len(Strlist)
    Newstr=[]
    for i in range(0,n):
        s1=Strlist[i]
        s1=str(s1)
        s1_list = s1.split('.')
        s1_new = s1_list[0] + '.' + s1_list[1][:6]                   #取小数点的后六位
        s1_new=float(s1_new)
        Newstr.append(s1_new)
    return Newstr

def GetTriangles(poly):  # [[x1,y1],[x2,y2]...]
    k_set = []
    for i,item in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = item
        x2, y2 = poly[next_i]
        k_set.append(abs((y1 - y2) / (x1 - x2)))
    return k_set

def x_y_transverse(x,y):#[x1,x2,x3....],[y1,y2,y3,y4...]变为：[[x1,y1],[x2,y2],[x3,y3]...]
    new_point_list=[]
    for i in range(len(x)):
        new_point_list.append([x[i],y[i]])
    return new_point_list

def XYTransverse(Pointlist):
    X=[]
    Y=[]
    for i in range(0,len(Pointlist)):
        X.append(Pointlist[i][0])
        Y.append(Pointlist[i][1])
    return X,Y

def GetTriangles(poly):  # [[x1,y1],[x2,y2]...]
    k_set = []
    for i,item in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = item
        x2, y2 = poly[next_i]
        k_set.append(abs((y1 - y2) / (x1 - x2)))
    return k_set

def search_k_b(x_list,y_list):
    k_list=[]
    b_list=[]
    for i in range(0,len(x_list)-1):
        k=((y_list[i+1]-y_list[i])/(x_list[i+1]-x_list[i]))
        k_list.append(k)
        b=y_list[i+1]-k*x_list[i+1]
        b_list.append(b)
    # print("k_list",k_list)
    # print("b_list",b_list)
    return k_list,b_list

def TwoPointsDistance(x1,y1,x2,y2,x3,y3):
    """用于第一类三角网的筛选和提取
    :param x1:六个点之间的距离都计算一下
    :param y1:
    :param x2:
    :param y2:
    :param x3:
    :param y3:
    :return: 相距最近的两个点
    """
    dis1=math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))
    dis2=math.sqrt(pow(x2-x3,2)+pow(y2-y3,2))
    dis3=math.sqrt(pow(x1-x3,2)+pow(y1-y3,2))
    if (dis1==min(dis1,dis2,dis3)):
        x=x1
        y=y1
        x_next=x2
        y_next=y2
    elif(dis2==min(dis1,dis2,dis3)):
        x =x2
        y =y2
        x_next =x3
        y_next =y3
    elif(dis3==min(dis1,dis2,dis3)):
        x =x1
        y =y1
        x_next =x3
        y_next =y3

    return x,y,x_next,y_next

def YDirectionReflaction(PointList):#
    """
    :param PointList: PointList=[[x1,y1],[x2,y2],[x3,y3]...]
    :return: PointList=[[x1,y1],[x2,y2],[x3,y3]...](按照升序排列)
    """
    if len(PointList) < 2:
        return PointList

    else:
        flag = PointList[0][1]
        less = []
        greater = []
        for i in PointList[1:]:
            if i[1] <= flag:
                less.append(i)   #i:[x1,y1]
            else:
                greater.append(i)
        return YDirectionReflaction(less)+[[PointList[0][0],flag]]+YDirectionReflaction(greater)

def XDirectionReflaction(PointList):#
    """
    :param PointList: PointList=[[x1,y1],[x2,y2],[x3,y3]...]
    :return: PointList=[[x1,y1],[x2,y2],[x3,y3]...](按照升序排列)
    """
    if len(PointList) < 2:
        return PointList

    else:
        flag = PointList[0][0]
        less = []
        greater = []
        for i in PointList[1:]:
            if i[0] <= flag:
                less.append(i)   #i:[x1,y1]
            else:
                greater.append(i)
        return XDirectionReflaction(less)+[[flag,PointList[0][1]]]+XDirectionReflaction(greater)

def Srotate(angle,valuex,valuey,pointx,pointy):                                                       #get array Srotate
    valuex = np.array(valuex)
    valuey = np.array(valuey)
    a = []
    b = []
    for i in range(0, len(valuex)):
        sRotatex = (valuex[i]-pointx)*math.cos(angle) + (valuey[i]-pointy)*math.sin(angle) + pointx
        sRotatey = (valuey[i]-pointy)*math.cos(angle) - (valuex[i]-pointx)*math.sin(angle) + pointy
        a.append(sRotatex)
        b.append(sRotatey)
    return a,b

#图形（多边形）
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class Line:
    def __init__(self, p1, p2):
        self.x = p1.getX() - p2.getX()
        self.y = p1.getY() - p2.getY()
        self.coor = [[p1.getX(), p1.getY()], [p2.getX(), p2.getY()]]                  #[[x1,y1],[x2,y2]]
        self.line = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def getLen(self):
        return self.line

#--------------------获取第三类三角形---------------------------------
def get_line_function(poly,line,value):
    """
    :param poly:  poly=[[x1,y1],[x2,y2],[x3,y3],[x4,y4],.....[xn,yn],[x1,y1]]
    :param line:[[x1,y1],[x2,y2]]
    :return:   判断单条线是否在多边形上.
    """
    a=0
    k = []
    b = []
    # print("3333333333",len(poly))
    for i in range(0, len(poly)-1):
        x1 = poly[i][0]
        y1 = poly[i][1]
        x2 = poly[i + 1][0]
        y2 = poly[i + 1][1]
        if(x1==x2):
            if (round(line.coor[0][0],value)==x1 and round(line.coor[1][0],value)==x1) and ((y1<round(line.coor[0][1],value)<y2 and y1<round(line.coor[1][1],value)<y2) or (y2<round(line.coor[0][1],value)<y1 and y2<round(line.coor[1][1],value)<y1)):
                a=1
        elif(y1==y2):
            if (round(line.coor[0][1],value)==y1 and round(line.coor[1][1],value)==y1) and ((x1<round(line.coor[0][0],value)<x2 and x1<round(line.coor[1][0],value)<x2) or (x2<round(line.coor[0][0],value)<x1 and x2<round(line.coor[1][0],value)<x1)):
                a=1
        else:
            k_item=(y1 - y2) / (x1 - x2)
            b=y1-k_item*x1
            if (round(line.coor[0][1],value)==round(k_item*line.coor[0][0]+b,value))and (round(line.coor[1][1],value)==round(k_item*line.coor[1][0]+b,value)):
                a=1
    return a

def get_three_kind_triangels(triangle_array,poly,value):
    """
    :param triangle_array:[[[x1,x2,x3,x1],[y1,y2,y3,y1]],[[x1,x2,x3,x1],[y1,y2,y3,y1]]....]
    :poly:[[x1,y1],[x2,y2],[x3,y3],...[xn,yn],[x1,y1]]
    :return:
    """
    one_kind_triangles = []
    second_kind_triangles = []
    Three_kind_triangles=[]
    item=0
    for i in range (0,len(triangle_array)):                                          # 遍历每一个三角形
        p1=Point(triangle_array[i][0][0], triangle_array[i][1][0])
        p2=Point(triangle_array[i][0][1], triangle_array[i][1][1])
        p3=Point(triangle_array[i][0][2], triangle_array[i][1][2])
        p4=Point(triangle_array[i][0][3], triangle_array[i][1][3])

        line1 = Line(p1, p2)            #Dealaunay三角形的第一条边
        line2 = Line(p2, p3)            #Dealaunay三角形的第二条边
        line3 = Line(p3, p4)            #Dealaunay三角形的第二条边

        if (get_line_function(poly,line1,value) == False) and (get_line_function(poly,line2,value) == False) and (get_line_function(poly,line3,value) == False):
            Three_kind_triangles.append(triangle_array[i])                     #将第三类三角形放在三角形数组当中。

    return Three_kind_triangles
            #一条线在多边形上的条件。
#一条线上的两个点(x1,y1),(x2,y2)都在这个多边形上。
#(x1,y1)符合这个条件。
#------------------------判断单条线是否在多边形上。

def x_y_transverse(poly):  #[[x1,y1],[x2,y2],[x3,y3]...] 变为： [x1,x2,x3....],[y1,y2,y3,y4...]
    new_point_listx = []
    new_point_listy = []
    for i in range(len(poly)):
        new_point_listx.append(poly[i][0])
        new_point_listy.append(poly[i][1])
    return new_point_listx,new_point_listy

#----------------------get_third_Tri_shape_heart------------------------
def Get_shape_in_heart(Third_Tri_array):
    """
    :param Third_Tri_array:[[[x1,x2,x3,x1],[y1,y2,y3,y1]],....]
    :return:shape_heart=[[x01,y01],[x02,y02],....]
    """
    shape_heart=[]
    for i in range(0,len(Third_Tri_array)):
        x0,y0 = get_net_in_circle(Third_Tri_array[i][0][0], Third_Tri_array[i][1][0], Third_Tri_array[i][0][1], Third_Tri_array[i][1][1], Third_Tri_array[i][0][2], Third_Tri_array[i][1][2])
        shape_heart.append([x0,y0])

    return shape_heart
#------------------------------------------------生成第三类三角网----------------------------------------------------
#-----------------------------------------input-----------------------------------------
# a=process_data('F:/00000000第二篇论文00000000000/experiencement_data/4/U_500.json')
# #-------传入参数--------
triInNet=[]   #----------------------所有的三角网------------------------
third_tri_array=[]   #--------------------第三类三角形的集合-----------------------

polygon=[[[35386081.61814474, 3995477.795727629], [35386132.71051825, 3995439.79529537], [35386122.33227237, 3995425.9568432122], [35386093.752267756, 3995447.216244752], [35386074.682625, 3995421.792751719], [35386105.555719525, 3995398.8164684186], [35386094.74652042, 3995384.4065129547], [35386039.53168866, 3995425.479643049], [35386050.074949324, 3995439.5267324303], [35386060.59495264, 3995431.6984685436], [35386078.84865355, 3995456.033763956], [35386070.148758665, 3995462.4953871155], [35386081.61814474, 3995477.795727629]], [[35406579.41204409, 3985881.650648137], [35406590.98105711, 3985878.1539736995], [35406598.97354321, 3985902.1510742567], [35406626.93708724, 3985892.698317018], [35406598.47269971, 3985809.201928573], [35406570.5230036, 3985819.1318224943], [35406577.49438894, 3985837.835051281], [35406565.45893394, 3985843.267703369], [35406544.25723277, 3985805.9273557374], [35406525.48569747, 3985814.7943011164], [35406548.14044858, 3985853.0846564816], [35406561.12880449, 3985891.477833317], [35406565.41176131, 3985930.44077762], [35406586.675163135, 3985927.806535586], [35406579.41204409, 3985881.650648137]], [[35394375.21712177, 3990415.5536773303], [35394402.12514579, 3990399.9474916263], [35394402.76924838, 3990401.0384726133], [35394401.17581789, 3990401.9566086563], [35394410.16753713, 3990417.3416378703], [35394421.455264136, 3990410.7910127346], [35394417.5530119, 3990404.112393047], [35394419.29859004, 3990403.1036431235], [35394414.20913828, 3990394.3972215056], [35394415.84736758, 3990393.456352341], [35394403.49658851, 3990372.34062106], [35394390.41844702, 3990379.9227590146], [35394394.34830226, 3990386.6454285155], [35394367.44011578, 3990402.240540439], [35394364.80800827, 3990397.744117372], [35394352.159603655, 3990405.0769796036], [35394366.97700024, 3990430.413599864], [35394379.616499946, 3990423.091963328], [35394375.21712177, 3990415.5536773303]], [[35385823.63710699, 3998169.8274588706], [35385861.00509376, 3998147.075879917], [35385861.511213645, 3998147.9016920715], [35385889.31837137, 3998130.9686084753], [35385878.34074135, 3998113.0983349173], [35385850.53354504, 3998130.031452062], [35385851.536638945, 3998131.672095735], [35385843.40529467, 3998136.617222751], [35385838.91611999, 3998129.4060400054], [35385842.41934148, 3998128.694422693], [35385840.91589518, 3998123.908239736], [35385844.447758, 3998122.6302098525], [35385839.64046226, 3998106.9103784147], [35385832.7717152, 3998091.961056554], [35385823.96219042, 3998078.0581453186], [35385813.37715507, 3998065.443668558], [35385801.19088484, 3998054.359533026], [35385797.99012736, 3998056.166003258], [35385793.368959956, 3998053.3405992], [35385791.876829796, 3998054.9471986215], [35385787.304646306, 3998047.5928383814], [35385795.74789033, 3998042.3883197657], [35385796.75986414, 3998044.0177430287], [35385824.48431796, 3998026.9412583336], [35385813.41710668, 3998009.127721719], [35385785.69261496, 3998026.2042401563], [35385786.20775351, 3998027.029930661], [35385748.95909259, 3998049.980033945], [35385759.13408354, 3998066.362290004], [35385763.23506158, 3998063.8337321207], [35385762.60025167, 3998062.809825804], [35385782.488758676, 3998050.552467821], [35385787.89820486, 3998059.261056889], [35385784.0261954, 3998063.46253779], [35385796.21262096, 3998074.557746739], [35385803.028286, 3998082.6708593485], [35385806.79767146, 3998087.1722032633], [35385815.60721571, 3998101.0750978505], [35385819.06476739, 3998108.599394338], [35385822.47584146, 3998116.013310052], [35385827.28330894, 3998131.744229856], [35385832.76282667, 3998130.640570379], [35385838.37462531, 3998139.6795134726], [35385818.287857145, 3998151.9171394682], [35385817.65305968, 3998150.8932293486], [35385813.5426698, 3998153.3885893393], [35385823.63710699, 3998169.8274588706]], [[35389919.350307055, 3993415.710223652], [35389936.93478581, 3993411.715938416], [35389938.77506282, 3993419.77257974], [35389952.13643735, 3993416.741424214], [35389945.81549972, 3993389.1298892964], [35389932.45422382, 3993392.172150189], [35389934.51315384, 3993401.136126652], [35389916.91964494, 3993405.1305293357], [35389914.95511353, 3993396.509426079], [35389901.5666897, 3993399.5409771795], [35389908.10724584, 3993428.126400083], [35389921.49548812, 3993425.0837610597], [35389919.350307055, 3993415.710223652]], [[35384674.55382232, 3997903.1241371203], [35384732.55718671, 3997890.140341075], [35384736.50377412, 3997908.734480661], [35384752.590195835, 3997905.348410876], [35384739.713203005, 3997844.6628361237], [35384723.62667272, 3997848.048926632], [35384728.59140517, 3997871.4576649354], [35384670.01319807, 3997884.5711431685], [35384664.311496094, 3997861.294229012], [35384646.98382769, 3997865.4959335965], [35384661.53861764, 3997924.9606126696], [35384678.86602664, 3997920.747836843], [35384674.55382232, 3997903.1241371203]], [[35389919.350307055, 3993415.710223652], [35389936.93478581, 3993411.715938416], [35389938.77506282, 3993419.77257974], [35389952.13643735, 3993416.741424214], [35389945.81549972, 3993389.1298892964], [35389932.45422382, 3993392.172150189], [35389934.51315384, 3993401.136126652], [35389916.91964494, 3993405.1305293357], [35389914.95511353, 3993396.509426079], [35389901.5666897, 3993399.5409771795], [35389908.10724584, 3993428.126400083], [35389921.49548812, 3993425.0837610597], [35389919.350307055, 3993415.710223652]], [[35389476.48495499, 3994121.9020568985], [35389473.61556925, 3994109.430135923], [35389447.28206424, 3994115.4447166156], [35389446.61518868, 3994112.578594519], [35389450.00231593, 3994111.8033664073], [35389443.77754557, 3994084.7680376857], [35389461.78250763, 3994080.6564497706], [35389459.40912623, 3994070.364698735], [35389416.25637365, 3994080.209639162], [35389418.629804015, 3994090.5013798056], [35389431.495621994, 3994087.564425223], [35389437.71156002, 3994114.6109566567], [35389443.14712164, 3994113.3659434803], [35389443.80498938, 3994116.2321789665], [35389419.286423154, 3994121.835502266], [35389422.15574362, 3994134.296310604], [35389476.48495499, 3994121.9020568985]], [[35386672.24144894, 3994690.949503588], [35386665.828097105, 3994661.820602205], [35386658.514610946, 3994663.4135157033], [35386654.64757463, 3994645.860954397], [35386661.97008347, 3994644.267921547], [35386655.29779803, 3994613.932615359], [35386620.841732934, 3994621.448213304], [35386627.42760291, 3994651.362864247], [35386637.58916284, 3994649.1448499816], [35386641.55248905, 3994667.173404702], [35386631.39080586, 3994669.3803180372], [35386637.79468618, 3994698.4649262507], [35386672.24144894, 3994690.949503588]], [[35381204.93931176, 4000727.772541566], [35381225.350222446, 4000713.765751644], [35381220.26225084, 4000706.420656531], [35381205.855189025, 4000716.316936876], [35381198.92110108, 4000706.2998492923], [35381207.297741264, 4000700.547731235], [35381201.67705862, 4000692.4329452226], [35381182.729251325, 4000705.4431924466], [35381188.34094195, 4000713.558088969], [35381195.138623446, 4000708.8929212685], [35381202.07271394, 4000718.9100059494], [35381199.85148081, 4000720.438554989], [35381199.64935954, 4000720.14162496], [35381192.896395005, 4000724.7839838555], [35381200.46429851, 4000735.7247811225], [35381207.226260394, 4000731.0823056162], [35381204.93931176, 4000727.772541566]], [[35376358.2358304, 3996079.733016679], [35376396.2022211, 3996063.9357222253], [35376400.53700062, 3996074.252358774], [35376411.91169787, 3996069.518973128], [35376397.573444344, 3996035.335794659], [35376386.18970142, 3996040.069324807], [35376391.074723445, 3996051.710102837], [35376353.1082869, 3996067.507418064], [35376348.22337789, 3996055.8777568736], [35376337.66365459, 3996060.2667426425], [35376352.010960914, 3996094.4386052545], [35376362.56164134, 3996090.0497627975], [35376358.2358304, 3996079.733016679]], [[35386081.61814474, 3995477.795727629], [35386132.71051825, 3995439.79529537], [35386122.33227237, 3995425.9568432122], [35386093.752267756, 3995447.216244752], [35386074.682625, 3995421.792751719], [35386105.555719525, 3995398.8164684186], [35386094.74652042, 3995384.4065129547], [35386039.53168866, 3995425.479643049], [35386050.074949324, 3995439.5267324303], [35386060.59495264, 3995431.6984685436], [35386078.84865355, 3995456.033763956], [35386070.148758665, 3995462.4953871155], [35386081.61814474, 3995477.795727629]], [[35394375.21712177, 3990415.5536773303], [35394402.12514579, 3990399.9474916263], [35394402.76924838, 3990401.0384726133], [35394401.17581789, 3990401.9566086563], [35394410.16753713, 3990417.3416378703], [35394421.455264136, 3990410.7910127346], [35394417.5530119, 3990404.112393047], [35394419.29859004, 3990403.1036431235], [35394414.20913828, 3990394.3972215056], [35394415.84736758, 3990393.456352341], [35394403.49658851, 3990372.34062106], [35394390.41844702, 3990379.9227590146], [35394394.34830226, 3990386.6454285155], [35394367.44011578, 3990402.240540439], [35394364.80800827, 3990397.744117372], [35394352.159603655, 3990405.0769796036], [35394366.97700024, 3990430.413599864], [35394379.616499946, 3990423.091963328], [35394375.21712177, 3990415.5536773303]], [[35385823.63710699, 3998169.8274588706], [35385861.00509376, 3998147.075879917], [35385861.511213645, 3998147.9016920715], [35385889.31837137, 3998130.9686084753], [35385878.34074135, 3998113.0983349173], [35385850.53354504, 3998130.031452062], [35385851.536638945, 3998131.672095735], [35385843.40529467, 3998136.617222751], [35385838.91611999, 3998129.4060400054], [35385842.41934148, 3998128.694422693], [35385840.91589518, 3998123.908239736], [35385844.447758, 3998122.6302098525], [35385839.64046226, 3998106.9103784147], [35385832.7717152, 3998091.961056554], [35385823.96219042, 3998078.0581453186], [35385813.37715507, 3998065.443668558], [35385801.19088484, 3998054.359533026], [35385797.99012736, 3998056.166003258], [35385793.368959956, 3998053.3405992], [35385791.876829796, 3998054.9471986215], [35385787.304646306, 3998047.5928383814], [35385795.74789033, 3998042.3883197657], [35385796.75986414, 3998044.0177430287], [35385824.48431796, 3998026.9412583336], [35385813.41710668, 3998009.127721719], [35385785.69261496, 3998026.2042401563], [35385786.20775351, 3998027.029930661], [35385748.95909259, 3998049.980033945], [35385759.13408354, 3998066.362290004], [35385763.23506158, 3998063.8337321207], [35385762.60025167, 3998062.809825804], [35385782.488758676, 3998050.552467821], [35385787.89820486, 3998059.261056889], [35385784.0261954, 3998063.46253779], [35385796.21262096, 3998074.557746739], [35385803.028286, 3998082.6708593485], [35385806.79767146, 3998087.1722032633], [35385815.60721571, 3998101.0750978505], [35385819.06476739, 3998108.599394338], [35385822.47584146, 3998116.013310052], [35385827.28330894, 3998131.744229856], [35385832.76282667, 3998130.640570379], [35385838.37462531, 3998139.6795134726], [35385818.287857145, 3998151.9171394682], [35385817.65305968, 3998150.8932293486], [35385813.5426698, 3998153.3885893393], [35385823.63710699, 3998169.8274588706]]]

print(polygon[1])

for i in range (0,len(polygon)):
    n=len(polygon)
    poly=polygon[i]
    #poly=[[x1,y1],[x2,y2],[x3,y3],...,[x1,y1]]
    point_list=np.array(poly)
    point_x_list=point_list.T[0]
    point_y_list=point_list.T[1]

    #---------------转化为列表-------------------
    point_x_list.tolist()
    # print("--------------------",point_x_list)
    point_y_list.tolist()

    # #---------------加密节点---------------------
    aX,aY=JiaMiNode(point_x_list,point_y_list,2)   #加密节点
    plt.plot(aX,aY, 'o', linewidth=1.0, color='black')
    # #--------------生成三角网---------------------
    # print("==============================================",aX)
    NL=[]
    for i in range(0,len(aX)):
        NL.append([aX[i],aY[i]])
    # print(NL)
    points =np.array(NL)

    tri = Delaunay(points)
    z=tri.simplices
    a_list=z.tolist()
    TrianglesT=GetTrianglesXY(a_list,aX,aY)         #得到三角网
    #----------------改参数2-----------------
    tri_in=Get_tri_net(TrianglesT,poly)              #得到图形内三角网               #len(a)=71
    triInNet.append(tri_in)
    for i12 in range(0, len(tri_in)):
        plt.plot(tri_in[i12][0],tri_in[i12][1], color='green', linewidth=1.0, linestyle='-')
    a3=get_three_kind_triangels(tri_in,poly,3)
    third_tri_array.append(a3)
    for i1 in range(0, len(a3)):
        plt.plot(a3[i1][0],a3[i1][1], color='red', linewidth=1.0, linestyle='-')
    poly=np.array(poly)
    plt.plot(poly.T[0],poly.T[1], color='black', linewidth=1.0, linestyle='-')
    AAAA=Get_shape_in_heart(a3)
    point_x_list=np.array(point_x_list)
    point_y_list=np.array(point_y_list)
# for i1 in range(0, len(AAAA)):
    plt.show()


print(triInNet)
print("----------------",third_tri_array)
# ----------------------------------------------------------------------------------------------------------------------
plt.plot(point_x_list,point_y_list, color='green', linewidth=1.0, linestyle='-')
# -------------------------三角形内切圆-------------------------
