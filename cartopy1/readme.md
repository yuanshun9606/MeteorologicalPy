# Cartopy的应用

### 引用的库
```python
import numpy as np
import xarray as xr
import matplotlib
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

np.set_printoptions(suppress=True)  # 关闭科学计数法
matplotlib.rc("font", family='MicroSoft YaHei', weight='bold', size=12)  # 设置中文
```

### 创建地图
```python
def creatmap():
    proj = ccrs.PlateCarree()  # 创建投影
    fig = plt.figure(figsize=(15, 8), dpi=80)  # 创建页面
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  # 子图
    # 设置地图属性 
    # ax.add_feature(cfeat.RIVERS.with_scale('50m'), zorder=1)  # rivers
    # ax.add_feature(cfeat.LAKES.with_scale('50m'), zorder=1)   # lakers
    ax.add_feature(cfeat.BORDERS.with_scale('50m'), linewidth=1, zorder=1)  # 国界
    ax.add_feature(cfeat.COASTLINE.with_scale('50m'), linewidth=1, zorder=1)  # 海岸线
    # 设置网格点属性
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.8, color='k', alpha=0.5, linestyle='--')
    gl.toplabels_top = False  # 关闭顶端标签
    gl.rightlabels_right = False  # 关闭右侧标签
    gl.xformatter = LONGITUDE_FORMATTER  # x轴设为经度格式
    gl.yformatter = LATITUDE_FORMATTER  # y轴设为纬度格式
    return fig, ax
```
> 可以单独设置一个文件，如create_map.py以后其他文件需要画图时直接import这个文件,如work1.py示例
```python
from cartopy1.create_map import *
# 建立地图
fig,ax= creatmap()
```
> 如果没出图，尝试以下设置步骤：File ——> Settings ——> Tools ——> Python Scientific ——> 取消勾选 Show plots in toolwindow

- 使用地图时，某些地图属性不要使用时可以在creatmap()函数中将其注释掉
- 其他类型的地图投影可以自行去官方文档查看
### 进行第一次绘图测试
运用xarray1文件中的示例及数据，在work1.py文件中进行绘图测试
```python
# 按时间计算平均值
airmean = air.sel(time=slice('1961-01-01','1990-12-01')).mean(dim='time')
# 绘图
airmean.sel(level=925).plot.contourf(ax=ax,levels=np.arange(-45, 46, 1),cmap='coolwarm',#Spectral_r
                                transform=ccrs.PlateCarree())
```

绘图语句中：

- airmean 为xarray的DataArray或DataSet类型数据集
- sel(level=925) 是取925hPa
- .plot.contourf 是基于matpllib的绘图函数 contourf是填色图 contour是等高线图
- ax=ax 是在设置的地图画图上绘图，一般不用更改
- levels 绘图数值范围，此处设置-45℃~45℃，(步长为1可省略)，类似list类型的序列可以作为参数
- cmap 是填色图的色标选择 常用coolwarm，Spectral_r(加_r是色标反向)，其他类型查看[文档](https://matplotlib.org/2.0.2/users/colormaps.html)
- transform=ccrs.PlateCarree() 对应地图的投影类型，一般不用更改

### 绘图：高度场、距平场、风场综合
如work2.py示例，数据同样来源于[NCEP-DOE Reanalysis 2: Pressure Level](https://psl.noaa.gov/data/gridded/data.ncep.reanalysis2.pressure.html)
```python
# 创建地图
fig, ax = creatmap()
# 设置绘图范围
img_extent = [30, 150, 0, 70]
ax.set_extent(img_extent, crs=ccrs.PlateCarree())
lon, lat = file.lon, file.lat
# 色标信息
cbar_kwargs = cbar_kwargs = {
    'orientation': 'horizontal', # 水平
    'label': '高度场距平 单位： gpm',
    'shrink': 0.5, # 缩小
}
# 高度场距平
(hgt - hgtmean).plot.contourf(levels=np.arange(-40, 60, 5), ax=ax, cmap='coolwarm', cbar_kwargs=cbar_kwargs,
                              transform=ccrs.PlateCarree())
# 高度场等高线
h = hgt.plot.contour(levels=np.arange(4880, 5960, 20), ax=ax, linewidths=1.2, colors='black',
                     transform=ccrs.PlateCarree())
# 等值线上的数值信息
plt.clabel(h, inline=1, fontsize=10, fmt='%1.0f', colors='black')
# 风场
ax.quiver(lon, lat, (u - umean), (v - vmean), transform=ccrs.PlateCarree(), width=0.0025, scale=200, color='g')
# 标题
plt.title('2020年夏季500hPa位势高度场（等值线）和距平场（阴影区）及850hPa风场距平（箭头）')
plt.savefig('../images/2020年夏季500hPa位势高度场（等值线）和距平场（阴影区）及850hPa风场距平（箭头）.png')
```
#### 需要注意的：
- 由于出现了 ax.quiver 这个文件必须要def createmap() 不然会出现bug,可能是由于变量的作用范围引起的问题
- 由于图层覆盖，一般先画填色，再画等值线和风场
- 色标信息不需要调整时用默认的可以在contourf中不写
- 每个函数的颜色属性名不一样，如contourf对应cmap,contourd和clabel对应colors,quiver对应color
- quiver 需要四个参数:前两个是经纬度信息，一般直接引用nc文件的；后两个分别为u，v分量
- quiver width，scale用于调整箭头大小及比例，没有固定数值，需要手动调参到合适情况
![2020年夏季500hPa位势高度场（等值线）和距平场（阴影区）及850hPa风场距平（箭头）.png](D:\mywork\MeteorologicalPy\images\2020年夏季500hPa位势高度场（等值线）和距平场（阴影区）及850hPa风场距平（箭头）.png)