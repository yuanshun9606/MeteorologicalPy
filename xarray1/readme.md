# xarray 应用

###  设置python console运行环境
- 选取工程文件夹MeteorologicalPy
- 打开菜单栏run->edit configurations
- 勾选 Run with Python console
> 使用方式:可以在Python console终端进行交互式调试,如输入变量名，回车后自动输出改变量名结果；输入可执行语句也能执行。
### NC文件结构
```python
import xarray as xr
file = xr.open_dataset('D:\mywork\meteorological\\air.mon.mean.nc')
```
以read.py 结果为例
```
<xarray.Dataset>
Dimensions:  (lat: 73, level: 17, lon: 144, time: 832)
Coordinates:
  * level    (level) float32 1000.0 925.0 850.0 700.0 ... 50.0 30.0 20.0 10.0
  * lat      (lat) float32 90.0 87.5 85.0 82.5 80.0 ... -82.5 -85.0 -87.5 -90.0
  * lon      (lon) float32 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
  * time     (time) datetime64[ns] 1948-01-01 1948-02-01 ... 2017-04-01
Data variables:
    air      (time, level, lat, lon) float32 ...
Attributes:
    description:     Data from NCEP initialized reanalysis (4x/day).  These a...
    platform:       Model
    Conventions:    COARDS
    NCO:            20121012
    history:        Mon Jul  5 21:45:36 1999: ncrcat air.mon.mean.nc /Dataset...
    title:          monthly mean air from the NCEP Reanalysis
    References:     http://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reana...
    dataset_title:  NCEP-NCAR Reanalysis 1
```
- Dimensions 数据的维度信息
- Coordinates 坐标信息
- Data variables 文件内储存的变量 air(即温度)
- Attributes 文件附加的描述信息

### 选取变量
```python
# 选取要使用的变量
air= file['air']
```
如operate.py line7示例

```
<xarray.DataArray 'air' (time: 832, level: 17, lat: 73, lon: 144)>
[148681728 values with dtype=float32]
Coordinates:
  * level    (level) float32 1000.0 925.0 850.0 700.0 ... 50.0 30.0 20.0 10.0
  * lat      (lat) float32 90.0 87.5 85.0 82.5 80.0 ... -82.5 -85.0 -87.5 -90.0
  * lon      (lon) float32 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
  * time     (time) datetime64[ns] 1948-01-01 1948-02-01 ... 2017-04-01
Attributes:
    long_name:     Monthly Mean of Air temperature
    units:         degC
    precision:     2
    var_desc:      Air Temperature
    level_desc:    Multiple levels
    statistic:     Mean
    parent_stat:   Other
    valid_range:   [-200.  300.]
    dataset:       NCEP Reanalysis Derived Products
    actual_range:  [-108.64999    43.240005]
```
> **数据结构为DataArray**，同样具有坐标信息，**只有选取了单个变量才能对其进行操作，是读取文件后的必要操作**

### 选取某维度数据
```python
#选取某维度数据
air1 = air.sel(time='2000-01-01')

#可同时选取多个维度 两种取法都行
air2 = air.sel(time='2000-01-01',lat=30)
air3 = air.sel(time='2000-01-01').sel(lat=30)
```
### 常用的切片操作
```python
# 对时间切片
air4 = air.sel(time=slice('1961-01-01','1990-12-01'))

# 多维度切片
lon = file.lon
lat= file.lat
lon_range = lon[(lon > 70) & (lon < 140)]
lat_range = lat[(lat > 15) & (lat < 55)]
air5 = air.sel(lon=lon_range, lat=lat_range)

# 多维度简单切片
air5 = air.sel(lon=slice(105,125),lat=slice(40,20),level=500)
```

### 常用的计算操作
> 由于xarray与numpy有非常好的融合性，numpy对矩阵的操作函数及广播功能都能对xarray的数据结构使用

示例：calculate.py
```python
# 常用的对时间平均
airmean = air.sel(time=slice('1961-01-01', '1990-12-01')).mean(dim='time')
# 其他维度操作类似

# 将文件中的摄氏温度数值转化成开尔文，所有数值都会被广播操作
airK = air+273.15

# 计算时将pv放大10^6倍
pv7 = (pv*1e6).sel(level=850).sel(time=slice('2020-7-1','2020-7-31')).mean(dim='time')

# 可以运用numpy的函数进行广播
# 假设对一个DataArray数据集 data 所有数据开平方操作
import numpy as np
data1 = np.np.sqrt(data)
```
