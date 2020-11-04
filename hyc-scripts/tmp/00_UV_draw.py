#%matplotlib inline
import numpy as np, pandas as pd, datetime, netCDF4 as nc4, glob, os, sys
from numpy import ma
# import matplotlib.pyplot as plt
import pylab as plt


def read_file_list(work_dir):
    
    # Read First schout_1.nc
    file_list = glob.glob('{}/UV_*nc'.format(work_dir))
    if len(file_list) != 0 :
        print('\n# File List :\n{}\n~\n{}'.format(file_list[0],file_list[-1]))
    else : raise Exception('There is no UV file in working directory')

    return file_list

def read_UV(work_dir,nc_dataset,stride):
    os.makedirs(work_dir+'/outputs', exist_ok=True)
    depth = nc_dataset.variables['depth'][:]
    time = nc_dataset.variables['time'][:]
    lat= nc_dataset.variables['lat'][:]
    lon= nc_dataset.variables['lon'][:]
    LON,LAT = np.meshgrid(lon,lat)

    uu = nc_dataset.variables['water_u']
    vv = nc_dataset.variables['water_v']
    uuoffset = getattr(uu,'add_offset')
    vvoffset = getattr(vv,'add_offset')
    uuscale  = getattr(uu,'scale_factor')
    vvscale  = getattr(vv,'scale_factor')
    print(uuscale,uuoffset)
    uf = np.array(uu[:],'f')
    vf = np.array(vv[:],'f')
    uf = np.where(uf!=uu._FillValue, uf, np.nan)
    vf = np.where(vf!=vv._FillValue, vf, np.nan)
    # uf = np.where(uf!=uu._FillValue, uf*uuscale+uuoffset, np.nan)
    # vf = np.where(vf!=vv._FillValue, vf*vvscale+vvoffset, np.nan)
    
    print('\n# num of vertical Layer  = {} '.format(len(depth)))
    print('\n# num of time step       = {} '.format(len(time)))
    levels = np.arange(0,1.1,0.1)
    for ti, tt in enumerate(time) :
        for di, dd in enumerate(depth[:20]) :
            print(np.nanmax(uf[ti,di,:,:]))
            print(np.nanmin(uf[ti,di,:,:]))
            fig, ax = plt.subplots(figsize=(10,10), dpi=300, facecolor='w')
            cntr = ax.contourf(LON[::stride,::stride],LAT[::stride,::stride],(uf[ti,di,::stride,::stride]**2+vf[ti,di,::stride,::stride]**2)**0.5,levels, cmap=plt.cm.jet)
            cntr.cmap.set_under('k')
            plt.colorbar(cntr, ax=ax)
            # plt.clim(0, 1)
            m = ax.quiver(LON[::stride,::stride],LAT[::stride,::stride],uf[ti,di,::stride,::stride],vf[ti,di,::stride,::stride],angles='xy', scale_units='xy',scale=1, width=0.001,headwidth=5)
            qk = ax.quiverkey(m, 0.3, 0.7, 1, '1 m/s', coordinates='figure')
            print('saving.... t={}_d={}.png'.format(tt,str(dd).zfill(6)))
            plt.savefig('{}/outputs/t={}_d={}.png'.format(work_dir, tt,str(dd).zfill(6)),dpi=300)
            plt.close(fig)

            # if di == 1 : raise Exception('!!')




if __name__ == "__main__" : 
    work_dir  = "/home/dbshin/01_WORKS/99_EXT_DATAS/HYCOM_DATA"
    file_list = read_file_list(work_dir)
    for ii in range(0,1):
        nc_dataset = nc4.Dataset(file_list[ii],"r",format="netcdf4")
        stride = 2
        read_UV(work_dir,nc_dataset, stride)


