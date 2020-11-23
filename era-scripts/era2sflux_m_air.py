import gdal
import numpy as np
import netCDF4 as nc4
import glob
import sys

# python era2sflux_air.py work_dir latmin latmax lonmin lonmax resolution timestep sta_year month day
# Read Argument Values                                                                 
data_dir = "/home/dbshin/01_WORKS/99_EXT_DATAS/ERA5/raw_datas/monthly-averaged_20_60_110_150_2017-2019.grib"
outp_dir = "/home/dbshin/01_WORKS/99_EXT_DATAS/ERA5"

[lat_min, lat_max] = [20, 60]   #[ float(sys.argv[1]), float(sys.argv[2]) ]
[lon_min, lon_max] = [110, 150] #[ float(sys.argv[3]), float(sys.argv[4]) ]
lonlat_degree = 0.25 #float(sys.argv[5])
timedata   = np.loadtxt('./time_steps.txt',dtype=np.float32)
time_steps = timedata[4:]
sta_year   = int(timedata[0])
sta_month  = int(timedata[1])
sta_day    = int(float(timedata[2]))
sta_hour   = int(timedata[3])

print(sta_year,sta_month,sta_day)

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

    ncout = nc4.Dataset('{}/sflux_air_1.{}.nc'.format(outp_dir,str(tt+1).zfill(4)),'w', format='NETCDF4') #'w' stands for write
    ncout.createDimension('time', None)
    ncout.createDimension('nx_grid', len(lon))
    ncout.createDimension('ny_grid', len(lat))

    time_nc  = ncout.createVariable('time',  'f4','time')
    time_nc.long_name = "Time"; time_nc.standard_name = "time" 
    time_nc.units = "days since {0}-{1}-{2} {3}:00".format(int(sta_year), int(sta_month), int(sta_day),int(sta_hour))
    time_nc.base_date = [int(sta_year), int(sta_month), int(sta_day), int(sta_hour)]
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

    # 2020053100 :  6481 = 9*720 + 1
    # 2020060100 :  6697 = 9*744 + 1
    # 2020070100 : 13177 = 9*720 + 9*744 + 1
    tgrb = ti*6
    grb_uwind = gribfile.GetRasterBand(1+tgrb) # uwind: 10 m above ground:anl: m/s
    grb_vwind = gribfile.GetRasterBand(2+tgrb) # vwind: 10 m above ground:anl: m/s
    grb_Td    = gribfile.GetRasterBand(3+tgrb) # Td   : 2 m Dewpoint Tempi : K
    grb_stmp  = gribfile.GetRasterBand(4+tgrb) # TMP  : 2 m above ground:anl: K
    grb_prmsl = gribfile.GetRasterBand(5+tgrb) # prmsl: msl:anl: Pa
    grb_sp    = gribfile.GetRasterBand(6+tgrb) # SP   : surface pressrue : Pa

    td = np.array(list(grb_Td.ReadAsArray()))-273.15 # Dewpoint Temp : C degree
    sp = np.array(list(grb_sp.ReadAsArray()))*0.01 # Surface pressure : mb 

    vp    = 6.112*np.exp((17.67*td)/(td+243.5)) # vapor pressure : mb
    spfh  = (0.622*vp)/(sp-0.378*vp)  # SPFH:2 m above ground:anl: kg/kg
    
    
    
    # time_nc[tt]     =  time_steps[tt] + ttt# days from start time
    # stmp_nc[tt, :,:] = list(reversed(list(grb_stmp.ReadAsArray())))
    # spfh_nc[tt, :,:] = list(reversed(spfh))
    # uwind_nc[tt,:,:] = list(reversed(list(grb_uwind.ReadAsArray())))
    # vwind_nc[tt,:,:] = list(reversed(list(grb_vwind.ReadAsArray())))
    # prmsl_nc[tt,:,:] = list(reversed(list(grb_prmsl.ReadAsArray())))

    dT = 30
    for ttt in range(dT):
        time_nc[ttt]     =  time_steps[tt] + ttt# days from start time
        stmp_nc[ttt, :,:] = list(reversed(list(grb_stmp.ReadAsArray())))
        spfh_nc[ttt, :,:] = list(reversed(spfh))
        uwind_nc[ttt,:,:] = list(reversed(list(grb_uwind.ReadAsArray())))
        vwind_nc[ttt,:,:] = list(reversed(list(grb_vwind.ReadAsArray())))
        prmsl_nc[ttt,:,:] = list(reversed(list(grb_prmsl.ReadAsArray())))
    ncout.close()
gribfile  = None

