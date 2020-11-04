#%matplotlib inline
import numpy as np, pandas as pd, datetime, netCDF4 as nc4, glob, os, sys
import matplotlib.pyplot as plt

HYC_dir  = "/home/dbshin/01_WORKS/99_EXT_DATAS/HYCOM_DATA"
SBC_dir  = "/home/Work2/home/dbshin/2020/eastsea/202_fine/515_hourly-air_tide8_bchycom_ihorcon2_hvis0.0001/"
os.makedirs(HYC_dir+'/outputs', exist_ok=True)
HYC_list = glob.glob('{}/UV_*nc'.format(HYC_dir))
SBC_list = glob.glob('{}/uv3D.th.nc'.format(SBC_dir))
HYC_list.sort(key= lambda x : int(x.replace('.','_').split(sep='_')[-2]))

if len(HYC_list) != 0 :
    print('Reading hycom Files List')
else : raise Exception('There is no HYCOM UV file')

if len(SBC_list) != 0 :
    print('Reading schism bc Files List')
else : raise Exception('There is no Schism BC UV file')


# Point to compare
bcnodenumber= 18
pointx= 129.68
pointy= 35.32


# extract uv timeseries at bc from schism bc data 
for ii in range(0,len(SBC_list)):
    print(SBC_list[ii])
    with nc4.Dataset(SBC_list[ii]) as sbc:
        uv_sbc = np.array(sbc.variables['time_series'][:])
        u_sbc = uv_sbc[:,bcnodenumber,-1,0]
        v_sbc = uv_sbc[:,bcnodenumber,-1,1]
np.savetxt("./schism_bc_u_{}.csv".format(bcnodenumber),u_sbc,delimiter='\n')
np.savetxt("./schism_bc_v_{}.csv".format(bcnodenumber),v_sbc,delimiter='\n')

        
# extract uv timeseries at bc from hycom data
tmp_hyc=nc4.Dataset(HYC_list[0])
lon_hyc = np.array(tmp_hyc.variables['lon'][:])
lat_hyc = np.array(tmp_hyc.variables['lat'][:])
lon_idx = (lon_hyc > (pointx-0.01))&(lon_hyc < (pointx+0.01))
lat_idx = (lat_hyc > (pointy-0.01))&(lat_hyc < (pointy+0.01))
uu_hyc = np.array(tmp_hyc.variables['water_u'][:])[:,0,lat_idx,lon_idx]
vv_hyc = np.array(tmp_hyc.variables['water_v'][:])[:,0,lat_idx,lon_idx]
print(lon_hyc[lon_idx])
print(lat_hyc[lat_idx])
for ii in range(1,len(HYC_list)):
    print(HYC_list[ii])
    with nc4.Dataset(HYC_list[ii]) as hyc:
        u_hyc = np.array(hyc.variables['water_u'][:])
        v_hyc = np.array(hyc.variables['water_v'][:])
        uu_hyc= np.append(uu_hyc, u_hyc[:,0,lat_idx,lon_idx])
        vv_hyc= np.append(vv_hyc, v_hyc[:,0,lat_idx,lon_idx])
np.savetxt("./hycom_bc_u_{}.csv".format(bcnodenumber),uu_hyc,delimiter='\n')
np.savetxt("./hycom_bc_v_{}.csv".format(bcnodenumber),vv_hyc,delimiter='\n')
        
