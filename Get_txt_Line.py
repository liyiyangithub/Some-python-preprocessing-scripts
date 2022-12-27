



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
