import xarray as xr

# 读取NC文件
file = xr.open_dataset('D:\mywork\meteorological\\air.mon.mean.nc')

# 选取要使用的变量
air= file['air']

#选取某维度数据
air1 = air.sel(time='2000-01-01')

#可同时选取多个维度 两种取法都行
air2 = air.sel(time='2000-01-01',lat=30)
air3 = air.sel(time='2000-01-01').sel(lat=30)

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