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
sta_year = int(sys.argv[8])
sta_month= int(sys.argv[9])
sta_day  = int(sys.argv[10])

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
dswrf_nc  = ncout.createVariable('dswrf',  'f4',('time','ny_grid','nx_grid'))
dswrf_nc.long_name = "Downward short Wave Radiation Flux" ;
dswrf_nc.standard_name = "surface_downwelling_shortwave_flux_in_air" ;
dswrf_nc.units = "W/m^2" ;
dlwrf_nc  = ncout.createVariable('dlwrf',  'f4',('time','ny_grid','nx_grid'))
dlwrf_nc.long_name = "Downward Long Wave Radiation Flux" ;
dlwrf_nc.standard_name = "surface_downwelling_longwave_flux_in_air" ;
dlwrf_nc.units = "W/m^2" ;


print(time_nc)
for i, grib_dir in enumerate(files):    
    print(grib_dir)
    gribfile  = gdal.Open(grib_dir)
    grb_dswrf  = gribfile.GetRasterBand(1) # DSWRF:surface:0-3 hour ave fcst:
    grb_dlwrf  = gribfile.GetRasterBand(2) # DLWRF:surface:0-3 hour ave fcst:

    time_nc[i] = i*time_step/24 # hours from start time
    dswrf_nc[i,:,:] = list(reversed(list(grb_dswrf.ReadAsArray())))
    dlwrf_nc[i,:,:] = list(reversed(list(grb_dlwrf.ReadAsArray())))
    gribfile  = None
ncout.close()
