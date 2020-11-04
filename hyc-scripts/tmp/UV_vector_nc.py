#%matplotlib inline
import numpy as np, pandas as pd, datetime, netCDF4 as nc4, glob, os, sys

'''
        short water_v(time, depth, lat, lon) ;
                water_v:long_name = "Northward Water Velocity" ;
                water_v:standard_name = "northward_sea_water_velocity" ;
                water_v:units = "m/s" ;
                water_v:_FillValue = -30000s ;
                water_v:missing_value = -30000s ;
                water_v:scale_factor = 0.001f ;
                water_v:add_offset = 0.f ;
                water_v:NAVO_code = 18 ;
                water_v:coordinates = "time depth lat lon lat lon" ;

        float hvel(time, nSCHISM_hgrid_node, nSCHISM_vgrid_layers, two) ;
                hvel:missing_value = 9.96921e+36f ;
                hvel:mesh = "SCHISM_hgrid" ;
                hvel:data_horizontal_center = "node" ;
                hvel:data_vertical_center = "full" ;
                hvel:i23d = 2 ;
                hvel:ivs = 2 ;
'''
work_dir  = "/home/dbshin/01_WORKS/99_EXT_DATAS/HYCOM_DATA"
os.makedirs(work_dir+'/outputs', exist_ok=True)
file_list = glob.glob('{}/UV_*nc'.format(work_dir))
if len(file_list) != 0 :
    print('Reading Files List')
else : raise Exception('There is no UV file in working directory')

toexclude = ["water_u","water_v"]
for ii in range(0,1):
    with nc4.Dataset(file_list[ii]) as src, nc4.Dataset('{}/outputs/{}.vec.nc'.format(work_dir,file_list[ii].split(sep='/',)[-1]), "w") as dst:
        # copy attributes
        for name in src.ncattrs():
            dst.setncattr(name, src.getncattr(name))
        # copy dimensions
        for name, dimension in src.dimensions.items():
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited else None))
        # copy all file data except for the excluded
        for name, variable in src.variables.items():
            if name not in toexclude:
                x = dst.createVariable(name, variable.datatype, variable.dimensions)
                dst.variables[name][:] = src.variables[name][:]
        uu = src.variables['water_u']
        vv = src.variables['water_v']
        dst.createDimension('two', 2)
        UV = dst.createVariable('UV','f4',('time','depth','lat','lon','two'))
        UV.long_name = "uv vector" 
        UV.standard_name = "uv vector" 
        UV.units = "m/s" 
        # print(np.shape(uu[:]))

        # print(np.shape(UV[:,:,:,:,0]))

        # UV._FillValue = uu._FillValue
        UV[:,:,:,:,0]=uu[:]
        UV[:,:,:,:,1]=vv[:]


            
# for ii in range(0,1):
#     # Open the UV_*.nc file
#     print('Open "{}" file.'.format(file_list[ii]))
#     ncori = nc4.Dataset(file_list[ii],"r",format="netcdf4")
#     ncout = nc4.Dataset('{}/outputs/{}.vec.nc'.format(work_dir,file_list[ii].split(sep='/',)[-1]),'w', format='NETCDF4') #'w' stands for write
#     print(ncori.__dict__)
#     ncout.setncatts(ncori.__dict__)
#     for name, dimension in ncori.dimensions.items():
#         ncout.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
    
#     for name, variable in ncori.variables.items():
#         if name not in toexclude:
#             x = ncout.createVariable(name, variable.datatype, variable.dimensions)
#             ncout[name][:] = ncori[name][:]
#             ncout[name].setncatts(ncori[name].__dict__)
# ncout.close()
    # # Reading variables
    # depthi = ncori.variables['depth']
    # time = ncori.variables['time']
    # lat= ncori.variables['lat']
    # lon= ncori.variables['lon']
    # uu = ncori.variables['water_u']
    # vv = ncori.variables['water_v']
    
    # uf = np.array(uu[:],'f')
    # vf = np.array(vv[:],'f')
    # uf = np.where(uf!=uu._FillValue, uf, np.nan)
    # vf = np.where(vf!=vv._FillValue, vf, np.nan)

    
    # # Outputs
    # ncout.createDimension('time', None)
    # ncout.createDimension('nx_grid', len(lon[:]))
    # ncout.createDimension('ny_grid', len(lat[:]))
    # ncout.createDimension('depth', len(depthi[:]))
    # ncout.createDimension('rank', 2)

    # deptho = ncout.createVariable('time','f4','time')


    

