import os
import pandas as pd

# 读取文件夹下文件名
files = os.listdir('D:\mywork\meteorological\\fix\\file')
print(files)

for filename in files:
    file = pd.read_csv(f'D:\mywork\meteorological\\fix\\file\{filename}', encoding='utf-8')
    # file = pd.read_excel(f'D:\mywork\meteorological\\fix\\file\{file}', engine='openpyxl',keep_default_na=False)
