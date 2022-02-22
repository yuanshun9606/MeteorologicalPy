import os
#  批量读取数据
def loaddata(path, n):  # n是跳过的行数
    data = []
    files = os.listdir(path)
    files.sort(key=int)

    for file in files:
        level = path + '/' + file
        positions = os.listdir(level)
        for position in positions:
            if position[8:10] == '00':  # 仅读取指定时次数据
                f = level + '/' + position
                with open(f, 'r', errors='ignore') as f1:
                    lines = f1.readlines()[n:]  # 跳过前多少行
                    for line in lines:
                        linelist = [float(s) for s in line.split()]
                        data.extend(linelist)
    data = np.array(data)
    return data