#%matplotlib inline
import numpy as np, pandas as pd, datetime, netCDF4 as nc4, glob, os, sys
import matplotlib.pyplot as pyplot

HYC_dir  = "/home/dbshin/01_WORKS/99_EXT_DATAS/HYCOM_DATA"
SCO_dir  = "/home/Work2/home/dbshin/2020/eastsea/202_fine/905_*/outputs"
os.makedirs(HYC_dir+'/outputs', exist_ok=True)
HYC_list = glob.glob('{}/UV_*nc'.format(HYC_dir))
SCO_list = glob.glob('{}/schout_[0-99].nc'.format(SCO_dir))
HYC_list.sort(key= lambda x : int(x.replace('.','_').split(sep='_')[-2]))
SCO_list.sort(key= lambda x : int(x.replace('.','_').split(sep='_')[-2]))

if len(HYC_list) != 0 :
    print('Reading hycom Files List')
    print('  {} files read'.format(len(HYC_list)))
else : raise Exception('There is no HYCOM UV file')

if len(SCO_list) != 0 :
    print('Reading schism bc Files List')
    print('  {} files read'.format(len(SCO_list)))
else : raise Exception('There is no Schism BC UV file')

# 
schismOn =1
hycomOn = 0

# Point to compare

nodenumber_list= [26, 83, 218, 374]
pointx_list= [130.8, 130.96, 131.2, 131.44]
pointy_list= [34.56, 34.63,  34.66, 35.16]

for pid in range(len(nodenumber_list)):
    nodenumber= nodenumber_list[pid]
    pointx= pointx_list[pid]
    pointy= pointy_list[pid]

    # extract uv timeseries at bc from schism bc data 
    if schismOn == 1 : 
        u_SCO = np.array([])
        v_SCO = np.array([])
        for ii in range(0,len(SCO_list)):
            print(SCO_list[ii])
            with nc4.Dataset(SCO_list[ii]) as SCO:
                uv_SCO = np.array(SCO.variables['hvel'][:])
                u_SCO = np.append(u_SCO,uv_SCO[:,nodenumber,-1,0])
                v_SCO = np.append(v_SCO,uv_SCO[:,nodenumber,-1,1])
        np.savetxt("./schism_node_u_{}.csv".format(nodenumber),u_SCO,delimiter='\n')
        np.savetxt("./schism_node_v_{}.csv".format(nodenumber),v_SCO,delimiter='\n')

            
    # extract uv timeseries at bc from hycom data
    if hycomOn == 1 : 
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
        np.savetxt("./hycom_node_u_{}.csv".format(nodenumber),uu_hyc,delimiter='\n')
        np.savetxt("./hycom_node_v_{}.csv".format(nodenumber),vv_hyc,delimiter='\n')
                
