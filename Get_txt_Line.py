
# import linecache
#
# h=4
#
# def get_contexts(file_path, line_number):
#     try:
#         return linecache.getline(file_path, line_number)
#     finally:
#         linecache.clearcache()
#
# a=get_contexts('All_training_set.txt', h)
# # b=get_contexts('triInnet_set_.txt', h)
#
# print("--a--",a)

# def openreadtxt(file_name):
#     data = []
#     file = open(file_name, 'r')  # 打开文件
#     file_data = file.readlines()  # 读取所有行
#     for row in file_data:
#         tmp_list = row.split('_')  # 按‘，’切分每行的数据
#         # tmp_list[-1] = tmp_list[-1].replace('\n',',') #去掉换行符
#         data.append(tmp_list)  # 将每行数据插入data中
#     return data
#
#
# if __name__ == "__main__":
#     data = openreadtxt('All_training_set.txt')
#     print(data)

# import numpy as np
#
#
# def loadtxtmethod(filename):
#     data = np.loadtxt(filename, dtype=np.float32, delimiter='_')
#     return data
#
#
# if __name__ == "__main__":
#     data = loadtxtmethod('All_training_set.txt')
#     print(data)


import csv

path = 'C:/Users/Administrator/Desktop/All_training_set.txt'
# newline这里是去除行之间的空行
f = open('C:/Users/Administrator/Desktop/All_training_set.csv', 'w', encoding='utf-8', newline="")

# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)

with open(path, 'r') as f1:
    lines = f1.readlines()
    for i in lines:
        # 这里的字段分割开，是采用的空格方式，如是其它的分割方式，可以替换掉
        data = i.split(' ')
        # 因为txt存储数据往往带有"\n"换行，因此在这里需要去掉
        data1 = data[2][:-1]
        csv_writer.writerow([data[0], data[1], data1])