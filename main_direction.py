#main_direction

import math
import numpy as np

def distance(x1,y1,x2,y2):
    return math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))

def get_main_direction(point_set):
    """
    :param point_set:[[x1,y1],[x2,y2],[x3,y3],[x4,y4]...,[xn,yn],[x1,y1]]
    :return: direction
    """
    # 对点集分离横纵坐标
    x = []
    y = []
    for i in range(len(point_set)):
        x.append(point_set[i][0])
        y.append(point_set[i][1])

    angle = []
    l = []

    n = len(x)                           #输入的所有点的长度
    for i in range(n - 1):               #计算所有边与x正方向的夹角并存到“angle”当中。
        # 找出第i条边的两个端点(x1, y1), (x2, y2)
        x1 = x[i]
        y1 = y[i]
        x2 = x[i + 1]
        y2 = y[i + 1]
        # 求解第i个线段的模
        l.append(distance(x1,y1,x2,y2))
        # 求解第i个线段的角度
        if(x1<x2 and y1<y2):
            angle.append(math.atan((y2 - y1) / (x2 - x1)) / (2 * 3.141592653589793238) * 360)
        elif(x2<x1 and y2<y1):
            angle.append(math.atan((y1 - y2) / (x1 - x2)) / (2 * 3.141592653589793238) * 360)
        elif(x1>x2 and y1<y2):
            angle.append(math.atan(abs(x1 - x2) / abs(y2 - y1)) / (2 * 3.141592653589793238) * 360)
        elif(x1==x2):
            angle.append(90)
        elif(y1==y2):
            angle.append(0)
        else:
            angle.append(math.atan(abs(x2 - x1) / abs(y1 - y2)) / (2 * 3.141592653589793238) * 360)

    # 规定步长为1°
    step = 1
    # 规定偏差系数alpha
    alpha = 10
    # 初始化最大的加权和
    max_sum = -1
    # 初始化主方向
    main_direction = -1

    for choose_angle in np.arange(0, 91, step):              #选定一个候选方向用于后续计算
        print("-----------",choose_angle)
        conbribute_L = 0.0
        for i in range(n-1):                               #边数为n-1，遍历每一条边
            # 当前边在[choose_angle - alpha,choose_angle + alpha]范围内
            if (choose_angle - alpha <= angle[i]  <= choose_angle + alpha):
                conbribute_L = conbribute_L + ((alpha - abs(choose_angle - angle[i])) / alpha )* l[i]

        if (conbribute_L > max_sum):
            max_sum = conbribute_L
            main_direction = choose_angle

    return main_direction

test=[[0,0],[0,5],[9,8],[9,3],[0,0]]
aaaa=get_main_direction(test)
print(":---------",aaaa)
