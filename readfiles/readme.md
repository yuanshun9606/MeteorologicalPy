# 文件读取及应用
### 读取NC文件
> 详情请关注xarray1文件
### 用pandas读取csv文件
```python
import os
import pandas as pd

# 读取文件夹下文件名
files = os.listdir('D:\mywork\meteorological\\fix\\file')
print(files)

# 按照文件名列表逐个读取csv文件
for filename in files:
    file = pd.read_csv(f'D:\mywork\meteorological\\fix\\file\{filename}', encoding='utf-8')
```
注意： 

1、python3.6以上才适用f-string

2、文件名字符串内有的是转义字符，需要调整**双斜杠**(\\\\)


##### 打印的文件名结果（数据结构为列表，元素为带后缀的字符串）
```
['娄底市空气质量指数.csv', '娄底市空气质量指数.xlsx', '岳阳市空气质量指数.csv', '岳阳市空气质量指数.xlsx', '常德市空气质量指数.csv', '常德市空气质量指数.xlsx', '张家界市空气质量指数.csv', '张家界市空气质量指数.xlsx', '怀化市空气质量指数.csv', '怀化市空气质量指数.xlsx', '株洲空气质量指数日历史数据.xls', '永州市空气质量指数.csv', '永州市空气质量指数.xlsx', '湘潭市空气质量指数.csv', '湘潭市空气质量指数.xlsx', '湘西土家族苗族自治州空气质量指数（无数据）.xlsx', '益阳市空气质量指数.csv', '益阳市空气质量指数.xlsx', '衡阳市空气质量指数.csv', '衡阳市空气质量指数.xlsx', '邵阳市空气质量指数.csv', '邵阳市空气质量指数.xlsx', '郴州市空气质量指数.csv', '郴州市空气质量指数.xlsx']

Process finished with exit code 0
```

### 用pandas读取Excel
```python
file = pd.read_excel(f'D:\mywork\meteorological\\fix\\file\{file}', engine='openpyxl',keep_default_na=False)
```
与csv文件大同小异，需要添加（engine='openpyxl'）

### 读取text文件
#### 批量读取txt基本思路：
```python
# 读取文件夹下的文件名列表：  
files = os.listdir(path)
# 对files列表内元素遍历读取
for file in files:
    # 获取该次循环需要读取的文件名
    filename = path+'/'+file 
    # 用with open读取文件
    with open(filename,'r') as f:
        # 每次读入一行
        lines = f.readlines()
        # 如果需要跳过n行
        # lines = f1.readlines()[n:]  
        for line in lines:
            # 逐行读入 将每行元素分解并转化成float数据结构
            linelist = [float(s) for s in line.split()]
            # 此处得到每行的数据，后面操作根据具体情行而定 
```

#### 实例分析
实验的文件结构： data文件中包含air,height...等物理量，每个物理量文件夹下按高度分，每个高度文件夹下按时次分
- data
    - air
        - 100
            - 2020062400.txt
            - 2020062412.txt
            - 2020062500.txt
            - 2020062512.txt
            - 2020062600.txt
            - 2020062612.txt
            - 2020062700.txt
            - ...
        - 150
        - 200
        - 250
        - 300
        - 400
        - 500
        - 700 
        - 850
        - ....
    - height
    - rh
    - uv
```python
import os
import numpy as np
#  批量读取数据
def loaddata(path, n):  # path是路径 n是跳过的行数
    data = []
    files = os.listdir(path)
    files.sort(key=int)  # 对文件名排序 保证次序

    for file in files:
        level = path + '/' + file  # data/物理量/高度
        positions = os.listdir(level) 
        for position in positions:
            if position[8:10] == '00':  # 仅读取指定时次数据
                f = level + '/' + position # data/物理量/每层高度/时次.txt
                # 开始读取数据文件
                with open(f, 'r', errors='ignore') as f1:
                    lines = f1.readlines()[n:]  # 跳过前多少行
                    for line in lines:
                        # 逐行读入 将每行元素分解并转化成float数据结构
                        linelist = [float(s) for s in line.split()]
                        # 将数据并入data列表
                        data.extend(linelist)
    data = np.array(data) # 将data列表转化成np.array的数据结构
    return data


# 读取data文件中air物理量各层数据，跳过前4行表头，并将np.array数据更换矩阵形状
data_air = loaddata('data/air', 4).reshape(11, 7, 37, 73)  # 11个层次，7个时次
```
