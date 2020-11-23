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
np.seterr(divide='ignore', invalid='ignore')

def read_time_info(schout_dir):
    # Read First schout_1.nc
    # total number of schout_*.nc files?
    try : 
        tmpNC4file = nc4.Dataset("{}/schout_1.nc".format(schout_dir),"r",format="netcdf4")
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
    else : 
        errmsg = '{}-th time step doesn\'t exist in outputs.'.format(target_time)
        raise Exception(errmsg)

    print(scho_fname, t_index)
    return [scho_fname, t_index]

def extract_xyv(schout_dir,scho_fname,t_index,target_var,vlayern=-999, save_csv=0):
    os.makedirs(schout_dir+'/figures', exist_ok=True)
    try : 
        nc4file  = nc4.Dataset("{}/{}".format(schout_dir,scho_fname),"r",format="netcdf4")

        x_lon = nc4file.variables['SCHISM_hgrid_node_x'][:]
        y_lat = nc4file.variables['SCHISM_hgrid_node_y'][:]
        timetable = nc4file.variables['time'][:]
        var_nc4 = nc4file.variables[target_var]
        var_data = np.array(nc4file.variables[target_var][:])
        var_data = np.where(var_data!=var_nc4.missing_value, var_data, np.nan)

    except : raise Exception('{} doesn\'t exist in working directory'.format(scho_fname))


    vars_2DS = ['elev','solar_radiation','specific_humidity']
    vars_2DV = ['dahv','wind_speed']
    vars_3DS = ['temp','zcor','vertical_velocity']
    vars_3DV = ['hvel']

    if vlayern == -999 :
        if target_var in vars_2DS :
            df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V':var_data[t_index,:]})
            if save_csv == 1 :    
                output_path = '{}/figures'.format(schout_dir)
                outf_name = '{}_t-{}.xyv'.format(target_var, int(timetable[t_index]))
                df.to_csv('{}/{}'.format(output_path,outf_name, index=None,header=None,sep='\t'))
        elif target_var in vars_2DV :
            length = (var_data[t_index,:,0]**2. + var_data[t_index,:,1]**2.)**(0.5)
            direct = np.rad2deg(np.arcsin(var_data[t_index,:,0]/length))
            df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'D':direct, 'L':length})
            # df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V1':var_data[t_index,:,0], 'V2':var_data[t_index,:,1]})
            if save_csv == 1 :    
                output_path = '{}/figures'.format(schout_dir)
                outf_name = '{}_t-{}_vl-{}.xydl'.format(target_var, int(timetable[t_index]), vlayern)
                df.to_csv('{}/{}'.format(output_path,outf_name, index=None,header=None,sep='\t'))
    else :
        try : 
            if target_var in vars_3DS :   
                df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'V':var_data[t_index,:,vlayern]}) 
                if save_csv == 1 :    
                    output_path = '{}/figures'.format(schout_dir)
                    outf_name = '{}_t-{}.xyv'.format(target_var, int(timetable[t_index]))
                    df.to_csv('{}/{}'.format(output_path,outf_name, index=None,header=None,sep='\t'))
            elif target_var in vars_3DV :
                length = (var_data[t_index,:,vlayern,0]**2. + var_data[t_index,:,vlayern,1]**2.)**(0.5)
                direct = np.rad2deg(np.arcsin(var_data[t_index,:,vlayern,0]/length))
                df = pd.DataFrame({'X':x_lon, 'Y':y_lat, 'D':direct, 'L':length})
                if save_csv == 1 :    
                    output_path = '{}/figures'.format(schout_dir)
                    outf_name = '{}_t-{}_vl-{}.xydl'.format(target_var, int(timetable[t_index]), vlayern)
                    df.to_csv('{}/{}'.format(output_path,outf_name, index=None,header=None,sep='\t'))
        except : raise Exception('The variable is not 3D data, or the vlayer number is out of range')
    
    return df


if __name__ == '__main__':
    #----- Arguments ------#
    schout_dir  = sys.argv[1]
    target_var  = sys.argv[2]
    target_time = float(sys.argv[3])
    vlayern     = int(sys.argv[4])
    #----------------------#

    [dt,nt]              = read_time_info(schout_dir)
    print(dt,nt)
    [scho_fname,t_index] = find_outputs_including_target_time(dt, nt, target_time)

    extract_xyv(schout_dir, scho_fname, t_index, target_var, vlayern, 1)
