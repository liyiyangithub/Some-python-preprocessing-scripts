import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import math
#
# #骨架线：
# #第一条线
# x1=[14.339860557359964, 14.151974491300823, 13.953630295906272, 13.75529090490065, 13.5569467095061, 13.358607318500479, 13.160263123105931, 12.96192373210031, 12.763579536705759, 12.565240145700137, 12.366895950305588, 12.168556559299967, 11.970212363905418, 11.771872972899796, 11.573528777505246, 11.375189386499624, 11.176845191105077, 10.978505800099455, 10.780161604704904, 10.581822213699283, 10.383478018304734, 10.185138627299112, 9.986794431904563, 9.788455040898942, 9.507254984002005, 9.308915592996383, 9.110576201990762, 8.91223681098514, 8.713897419979517, 8.095465004522117]
# y1= [48.32645790510927, 46.23304616824072, 45.2529137383348, 44.27278033620246, 43.29264790629654, 42.31251450416419, 41.33238207425827, 40.35224867212593, 39.37211624222001, 38.391982840087664, 37.41185041018174, 36.431717008049404, 35.45158457814348, 34.47145117601113, 33.49131874610521, 32.51118534397287, 31.531052914066947, 30.550919511934605, 29.57078708202868, 28.59065367989634, 27.61052124999042, 26.630387847858074, 25.650255417952152, 24.670122015819814, 23.280551252189326, 22.300417850056984, 21.320284447924642, 20.3401510457923, 19.36001764365996, 15.795458917416388]
# #第二条线
# x2=[8.095465004522117, 11.349839942760688, 12.33025100451328, 13.31066206626587, 14.29107312801846, 15.271484189771051, 16.251867360527573, 17.232278422280164, 18.212661593036685, 19.193072654789276, 20.1734558255458, 21.153866887298392, 22.13425005805491, 23.1146611198075, 24.095044290564026, 25.075455352316617, 26.055838523073138, 27.03624958482573, 28.01663275558225, 28.99704381733484, 29.977426988091363, 30.957838049843954, 31.93822122060048, 32.91863228235307, 33.899015453109584, 34.879426514862175, 35.8598096856187, 36.84022074737129, 37.853998221445806, 38.8344092831984, 39.81482034495099, 40.79523140670358, 44.36550172544341]
# y2=[15.795458917416388, 14.750545609723757, 14.553583303702638, 14.356620997681517, 14.159658691660399, 13.96269638563928, 13.765595298637232, 13.568632992616113, 13.371531905614065, 13.174569599592946, 12.9774685125909, 12.780506206569779, 12.58340511956773, 12.386442813546612, 12.189341726544564, 11.992379420523445, 11.795278333521397, 11.598316027500278, 11.401214940498232, 11.204252634477111, 11.007151547475065, 10.810189241453944, 10.613088154451896, 10.416125848430777, 10.219024761428729, 10.02206245540761, 9.824961368405564, 9.627999062384443, 9.424184219291934, 9.227221913270816, 9.030259607249697, 8.833297301228578, 8.373450713607268]
# #第三条线
# x3= [44.36550172544341, 45.471553389814815, 45.67002114085746, 45.868488891900114, 46.06695664294277, 46.26542439398541, 46.46402092029245, 46.6624886713351, 46.86108519764213, 47.05955294868478, 47.25814947499182, 47.45661722603447, 47.655213752341496, 47.85368150338415, 48.05227802969118, 48.194347034284625]
# y3=[8.373450713607268, 11.772326846326425, 12.752434264825068, 13.73254168332371, 14.712649101822352, 15.692756520320994, 16.672837853547364, 17.652945272046008, 18.633026605272377, 19.61313402377102, 20.59321535699739, 21.57332277549603, 22.553404108722404, 23.533511527221044, 24.513592860447417, 26.50862891922195]
#
# point_sett=[[15.841079711914062, 20.83474975451827], [39.43706441670656, 16.090896154288203], [42.59558478742838, 31.67831308208406], [55.8723328858614, 29.016120745334774], [49.99668689072132, 0.0], [0.0, 10.04421831574291], [8.83330512046814, 53.695745911449194], [21.957117296755314, 51.05759931914508], [15.841079711914062, 20.83474975451827]]
#
# def x_y_transverse(x,y):#[x1,x2,x3....],[y1,y2,y3,y4...]变为：[[x1,y1],[x2,y2],[x3,y3]...]
#     new_point_list=[]
#     for i in range(len(x)):
#         new_point_list.append([x[i],y[i]])
#     return new_point_list
#
# def distance(a, b):
#     return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
#
# def get_main_direction(point_set):
#     # 对点集分离横纵坐标
#     x = []
#     y = []
#     for i in range(len(point_set)):
#         x.append(point_set[i][0])
#         y.append(point_set[i][1])
#
#     angle = []
#     l = []
#
#     n = len(x)                      # 点集的长度n
#     for i in range(n - 1):
#         # 找出第i条边的两个端点(x1, y1), (x2, y2)
#         x1 = x[i]
#         y1 = y[i]
#         x2 = x[i + 1]
#         y2 = y[i + 1]
#
#         # 求解第i个线段的模
#         l.append(distance([x1, y1], [x2, y2]))
#         # 求解第i个线段的角度
#         if (x1 == x2):
#             angle.append(-90)
#         else:
#             angle.append(math.atan((y2 - y1) / (x2 - x1)) / (2 * 3.1415926) * 360)
#
#     # 规定步长为1°
#     step = 1
#     # 规定偏差系数alpha
#     alpha = 10
#     # 初始化最大的加权和       ？？？？？
#     max_sum = -1
#     # 初始化主方向
#     main_direction = -1
#     for base_angle in np.arange(0, 90, step):
#         sum = 0.0
#         for i in range(n - 1):
#             # 当前边在[base-alpha, base+alpha]范围内
#             if (base_angle - alpha <= angle[i] and angle[i] <= base_angle + alpha):
#                 sum = sum + (alpha - abs(base_angle - angle[i])) / alpha * l[i]
#             # 当前边的垂边在[base-alpha, base+alpha]范围内
#             elif (base_angle - alpha <= angle[i] + 90 and angle[i] + 90 <= base_angle + alpha):
#                 sum = sum + (alpha - abs(base_angle - (angle[i] + 90))) / alpha * l[i]
#             # 当前边在[base-alpha, base+alpha]范围内
#             elif (base_angle - alpha <= angle[i] + 180 and angle[i] + 180 <= base_angle + alpha):
#                 sum = sum + (alpha - abs(base_angle - (angle[i] + 180))) / alpha * l[i]
#         if (sum > max_sum):
#             max_sum = sum
#             main_direction = base_angle
#
#     return main_direction
#
# def Srotate(angle,valuex,valuey,pointx,pointy):               #get array Srotate
#     valuex = np.array(valuex)
#     valuey = np.array(valuey)
#     a = []
#     b = []
#     for i in range(0, len(valuex)):
#         sRotatex = (valuex[i]-pointx)*math.cos(angle) + (valuey[i]-pointy)*math.sin(angle) + pointx
#         sRotatey = (valuey[i]-pointy)*math.cos(angle) - (valuex[i]-pointx)*math.sin(angle) + pointy
#         a.append(sRotatex)
#         b.append(sRotatey)
#     return a,b
#
# def Nrotate(angle,valuex,valuey,pointx,pointy):                 #get array Nratate
#     valuex = np.array(valuex)
#     valuey = np.array(valuey)
#     a=[]
#     b=[]
#     for i in range(0,len(valuex)):
#         nRotatex = (valuex[i]-pointx)*math.cos(angle) - (valuey[i]-pointy)*math.sin(angle) + pointx
#         nRotatey = (valuex[i]-pointx)*math.sin(angle) + (valuey[i]-pointy)*math.cos(angle) + pointy
#         a.append(nRotatex)
#         b.append(nRotatey)
#     return a, b
#
#
# def cosine_similarity(moban_vector_data,true_vector_data):
#     """
#     :param moban_vector_data:[[vector_data_x1,vector_data_y1],[vector_data_x2,vector_data_y2],[vector_data_x3,vector_data_y3],[vector_data_x4,vector_data_y4]...]
#     :param true_vector_data: [[vector_truedata_x1,vector_truedata_y1],[vector_turedata_x2,vector_truedata_y2],[vector_turedata_x3,vector_truedata_y3]...]
#     :return:
#     """
#     # xx = 0.0
#     # yy = 0.0
#     # xy = 0.0
#     # for i in range(len(x)):
#     #     xx += x[i] * x[i]
#     #     yy += y[i] * y[i]
#     #     xy += x[i] * y[i]
#     # xx_sqrt = xx ** 0.5
#     # yy_sqrt = yy ** 0.5
#     # cos = xy/(xx_sqrt*yy_sqrt)*0.5+0.5
#     # return cosv
#     sum_son=0
#     sum_father_1=0
#     sum_father_2=0
#     sum_father=0
#     for i in range(len(moban_vector_data)):
#         sum_son+=(moban_vector_data[i][0]*true_vector_data[i][0]+moban_vector_data[i][1]*true_vector_data[i][1])
#
#     for j in range(len(moban_vector_data)):
#         sum_father_1+=pow(moban_vector_data[j][0],2)+pow(moban_vector_data[j][1],2)
#         sum_father_2+=pow(true_vector_data[j][0],2)+pow(true_vector_data[j][1],2)
#         sum_father=math.sqrt(sum_father_1)*math.sqrt(sum_father_2)
#
#     value=sum_son/sum_father
#     cosine_similarity=0.5*value+0.5
#
#     return cosine_similarity
#
# # a=cosine_similarity(moban_vector_data,true_vector_data)
#
# # print("-----------",a)
# plt.plot(x1[0], y1[0], 'o', linewidth=8.0, color='black')   #向量终点1
# plt.plot(x3[len(x3)-1], y3[len(y3)-1], 'o', linewidth=8.0, color='black')   #向量终点2
# plt.plot(x2[0], y2[0], 'o', linewidth=8.0, color='black')  #向量起点
# # plt.plot(x2,y2, color='red', linewidth=1.5, linestyle='-')
# plt.show()
# print("向量1",x1[0]-x2[0], y1[0]-y2[0])
# print("向量2",x3[len(x3)-1]-x2[0], y3[len(y3)-1]-y2[0])
#
# vector22=[[0.3816179907530896,1.963254366895328],[0.981627183447664,-0.1908089953765448]]
# real33=[[6.244395552837847,32.53099898769288],[40.09888202976251,10.713170001805564]]
#
#
# aaaaaaa=cosine_similarity(vector22,real33)
# print(aaaaaaa)


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
