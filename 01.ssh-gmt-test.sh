#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
var=elev
var_nic=SSH
T=14400 #"1200 2400 14400 15600 259200 270000"
window_x_min=128.35
window_x_max=128.85
window_y_min=34.85
window_y_max=35.25
window_v_min=0.0
window_v_max=0.2
v_interval=0.02


for tt in $T
do
  # SSH
  python ./gmt-scripts/python_scripts/sch2xyv.py ../outputs ./  $var $tt -1  
  filename=${var}_t-${tt}_vl--1
  gmt begin ${var_nic}_t-${tt}
    gmt nearneighbor -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -I0.05m -S1.5k -G$filename.nc $filename.xyv
  	gmt grdimage $filename.nc -JM6i -Cseafloor -B
    gmt grdcontour $filename.nc -JM6i -C$v_interval -A0.06 -B
    gmt colorbar -DJRM+o1.5c/0+e+mc -By+0.0lm
   	#gmt grdimage $filename.nc -JM6i -I+d
    #gmt coast -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -Ggray
  gmt end
    
  # SST
  # python ./gmt-scripts/python_scripts/sch2xyv.py ../outputs ./  temp $tt 0
done