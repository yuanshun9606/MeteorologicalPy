from cartopy1.create_map import *

fig, ax = creatmap()
# 读取NC文件
file = xr.open_dataset('D:\mywork\meteorological\\air.mon.mean.nc')
# 选取要使用的变量
air = file['air']
# 按时间计算平均值
airmean = air.sel(time=slice('1961-01-01', '1990-12-01')).mean(dim='time')
# 绘图
airmean.sel(level=925).plot.contourf(ax=ax, levels=np.arange(-45, 46, 1), cmap='coolwarm',  # Spectral_r
                                     transform=ccrs.PlateCarree())

#  cbar_kwargs=cbar_kwargs,,
