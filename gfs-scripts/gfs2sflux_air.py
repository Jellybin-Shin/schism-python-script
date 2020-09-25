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


ncout = nc4.Dataset('{}/sflux_air_1.0001.nc'.format(working_dir),'w', format='NETCDF4') #'w' stands for write
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
uwind_nc = ncout.createVariable('uwind', 'f4',('time','ny_grid','nx_grid'))
uwind_nc.long_name = "Surface Eastward Air Velocity (10m AGL)" 
uwind_nc.standard_name = "eastward_wind" 
uwind_nc.units = "m/s" 
vwind_nc = ncout.createVariable('vwind', 'f4',('time','ny_grid','nx_grid'))
vwind_nc.long_name = "Surface Northward Air Velocity (10m AGL)" 
vwind_nc.standard_name = "northward_wind" 
vwind_nc.units = "m/s" 
prmsl_nc = ncout.createVariable('prmsl', 'f4',('time','ny_grid','nx_grid'))
prmsl_nc.long_name = "Pressure reduced to MSL" 
prmsl_nc.standard_name = "air_pressure_at_sea_level" 
prmsl_nc.units = "Pa" 
stmp_nc  = ncout.createVariable('stmp',  'f4',('time','ny_grid','nx_grid'))
stmp_nc.long_name = "Surface Air Temperature (2m AGL)" 
stmp_nc.standard_name = "air_temperature" 
stmp_nc.units = "K" 
spfh_nc  = ncout.createVariable('spfh',  'f4',('time','ny_grid','nx_grid'))
spfh_nc.long_name = "Surface Specific Humidity (2m AGL)" 
spfh_nc.standard_name = "specific_humidity" 
spfh_nc.units = "kg/kg" 



print(time_nc)
for i, grib_dir in enumerate(files):    
    print(grib_dir)
    gribfile  = gdal.Open(grib_dir)
    grb_stmp  = gribfile.GetRasterBand(2) # TMP:2 m above ground:anl:
    grb_spfh  = gribfile.GetRasterBand(3) # SPFH:2 m above ground:anl:
    grb_uwind = gribfile.GetRasterBand(4) # uwind:10 m above ground:anl:
    grb_vwind = gribfile.GetRasterBand(5) # vwind:10 m above ground:anl:
    if (i%2)==0 :
        grb_prmsl = gribfile.GetRasterBand(7) # prmsl:msl:anl:
    else :
        grb_prmsl = gribfile.GetRasterBand(10) # prmsl:msl:anl:
    
    time_nc[i] = i*time_step/24 # hours from start time
    stmp_nc[i,:,:] = list(reversed(list(grb_stmp.ReadAsArray()+273.15)))
    spfh_nc[i,:,:] = list(reversed(list(grb_spfh.ReadAsArray())))
    uwind_nc[i,:,:] = list(reversed(list(grb_uwind.ReadAsArray())))
    vwind_nc[i,:,:] = list(reversed(list(grb_vwind.ReadAsArray())))
    prmsl_nc[i,:,:] = list(reversed(list(grb_prmsl.ReadAsArray())))
    gribfile  = None
ncout.close()
