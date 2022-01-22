from cartopy1.create_map import *


def creatmap():
    proj = ccrs.PlateCarree()  # 创建投影
    fig = plt.figure(figsize=(15, 8), dpi=80)  # 创建页面
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  # 子图
    # 设置地图属性
    # ax.add_feature(cfeat.RIVERS.with_scale('50m'), zorder=1)
    # ax.add_feature(cfeat.LAKES.with_scale('50m'), zorder=1)
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


def qihoutai(file, name, level):
    mean = file[name].sel(level=level).sel(time=slice('1981-01-01', '2010-12-01'))
    # 将5,7,8月选取并拼接成新的数据集
    xmean = xr.concat(
        [mean.isel(time=slice(5, 360, 12)), mean.isel(time=slice(6, 360, 12)),
         mean.isel(time=slice(7, 360, 12))],
        dim='time').mean(dim='time')
    return xmean


file = xr.open_dataset('D:\mywork\meteorological\paper\hgt.2020.nc')
# 月平均高度场文件
file2 = xr.open_dataset('D:\mywork\meteorological\sx\qihouyuce\hgt.mon.mean.nc')
# 月平均风场
file3 = xr.open_dataset('D:\mywork\meteorological\paper\\uwnd.mon.mean.nc')
file4 = xr.open_dataset('D:\mywork\meteorological\paper\\vwnd.mon.mean.nc')

# 2020夏季500hPa平均高度场
hgt = file['hgt'].sel(level='500').sel(time=slice('2020-06-01', '2020-08-31')).mean(dim='time')
# 850hPa风场
u = file3['uwnd'].sel(level='850').sel(time=slice('2020-06-01', '2020-08-31')).mean(dim='time')
v = file4['vwnd'].sel(level='850').sel(time=slice('2020-06-01', '2020-08-31')).mean(dim='time')

# 500hpa高度场气候态
hgtmean = qihoutai(file2, 'hgt', '500')
# 850 u气候态
umean = qihoutai(file3, 'uwnd', '850')
vmean = qihoutai(file4, 'vwnd', '850')

fig, ax = creatmap()
img_extent = [30, 150, 0, 70]
ax.set_extent(img_extent, crs=ccrs.PlateCarree())
lon, lat = file.lon, file.lat

cbar_kwargs = cbar_kwargs = {
    'orientation': 'horizontal',
    'label': '高度场距平 单位： gpm',
    'shrink': 0.5,
}

(hgt - hgtmean).plot.contourf(levels=np.arange(-40, 60, 5), ax=ax, cmap='coolwarm', cbar_kwargs=cbar_kwargs,
                              transform=ccrs.PlateCarree())
h = hgt.plot.contour(levels=np.arange(4880, 5960, 20), ax=ax, linewidths=1.2, colors='black',
                     transform=ccrs.PlateCarree())
plt.clabel(h, inline=1, fontsize=10, fmt='%1.0f', colors='black')

ax.quiver(lon, lat, (u - umean), (v - vmean), transform=ccrs.PlateCarree(), width=0.0025, scale=200, color='g')
plt.title('2020年夏季500hPa位势高度场（等值线）和距平场（阴影区）及850hPa风场距平（箭头）')
plt.savefig('../images/2020年夏季500hPa位势高度场（等值线）和距平场（阴影区）及850hPa风场距平（箭头）.png')