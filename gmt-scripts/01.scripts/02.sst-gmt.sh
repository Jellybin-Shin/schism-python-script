#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
var=temp
var_nic=SST
vlayer=$((${n_of_vlayer} - 1))

echo $window_v_max
for tt in $T
do
  python ./01.scripts/python_scripts/sch2xyv.py ../outputs ./  $var $tt $vlayer
  filename=./dum/${var}_t-${tt}_vl-$vlayer
  gmt begin ${var_nic}/${var_nic}_t-${tt} pdf,png
    gmt nearneighbor -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -I${resolution}m -S${fixed_radius}k -G$filename.nc $filename.xyv
    gmt makecpt -Cno_green -T${window_v_min}/${window_v_max}/$v_interval
  	gmt grdimage $filename.nc -JM10i -B
    gmt grdcontour $filename.nc -JM10i -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -A0.5 -B
    gmt colorbar -DJRM+o1.5c/0+e+mc -By+0.0lm -Ba
    #gmt coast -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -W0.1p,black -JM10i -Gdarkseagreen2 -Ba2f0.5g1 -BWSne+t"SST_T="$T
    gmt psxy -Gdarkseagreen2 -JM10i -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -W1p $coastfile  -Ba1f0.05 -BWSne+t$var_nic" 2020/08/01 00:00+"`expr $T / 3600 + 1`"hour"
  gmt end
done
