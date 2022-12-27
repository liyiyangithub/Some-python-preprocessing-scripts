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
