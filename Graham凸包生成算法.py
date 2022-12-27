
points_list=[[ 794285.980422999942675,2492208.568159999791533 ]  ,
[  794460.240722000016831,2491310.762870000209659 ]  ,
[  794553.455795999965630,2490732.677209999877959 ]  ,
[  794615.384552999981679,2491914.229139999952167 ]  ,
[  794850.242377000045963,2492299.421540000010282 ]  ,
[  794934.688332000048831,2491989.516859999857843 ]  ,
[  795070.868394999997690,2488661.735069999936968 ]  ,
[  795074.411058000056073,2488476.748360000085086 ]  ,
[  795124.789921000017785,2491518.702430000063032 ]  ,
[  795167.790909999981523,2488432.272859999909997 ]  ,
[  795230.515388000058010,2488780.451530000194907 ]  ,
[  795322.112334999954328,2492129.596909999847412 ]  ,
[  795343.914234000025317,2488898.282380000222474 ]  ,
[  795364.377085000043735,2489037.462429999839514 ]  ,
[  795396.927295999950729,2490957.856410000007600 ]  ,
[  795425.714570999960415,2488299.227950000204146 ]  ,
[  795453.733203000039794,2491612.209900000132620 ]  ,
[  795508.560323999961838,2492370.763859999831766 ]  ,
[  795571.956119999988005,2491348.760290000122041 ]  ,
[  795671.700287000043318,2491101.902029999997467 ]  ,
[  795695.264117000042461,2491079.226549999788404 ]  ,
[  795721.049093000008725,2490940.952080000191927 ]  ,
[  795731.233037000056356,2489206.418800000101328 ]  ,
[  795732.519861000007950,2487934.185279999859631 ]  ,
[  795798.380322000011802,2489323.362819999922067 ]  ,
[  795918.878279000055045,2489071.235599999781698 ]  ,
[  795928.929558999952860,2491766.223749999888241 ]  ,
[  796066.924975999980234,2490902.550230000168085 ]  ,
[  796151.439320000004955,2489006.310790000017732 ]  ,
[  796172.308353999978863,2489424.146439999807626 ]  ,
[  796175.451303999987431,2488960.509529999922961 ]  ,
[  796178.108366000000387,2491227.280079999938607 ]  ,
[  796194.572799999965355,2489169.059160000178963 ]  ,
[  796195.462032999959774,2489122.813839999958873 ]  ,
[  796223.457406000001356,2491274.409039999824017 ]  ,
[  796260.595749999978580,2489349.733039999846369 ]  ,
[  796334.667652999982238,2491006.665149999782443 ]  ]

#-----------------------------------------------------------------------------------------------------------------------



import matplotlib.pyplot as plt
import math

def get_bottom_point(points):
    """
    返回points中纵坐标最小的点的索引，如果有多个纵坐标最小的点则返回其中横坐标最小的那个
    :param points:
    :return:
    """
    min_index = 0
    n = len(points)
    for i in range(0, n):
        if points[i][1] < points[min_index][1] or (
                points[i][1] == points[min_index][1] and points[i][0] < points[min_index][0]):
            min_index = i
    return min_index


def sort_polar_angle_cos(points, center_point):
    """
    按照与中心点的极角进行排序，使用的是余弦的方法
    :param points: 需要排序的点
    :param center_point: 中心点
    :return:
    """
    n = len(points)
    cos_value = []
    rank = []
    norm_list = []
    for i in range(0, n):
        point_ = points[i]
        point = [point_[0] - center_point[0], point_[1] - center_point[1]]
        rank.append(i)
        norm_value = math.sqrt(point[0] * point[0] + point[1] * point[1])
        norm_list.append(norm_value)
        if norm_value == 0:
            cos_value.append(1)
        else:
            cos_value.append(point[0] / norm_value)

    for i in range(0, n - 1):
        index = i + 1
        while index > 0:
            if cos_value[index] > cos_value[index - 1] or (
                    cos_value[index] == cos_value[index - 1] and norm_list[index] > norm_list[index - 1]):
                temp = cos_value[index]
                temp_rank = rank[index]
                temp_norm = norm_list[index]
                cos_value[index] = cos_value[index - 1]
                rank[index] = rank[index - 1]
                norm_list[index] = norm_list[index - 1]
                cos_value[index - 1] = temp
                rank[index - 1] = temp_rank
                norm_list[index - 1] = temp_norm
                index = index - 1
            else:
                break
    sorted_points = []
    for i in rank:
        sorted_points.append(points[i])

    return sorted_points


def vector_angle(vector):
    """
    返回一个向量与向量 [1, 0]之间的夹角， 这个夹角是指从[1, 0]沿逆时针方向旋转多少度能到达这个向量
    :param vector:
    :return:
    """
    norm_ = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    if norm_ == 0:
        return 0

    angle = math.acos(vector[0] / norm_)
    if vector[1] >= 0:
        return angle
    else:
        return 2 * math.pi - angle


def coss_multi(v1, v2):
    """
    计算两个向量的叉乘
    :param v1:
    :param v2:
    :return:
    """
    return v1[0] * v2[1] - v1[1] * v2[0]


def graham_scan(points):
    # print("Graham扫描法计算凸包")
    bottom_index = get_bottom_point(points)
    bottom_point = points.pop(bottom_index)
    sorted_points = sort_polar_angle_cos(points, bottom_point)

    m = len(sorted_points)
    if m < 2:
        print("点的数量过少，无法构成凸包")
        return

    stack = []
    stack.append(bottom_point)
    stack.append(sorted_points[0])
    stack.append(sorted_points[1])

    for i in range(2, m):
        length = len(stack)
        top = stack[length - 1]
        next_top = stack[length - 2]
        v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
        v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        while coss_multi(v1, v2) >= 0:
            stack.pop()
            length = len(stack)
            top = stack[length - 1]
            next_top = stack[length - 2]
            v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
            v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        stack.append(sorted_points[i])

    stack.append(stack[0])

    return stack


result = graham_scan(points_list)


length = len(result)
print(length)
for i in range(0, length - 1):
    plt.plot([result[i][0], result[i + 1][0]], [result[i][1], result[i + 1][1]], c='b')

plt.show()


