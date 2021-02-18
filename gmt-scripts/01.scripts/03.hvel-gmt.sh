#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
var=hvel
var_nic=UVTOP

n_of_vlayer_=`expr $n_of_vlayer - 1`
qopt=0.07i


echo $window_v_min $window_v_max $v_interval
for tt in $T
do
  python ./01.scripts/python_scripts/sch2xyv.py ../outputs ./  $var $tt $n_of_vlayer_
  filename=./dum/${var}_t-${tt}_vl-${n_of_vlayer_}
  gmt begin ${var_nic}/${var_nic}_t-${tt} pdf,png
    gmt nearneighbor -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -I${resolution}m -S${fixed_radius}m -G$filename.nc $filename.xyv
    gmt nearneighbor -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -I${resolution}m -S${fixed_radius}m -G${filename}1.nc $filename.xyv2
    gmt nearneighbor -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -I${resolution}m -S${fixed_radius}m -G${filename}m.nc $filename.xym
    gmt makecpt -Cno_green -T${window_v_min}/${window_v_max}/$v_interval
  	gmt grdimage ${filename}m.nc -JM10i
    gmt grdcontour ${filename}m.nc -JM10i -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -A0.4
    gmt colorbar -DJRM+o1.5c/0+e+mc -By+0.0lm -Ba

    gmt grdvector $filename.nc ${filename}1.nc -W1p -JM10i -Q${qopt}+e+h0.5 -G0 -Ix3 -S2i
    #gmt coast -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -W0.1p,black -JM10i -Gdarkseagreen2 -Ba1f0.05 -BWSne+t"UVTOP_T="$T
    gmt psxy -Gdarkseagreen2 -JM10i -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max}  -W1p $coastfile -Ba1f0.05 -BWSne+t$var_nic" 2020/08/01 00:00+"`expr $T / 3600 + 1`"hour"
  gmt end
done
