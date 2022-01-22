import xarray as xr
import numpy as np

file = xr.open_dataset('D:\mywork\meteorological\\air.mon.mean.nc')
air = file['air']

# 常用的对时间平均
airmean = air.sel(time=slice('1961-01-01', '1990-12-01')).mean(dim='time')

# 将文件中的摄氏温度数值转化成开尔文
airK = air+273.15

np.sqrt(airK)