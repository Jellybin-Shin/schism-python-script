'''
Generate the schism B.C from the DTU(2010) tidal model.
The tidal constituents interpolate at boundary nodes.
the information of boundary nodes is read from hgrid.
'''

import numpy as np, pandas as pd, sys
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.interpolate import interp2d

class gen_tidal_constituents:
    
    def __init__(self, working_dir, data_dir, box=[-180,180,-90,90]):
        self.box =box
        self.working_dir = working_dir
        self.data_dir = data_dir
        #
        file_dir=self.data_dir+"/K1.d"
        f = open(file_dir,'r')
        flines = f.readlines()
        row, col         = np.array(flines[2].split(), dtype=np.int32)
        self.lat_min, self.lat_max = np.array(flines[3].split(), dtype=np.float32)
        self.lon_min, self.lon_max = np.array(flines[4].split(), dtype=np.float32)
        f.close()
        
    def read_utm(self):
        print('Reading UTM data...')
        utm = pd.read_csv(self.data_dir+"UTM.csv",names=['lon','lat'])
        if self.box != [utm['lon'][0],utm['lon'][1],utm['lat'][0],utm['lat'][1]]:
            raise Exception("Box boundary doesn't match")
        self.utmx = np.array(utm['lon'][2:])
        self.utmy = np.array(utm['lat'][2:])
        print('Reading UTM data... Done')

    def read_dtu(self, tidal_con,lon_interval,lat_interval):
        print('Reading DTU data...')
        self.tidal_con =tidal_con
        file_dir=self.data_dir+"/{}.d".format(tidal_con)
        f = open(file_dir,'r')
        flines = f.readlines()
        # row, col         = int(flines[2].split()[0]), int(flines[2].split()[1])
        row, col         = np.array(flines[2].split(), dtype=np.int32)
        self.lat_min, self.lat_max = np.array(flines[3].split(), dtype=np.float32)
        self.lon_min, self.lon_max = np.array(flines[4].split(), dtype=np.float32)

        self.AMP_o = np.zeros([row,col])
        self.PHS_o = np.zeros([row,col])
        
        for ln in range(0,row):
            self.AMP_o[ln] = np.array(flines[7+ln].split(), dtype=np.float32)
            self.PHS_o[ln] = np.array(flines[14+row+ln].split(), dtype=np.float32)
        
        self.lon = np.linspace(self.lon_min,self.lon_max,1+int((self.lon_max-self.lon_min)//lon_interval))
        self.lat = np.linspace(self.lat_min,self.lat_max,1+int((self.lat_max-self.lat_min)//lat_interval))
        
        if self.box != [-180,180,-90,90] :
            self.boxidxlon = (self.lon>box[0]) & (self.lon<box[1])
            self.boxidxlat = (self.lat>box[2]) & (self.lat<box[3])
            AMP_t = self.AMP_o[self.boxidxlat]
            PHS_t = self.PHS_o[self.boxidxlat]
            self.AMP = AMP_t.T[self.boxidxlon].T
            self.PHS = PHS_t.T[self.boxidxlon].T
            self.lon = self.lon[self.boxidxlon]
            self.lat = self.lat[self.boxidxlat]
        print('Reading DTU data... Done')



    def regular_grid(self):
        print('Regularization...')
        
        UTMX = np.arange(min(self.utmx),max(self.utmx),10000)
        UTMY = np.arange(min(self.utmy),max(self.utmy),10000)
        self.UTMX, self.UTMY = np.meshgrid(UTMX, UTMY)
        self.UTMA = griddata((self.utmx, self.utmy),self.AMP.flatten(),(self.UTMX, self.UTMY),method='cubic')
        self.UTMP = griddata((self.utmx, self.utmy),self.PHS.flatten(),(self.UTMX, self.UTMY),method='cubic')

    def figplot(self):
        # plt.figure(num=1)
        # plt.contourf(self.UTMX, self.UTMY, self.UTMA,levels=30)
        # plt.colorbar()
        # plt.savefig('a.png')
        # plt.figure(num=2)
        # plt.contourf(self.UTMX, self.UTMY, self.UTMP,levels=30)
        # plt.colorbar()
        # plt.savefig('p.png')
        plt.figure(num=2)
        LL1, LL2 = np.meshgrid(self.lon, self.lat)
        plt.contourf(LL1, LL2, self.AMP_o,levels=30,vmin=0, vmax=250)
        plt.colorbar()
        plt.savefig('a.png')


    def interpolation(self,x,y):
        print('Interpolation...')
        buff = 50000
        xmin = min(x)-buff; xmax = max(x)+buff
        ymin = min(y)-buff; ymax = max(y)+buff
        xidx = (self.UTMX[0]>xmin)&(self.UTMX[0]<xmax)
        yidx = (self.UTMY.T[0]>ymin)&(self.UTMY.T[0]<ymax)
        cUTMX = self.UTMX[yidx].T[xidx].T
        cUTMY = self.UTMY[yidx].T[xidx].T
        cUTMA  =  self.UTMA[yidx].T[xidx].T
        cUTMP  =  self.UTMP[yidx].T[xidx].T

        f_a = interp2d(cUTMX[0], cUTMY.T[0], cUTMA, kind='cubic')
        f_p = interp2d(cUTMX[0], cUTMY.T[0], cUTMP, kind='cubic')
        
        # outdata=pd.DataFrame(columns=['X','Y','Amp','Pha'])
        outdata=np.zeros([len(x),4])
        for ii in range(0, len(x)):
            amp = f_a(x[ii], y[ii])/100
            pha = f_p(x[ii], y[ii])
            outdata[ii] = [x[ii], y[ii], amp, pha]
        
        df=pd.DataFrame(outdata)
        df.to_csv(self.working_dir+"/harm/{}.csv".format(self.tidal_con),header=None, index=None, sep='\t')
        print('Interpolation... Done')
        
    def gen_lonlat(self,lon_interval,lat_interval):
        lon = np.linspace(self.lon_min,self.lon_max,1+int((self.lon_max-self.lon_min)//lon_interval))
        lat = np.linspace(self.lat_min,self.lat_max,1+int((self.lat_max-self.lat_min)//lat_interval))
        if self.box != [-180,180,-90,90] :
            print('aa')
            print(np.shape(lon))
            print(np.shape(lat))
            self.boxidxlon = (lon>box[0]) & (lon<box[1])
            self.boxidxlat = (lat>box[2]) & (lat<box[3])
            lon = lon[self.boxidxlon]
            lat = lat[self.boxidxlat]
            print(np.shape(lon))
            print(np.shape(lat))
        LON,LAT = np.meshgrid(lon,lat)
        np.savetxt(self.working_dir+'/LON.csv' ,LON,delimiter=',')
        np.savetxt(self.working_dir+'/LONf.csv',LON.flatten(),delimiter=',')
        np.savetxt(self.working_dir+'/LAT.csv' ,LAT,delimiter=',')
        np.savetxt(self.working_dir+'/LATf.csv',LAT.flatten(),delimiter=',')


if __name__ == '__main__' :

    box = [110,150,20,60]

    working_dir = sys.argv[1]

    data_dir = "/home/Work2/home/dbshin/99_EXT_DATAS/DTU_DATA/"

    tidal = ['M2','S2','K1','O1','N2','K2','P1','Q1']

    ixy = pd.read_csv(working_dir+'/bc0.ixy', names=['idx','x','y'], sep='\s+')

    x = ixy['x'].values
    y = ixy['y'].values
    
    gtc = gen_tidal_constituents(working_dir,data_dir)#, box=box)

    for ii,td in enumerate(tidal) :
        gtc.read_dtu(tidal[ii],0.125,0.125)
        # gtc.read_utm()
        # gtc.regular_grid()
        gtc.figplot()
        # gtc.interpolation(x,y)
        print('============================')
        print(td,'is done')