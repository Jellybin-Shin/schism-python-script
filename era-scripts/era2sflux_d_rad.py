import gdal
import numpy as np
import netCDF4 as nc4
import glob
import sys

# python era2sflux_rad.py work_dir latmin latmax lonmin lonmax resolution timestep sta_year month day
# resolution 0.25
# Read Argument Values                                                                 
working_dir = sys.argv[1]
[lat_min, lat_max] = [ float(sys.argv[2]), float(sys.argv[3]) ]
[lon_min, lon_max] = [ float(sys.argv[4]), float(sys.argv[5]) ]
lonlat_degree = float(sys.argv[6])
sta_year = int(sys.argv[7])
sta_month= int(sys.argv[8])
sta_day  = int(sys.argv[9])

# Create lon / lat array
print('==========================')
print('Working Direcotry : {}'.format(working_dir))
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
# print('==========================')
# print('Time Step : {}'.format(time_step))
# print('==========================')

files = glob.glob('{}/*rad.grib'.format(working_dir))
print("File : {}".format(files[0]))

ncout = nc4.Dataset('{}/sflux_rad_1.0001.nc'.format(working_dir),'w', format='NETCDF4') #'w' stands for write
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
dswrf_nc = ncout.createVariable('dswrf', 'f4',('time','ny_grid','nx_grid'))
dswrf_nc.long_name = "Downward short Wave Radiation Flux"  
dswrf_nc.standard_name = "surface_downwelling_shortwave_flux_in_air" 
dswrf_nc.units = "W/m^2" 
dlwrf_nc = ncout.createVariable('dlwrf', 'f4',('time','ny_grid','nx_grid'))
dlwrf_nc.long_name = "Downward Long Wave Radiation Flux"  
dlwrf_nc.standard_name = "surface_downwelling_longwave_flux_in_air"
dlwrf_nc.units = "W/m^2" 

gribfile  = gdal.Open(files[0])
# 2020 05 01 06 lw :         15
# 2020 05 30 06 lw :  1407 = 15 + 29*48      
# 2020 05 31 00 lw :  1443 = 15 + 29*48 + 36 
# 2020 07 01 06 lw :  2943 = 15 + 61*48      
t = 0
sta_time = 1443
end_time = 2943
for ti in range(sta_time,end_time,2):
    grb_long = gribfile.GetRasterBand(ti) 
    grb_short = gribfile.GetRasterBand(ti+1) 

    time_nc[t] = t/24. # hours from start time
    dlwrf_nc[t,:,:] = list(reversed(list(grb_long.ReadAsArray())))
    dswrf_nc[t,:,:] = list(reversed(list(grb_short.ReadAsArray())))
    t = t+1
gribfile  = None

ncout.close()