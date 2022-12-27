
#--------------质心---------------
def cal_area(vertices): #Gauss's area formula 高斯面积计算
    #按逆时针输入点，封闭图形
    A = 0.0
    point_p = vertices[-1]
    for point in vertices:
        A += (point[1]*point_p[0] - point[0]*point_p[1])
        point_p = point
    return abs(A)/2

def cal_centroid(points):
    #points=[[x1,y1],[x2,y2],...,[xn,yn],[x1,y1]]
    A = cal_area(points)
    c_x, c_y = 0.0, 0.0
    point_p = points[-1] # point_p 表示前一节点
    for point in points:
        c_x +=((point[0] + point_p[0]) * (point[1]*point_p[0] - point_p[1]*point[0]))
        c_y +=((point[1] + point_p[1]) * (point[1]*point_p[0] - point_p[1]*point[0]))
        point_p = point

    return c_x / (6*A), c_y / (6*A)


# x0,y0=cal_centroid(points)
# #[[x1,y1],[x2,y2],[x3,y3],...,[xn,yn]]
# x,y=[],[]
# list=[[[x1,y1],[],],[],[],]
# for i in range(0,len(list)):
#     if(list[i][0]==list[i][-1]):
#         x0, y0 = cal_centroid(list[i]):
#         x.append(x0)
#         y.append(y0)

