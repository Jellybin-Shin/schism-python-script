import wget, sys
from datetime import date, timedelta

[syear,smonth,sday]=sys.argv[1:4]
[eyear,emonth,eday]=sys.argv[4:7]

sdate=time=date(int(syear),int(smonth),int(sday))
edate=date(int(eyear),int(emonth),int(eday))

delta=edate-sdate

var_tag=['ssh?var=surf_el','uv3z?var=water_u&var=water_v','ts3z?var=salinity&var=water_temp']
var_name=['SSH','UV','TS']

for i in range(delta.days + 1):
    dday = sdate + timedelta(days=i)
    print('{}-{}-{}'.format(dday.year, dday.month, dday.day))
    for vv in range(len(var_tag)):
        url='https://ncss.hycom.org/thredds/ncss/GLBy0.08/expt_93.0/{0}&north=50&west=110&east=150&south=30&horizStride=1&time_start={1}-{2}-{3}T00%3A00%3A00Z&time_end={1}-{2}-{3}T23%3A59%3A59Z&timeStride=1&addLatLon=true&accept=netcdf4'.format(var_tag[vv],dday.year,dday.month,dday.day);
        wgetfname=wget.download(url, out='./{}_{}.nc'.format(var_name[vv], i+1), bar=None);
        print('Done.. /{}_{}.nc'.format(var_name[vv], i+1))