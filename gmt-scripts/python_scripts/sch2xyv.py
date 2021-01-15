'''
    Extracting xyv data from schout_*.nc. 
    Use this script after combining outputs.

    How to use:
        #-------------------------------------------------------------------#
        | #!/bin/sh                                                         |
        | perl {modelset}/autocombine_MPI_elfe.pl {} {}                     |
        | python sch2xyv.py {modelset/outputs} {output_dir} hvel 12000 3    |
        #-------------------------------------------------------------------#
        >> It produces outputs as '{output_dir}/hvel_t-12000_vl-3.xyz'
    
    Pakage Use: 
        numpy, pandas, datetime, netCDF4, glob, os, sys
        
    by dbshin
'''

import numpy as np, pandas as pd, datetime, netCDF4 as nc4, glob, os, sys
sys.path.append('/home/dbshin/git/schism-related-script-master/general-scripts')
from schismpy.mesh.hgrid import Hgrid

def read_time_info(work_dir):
    # Read First schout_1.nc
    # total number of schout_*.nc files?
    try : 
        tmpNC4file = nc4.Dataset("{}/schout_1.nc".format(work_dir),"r",format="netcdf4")
        time  = tmpNC4file.variables['time'][:]
    except : raise Exception('schout_1.nc doesn\'t exist in working directory')
    dt = time[1] - time[0]
    nt = len(time)
    return [dt, nt]

def find_outputs_including_target_time(dt,nt,target_time):
    if (target_time%dt)==0 : 
        schout_n=int((target_time//dt-1)//nt + 1)
        t_index =int((target_time//dt-1)%nt)
        scho_fname='schout_{}.nc'.format(schout_n)
    else : raise Exception('{}-th time step doesn\'t exist in outputs'.format(target_t))

    print(scho_fname, t_index)
    return [scho_fname, t_index]

def extract_xyv(work_dir,scho_fname,t_index,target_var,vlayern=-1):
    try : 
        nc4file  = nc4.Dataset("{}/{}".format(work_dir,scho_fname),"r",format="netcdf4")
        hgridDir  = '{}/../hgrid.ll'.format(work_dir)
        hgrid_dict = Hgrid.open(hgridDir)
        x_lon = hgrid_dict['Node'][:,0]
        y_lat = hgrid_dict['Node'][:,1]

        #x_lon = nc4file.variables['SCHISM_hgrid_node_x'][:]
        #y_lat = nc4file.variables['SCHISM_hgrid_node_y'][:]


        timetable = nc4file.variables['time'][:]
        var_data = nc4file.variables[target_var][:]

    except : raise Exception('{} doesn\'t exist in working directory'.format(scho_fname))


    vars_2DS = ['elev','solar_radiation','specific_humidity']
    vars_2DV = ['dahv','wind_speed']
    vars_3DS = ['temp','zcor','vertical_velocity']
    vars_3DV = ['hvel']

    if vlayern == -1 :
        if target_var in vars_2DS :
            df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V':var_data[t_index,:]})
        elif target_var in vars_2DV :
            df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V1':var_data[t_index,:,0], 'V2':var_data[t_index,:,1]})
    else :
        try : 
            if target_var in vars_3DS :   
                df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V':var_data[t_index,:,vlayern]}) 
            elif target_var in vars_3DV :
                df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V1':var_data[t_index,:,vlayern,0], 'V2':var_data[t_index,:,vlayern,1]}) 
        except : raise Exception('The variable is not 3D data, or the vlayer number is out of range')
    
    df.to_csv('{}/{}_t-{}_vl-{}.xyv'.format(output_path,target_var,int(timetable[t_index]),vlayern), index=None,header=None,sep='\t')

#----- Arguments ------#
work_dir    = sys.argv[1]
output_path = sys.argv[2]
target_var  = sys.argv[3]
target_time = float(sys.argv[4])
vlayern     = int(sys.argv[5])
#----------------------#

[dt,nt]              = read_time_info(work_dir)
[scho_fname,t_index] = find_outputs_including_target_time(dt, nt, target_time)

extract_xyv(work_dir, scho_fname, t_index, target_var, vlayern)
