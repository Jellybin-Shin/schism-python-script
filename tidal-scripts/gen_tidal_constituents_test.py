'''
Generate the schism B.C from the DTU(2010) tidal model.
The tidal constituents interpolate at boundary nodes.
the information of boundary nodes is read from hgrid.
'''

import numpy as np, pandas as pd
from scipy.interpolate import griddata

class gen_tidal_constituents:
    
    def __init__(self, working_dir, data_dir, box=[0,360,-90,90]):
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
        utm = pd.read_csv(self.data_dir+"UTM.csv",names=['lon','lat'])
        if self.box != [utm['lon'][0],utm['lon'][1],utm['lat'][0],utm['lat'][1]]:
            raise Exception("Box boundary doesn't match")
        self.utmx = np.array(utm['lon'][2:])
        self.utmy = np.array(utm['lat'][2:])

    def read_dtu(self, tidal_con,lon_interval,lat_interval):
        file_dir=self.data_dir+"/{}.d".format(tidal_con)
        f = open(file_dir,'r')
        flines = f.readlines()
        # row, col         = int(flines[2].split()[0]), int(flines[2].split()[1])
        row, col         = np.array(flines[2].split(), dtype=np.int32)
        self.lat_min, self.lat_max = np.array(flines[3].split(), dtype=np.float32)
        self.lon_min, self.lon_max = np.array(flines[4].split(), dtype=np.float32)

        AMP = np.zeros([row,col])
        PHS = np.zeros([row,col])
        
        for ln in range(0,row):
            AMP[ln] = np.array(flines[7+ln].split(), dtype=np.float32)
            PHS[ln] = np.array(flines[14+row+ln].split(), dtype=np.float32)
        
        if self.box != [0,360,-90,90] :
            lon = np.linspace(self.lon_min,self.lon_max,1+int((self.lon_max-self.lon_min)//lon_interval))
            lat = np.linspace(self.lat_min,self.lat_max,1+int((self.lat_max-self.lat_min)//lat_interval))
            self.boxidxlon = (lon>box[0]) & (lon<box[1])
            self.boxidxlat = (lat>box[2]) & (lat<box[3])
            AMP_t = AMP[self.boxidxlat]
            PHS_t = PHS[self.boxidxlat]
            self.AMP = AMP_t.T[self.boxidxlon].T
            self.PHS = PHS_t.T[self.boxidxlon].T

    def regular_grid(self):
        
        UTMX = np.arange(min(self.utmx),max(self.utmx),10000)
        UTMY = np.arange(min(self.utmy),max(self.utmy),10000)
        self.UTMX, self.UTMY = np.meshgrid(UTMX, UTMY)

        self.UTMA = griddata((utmx,utmy),self.AMP.flatten(),(self.UTMX, self.UTMY),method='cubic')
        self.UTMP = griddata((utmx,utmy),self.PHS.flatten(),(self.UTMX, self.UTMY),method='cubic')
        
    def gen_lonlat(self,lon_interval,lat_interval):
        lon = np.linspace(self.lon_min,self.lon_max,1+int((self.lon_max-self.lon_min)//lon_interval))
        lat = np.linspace(self.lat_min,self.lat_max,1+int((self.lat_max-self.lat_min)//lat_interval))
        if self.box != [0,360,-90,90] :
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


    def interpolation(self,x,y):
        buff = 10000
        xmin = min(x)-buff; xmax = max(x)+buff
        ymin = min(y)-buff; ymax = max(y)+buff
        xidx = (self.UTMX[0]>xmin)&(self.UTMX[0]<xmax)
        yidx = (self.UTMY.T[0]>ymin)&(self.UTMY.T[0]<ymax)
        cUTMY = self.UTMY[yidx].T[xidx].T
        cUTMX = self.UTMX[yidx].T[xidx].T
        cAMP  =  self.AMP[yidx].T[xidx].T
        
        print(np.shape(cUTMX))
        print(np.shape(cUTMY))
        print(np.shape(cAMP))
        print('aaaa')

        f_z = interp2d(cUTMX, cUTMY, cAMP)
        yy = f_z(x[0], y[0])

        print(yy)

# y_pred = gp.predict(the_grid_data_on_which _you_need_to_predict)


if __name__ == '__main__' :

    box = [110,150,20,60]

    working_dir = "."
    data_dir = "/home/Work2/home/dbshin/99_EXT_DATAS/DTU_DATA/"

    tidal = ['M2','S2','K1','O1','N2','K2','P1','Q1']
    
    gtc = gen_tidal_constituents(working_dir,data_dir,box=box)


    gtc.read_dtu(tidal[0],0.125,0.125)
    
    gtc.read_utm()


    x = [625335.70555453]
    y = [3857225.8388886]

    # gtc.interpolation(x,y)