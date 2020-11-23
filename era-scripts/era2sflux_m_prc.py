import gdal
import numpy as np
import netCDF4 as nc4
import glob
import sys

# python era2sflux_air.py work_dir latmin latmax lonmin lonmax resolution timestep sta_year month day
# Read Argument Values                                                                 
data_dir = "/home/dbshin/01_WORKS/99_EXT_DATAS/ERA5/raw_datas/monthly-averaged_20_60_110_150_2017-2019_prc.grib"
outp_dir = "/home/dbshin/01_WORKS/99_EXT_DATAS/ERA5"

[lat_min, lat_max] = [20, 60]   #[ float(sys.argv[1]), float(sys.argv[2]) ]
[lon_min, lon_max] = [110, 150] #[ float(sys.argv[3]), float(sys.argv[4]) ]
lonlat_degree = 0.25 #float(sys.argv[5])
timedata   = np.loadtxt('./time_steps.txt',dtype=np.float32)
time_steps = timedata[4:]
sta_year   = int(timedata[0])
sta_month  = int(timedata[1])
sta_day    = int(timedata[2])
sta_hour   = int(timedata[3])

print('==========================')
print('Data Direcotry : {}'.format(data_dir))
print('==========================')
print('     {}    '.format(lat_max))
print('{}      {}'.format(lon_min,lon_max))
print('     {}    '.format(lat_min))
print('==========================')
lon = np.arange(lon_min, lon_max+lonlat_degree, lonlat_degree)
lat = np.arange(lat_min, lat_max+lonlat_degree, lonlat_degree)
LON, LAT = np.meshgrid(lon, lat)
print(np.shape(LON))
# print(LON)
# print(LAT)
print('==========================')
print('Time Steps : {}'.format(time_steps))
print('==========================')

gribfile  = gdal.Open(data_dir)
for tt, ti in enumerate(range(0,36)):

    ncout = nc4.Dataset('{}/sflux_prc_1.{}.nc'.format(outp_dir,str(tt+1).zfill(4)),'w', format='NETCDF4') #'w' stands for write
    ncout.createDimension('time', None)
    ncout.createDimension('nx_grid', len(lon))
    ncout.createDimension('ny_grid', len(lat))

    time_nc  = ncout.createVariable('time',  'f4','time')
    time_nc.long_name = "Time"; time_nc.standard_name = "time" 
    time_nc.units = "days since {0}-{1}-{2}".format(sta_year, sta_month, sta_day);
    time_nc.base_date = [sta_year, sta_month, sta_day, 0]
    lon_nc   = ncout.createVariable('lon',   'f4',('ny_grid','nx_grid'))
    lon_nc.long_name = "Longitude" 
    lon_nc.standard_name = "longitude" 
    lon_nc.units = "degrees_east" 
    lat_nc   = ncout.createVariable('lat',   'f4',('ny_grid','nx_grid'))
    lat_nc.long_name = "Latitude" 
    lat_nc.standard_name = "latitude" 
    lat_nc.units = "degrees_north" 
    lon_nc[:,:] = LON; lat_nc[:,:] = LAT
    prate_nc = ncout.createVariable('prate', 'f4',('time','ny_grid','nx_grid'))
    prate_nc.long_name = "Surface Precipitation Rate"  
    prate_nc.standard_name = "precipitation_flux"
    prate_nc.units = "kg/m^2/s"

    # 2020053100 :  6481 = 9*720 + 1
    # 2020060100 :  6697 = 9*744 + 1
    # 2020070100 : 13177 = 9*720 + 9*744 + 1
    grb_prate = gribfile.GetRasterBand(ti+1)

    # time_nc[tt]     = time_steps[tt] # hours from start time
    # prate_nc[tt,:,:] = list(reversed(list(grb_prate.ReadAsArray())))

    
    dT = 30
    for ttt in range(dT):
        time_nc[ttt]     = time_steps[tt] + ttt # hours from start time
        prate_nc[ttt,:,:] = list(reversed(list(grb_prate.ReadAsArray())))
    ncout.close()
gribfile  = None

