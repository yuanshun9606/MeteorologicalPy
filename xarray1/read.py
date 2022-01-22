import xarray as xr

# 读取NC文件
file = xr.open_dataset('D:\mywork\meteorological\\air.mon.mean.nc')
print(file)
