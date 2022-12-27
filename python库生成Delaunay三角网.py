import numpy as np

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import math


point_x_list=[41.03497918055684, 56.28232126763442, 47.289697545685135, 32.906603782349586, 34.21378580906222, 17.72706682759642, 15.006001025992847, 0.1, 8.102651614008646, 23.10856521780375, 19.370665919606606, 35.12519478176533,41.03497918055684]

point_y_list=[55.20062828275897, 52.04532401156511, 6.905326757885632e-08, 2.1115904710029753, 14.512393348195311, 17.202151495123595, 6.694531201561515, 8.33019788, 59.72929682730032, 56.22364276300833, 30.292088549447517, 28.606184431250063,55.20062828275897]

def GetTrianglesXY(numberArray,pointX,pointY):#---------------------根据三角形的编号确定三角形的坐标点------------------------
    triangles=[]
    for i in range(0,len(numberArray)):
        triangles.append([[pointX[numberArray[i][0]],pointX[numberArray[i][1]],pointX[numberArray[i][2]],pointX[numberArray[i][0]]],[pointY[numberArray[i][0]],pointY[numberArray[i][1]],pointY[numberArray[i][2]],pointY[numberArray[i][0]]]])
    return triangles

#------------------------------------------------end------------------------------------------------------------------
NL=[]
for i in range(0,len(point_x_list)):
    NL.append([point_x_list[i],point_y_list[i]])
new_point_list=np.array(NL)

points = new_point_list
tri = Delaunay(points)

z=tri.simplices
a_list=z.tolist()
TrianglesT=GetTrianglesXY(a_list,point_x_list,point_y_list)

print("--三角网List--",TrianglesT)

for i12 in range(0, len(TrianglesT)):
    plt.plot(TrianglesT[i12][0],TrianglesT[i12][1], color='green', linewidth=1.0, linestyle='-')


plt.show()


