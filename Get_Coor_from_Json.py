import json, os, math, datetime
import numpy as np
import matplotlib.pyplot as plt

def process_data(filename):
    print("Interpreting the {} data".format(filename))
    file = open(filename, 'r', encoding='utf-8')
    data = json.load(file)
    feature_size = len(data['features'])
    inFIDDic = {}
    totally=[]
    # print("-----------------",feature_size)
    for i in range(0, feature_size):
        # Get the attributes.
        # label = data['features'][i]['attributes']['type']
        # inFID = data['features'][i]['attributes']['inFID']
        # label = data['features'][i]['attributes']['A']
        # inFID = data['features'][i]['attributes']['inFID']
        Geometry=data['features'][i]['geometry']
        geome_dict = data['features'][i]['geometry']
        geo_content = geome_dict.get('rings')
        # print("111111111111111111111111",geo_content)
        building_coords=[]
        for j in range(0, len(geo_content[0])):
            building_coords.append([geo_content[0][j][0], geo_content[0][j][1]])
        # if inFIDDic.get(inFID) == None:
        #     inFIDDic[inFID] = [label, [building_coords]]
        # else:
        #     inFIDDic[inFID][1].append(building_coords)
        totally.append(building_coords)
    # print("inFIDDic",inFIDDic)
    return totally

# A=process_data('F:\--------------毕业论文------------\毕业论文\H.json')

A=process_data('E:/0000000顾及局部特征的模板化简方法0000000000/hebing.json')
#-------------------明天转为字典-----------------------把训练集做出来---------------------------
A=list(A)
print(A)
#
# for i in range(0,len(list(A))):
#     plt.plot(np.array(list(A)[i]).T[0],np.array(list(A)[i]).T[1], color='black', linewidth=2.0, linestyle='-')
#     # plt.plot(np.array(a[p]).T[0], np.array(a[p]).T[1], color='black', linewidth=2.0, linestyle='-')
#     plt.show()


# def JiaMiNode(X,Y,value):
#     new_x=[]
#     new_y=[]
#     start_dis=0
#     for i in range (0,len(X)-1):
#         if ((X[i] < X[i + 1]) and (Y[i] < Y[i + 1])):
#             "CASE1"
#             dis=math.sqrt(pow((X[i+1]-X[i]),2)+pow((Y[i+1]-Y[i]),2))
#             cos_angle=(X[i+1]-X[i])/dis
#             sin_angle=(Y[i+1]-Y[i])/dis                                 #角度计算
#             current_x=X[i]+start_dis*cos_angle
#             current_y=Y[i]+start_dis*sin_angle
#
#             while ((current_x < X[i + 1]) and (current_y < Y[i + 1])):      #如果超过线段的另一个端点
#                 new_x.append(current_x)
#                 new_y.append(current_y)
#                 current_x = current_x + value * cos_angle
#                 current_y = current_y + value * sin_angle
#             new_x.append(X[i + 1])
#             new_y.append(Y[i + 1])
#             start_dis= value-math.sqrt(pow(current_x-X[i + 1],2)+pow(current_y-Y[i + 1],2))
# #-----------------------------------------------------------------------------------------------------------------------
#         elif ((X[i] < X[i + 1]) and (Y[i] > Y[i + 1])):
#             "CASE2"
#             dis = math.sqrt(pow((X[i + 1] - X[i]), 2) + pow((Y[i] - Y[i+1]), 2))
#             cos_angle = (X[i+1] - X[i]) / dis
#             sin_angle = (Y[i] - Y[i+1]) / dis
#             current_x = X[i] + start_dis * cos_angle
#             current_y = Y[i] - start_dis * sin_angle
#
#             while ((current_x < X[i + 1]) and (current_y > Y[i + 1])):  # 如果超过线段的另一个端点
#                 new_x.append(current_x)
#                 new_y.append(current_y)
#                 current_x = current_x + value * cos_angle
#                 current_y = current_y - value * sin_angle
#             new_x.append(X[i + 1])
#             new_y.append(Y[i + 1])
#             start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))
# # -----------------------------------------------------------------------------------------------------------------------
#         elif ((X[i] > X[i + 1]) and (Y[i] < Y[i + 1])):
#             "CASE3"
#             dis = math.sqrt(pow((X[i] - X[i+1]), 2) + pow((Y[i+1] - Y[i]), 2))
#             cos_angle = (X[i] - X[i+1]) / dis
#             sin_angle = (Y[i+1] - Y[i]) / dis
#             current_x = X[i] - value * cos_angle
#             current_y = Y[i] + value * sin_angle
#
#             while ((current_x > X[i + 1]) and (current_y < Y[i + 1])):  # 如果没有超过线段的另一个端点
#                 new_x.append(current_x)
#                 new_y.append(current_y)
#                 current_x = current_x - value * cos_angle
#                 current_y = current_y + value * sin_angle
#             new_x.append(X[i + 1])
#             new_y.append(Y[i + 1])
#             start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))
# # -----------------------------------------------------------------------------------------------------------------------
#         elif ((X[i] > X[i + 1]) and (Y[i] > Y[i + 1])):
#             "CASE4"
#             dis = math.sqrt(pow((X[i] - X[i + 1]), 2) + pow((Y[i] - Y[i + 1]), 2))
#             cos_angle = (X[i] - X[i + 1]) / dis
#             sin_angle = (Y[i] - Y[i + 1]) / dis
#             current_x = X[i] - value * cos_angle
#             current_y = Y[i] - value * sin_angle
#
#             while ((current_x > X[i + 1]) and (current_y > Y[i + 1])):  # 如果没有超过线段的另一个端点
#                 new_x.append(current_x)
#                 new_y.append(current_y)
#                 current_x = current_x - value * cos_angle
#                 current_y = current_y - value * sin_angle
#             new_x.append(X[i + 1])
#             new_y.append(Y[i + 1])
#             start_dis = value - math.sqrt(pow(current_x - X[i + 1], 2) + pow(current_y - Y[i + 1], 2))
#
#     return new_x,new_y