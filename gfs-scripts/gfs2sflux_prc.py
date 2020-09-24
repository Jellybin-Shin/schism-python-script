import gdal
import numpy as np
import netCDF4 as nc4
import glob
import sys

# Read Argument Values                                                                 
working_dir = sys.argv[1]
[lat_min, lat_max] = [ float(sys.argv[2]), float(sys.argv[3]) ]
[lon_min, lon_max] = [ float(sys.argv[4]), float(sys.argv[5]) ]
lonlat_degree = float(sys.argv[6])
time_step = float(sys.argv[7])

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
print('==========================')
print('Time Step : {}'.format(time_step))
print('==========================')

files = glob.glob('{}/*grib2*'.format(working_dir))

ncout = nc4.Dataset('sflux_prc_1.0001.nc','w', format='NETCDF4') #'w' stands for write
ncout.createDimension('time', None)
ncout.createDimension('nx_grid', len(lon))
ncout.createDimension('ny_grid', len(lat))

time_nc  = ncout.createVariable('time',  'f4','time')
time_nc.long_name = "Time"; time_nc.standard_name = "time" 
time_nc.units = "days since 2020-06-10"; time_nc.base_date = [2020, 6, 10, 0]
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
prate_nc.long_name =  "Surface Precipitation Rate"
prate_nc.standard_name = "precipitation_flux"
prate_nc.units = "kg/m^2/s" 

print(time_nc)
for i, grib_dir in enumerate(files):    
    print(grib_dir)
    gribfile  = gdal.Open(grib_dir)
    grb_prate  = gribfile.GetRasterBand(1) # PRATE:surface:anl

    time_nc[i] = i*time_step/24 # hours from start time
    prate_nc[i,:,:] = list(reversed(list(grb_prate.ReadAsArray())))
    gribfile  = None
ncout.close()
