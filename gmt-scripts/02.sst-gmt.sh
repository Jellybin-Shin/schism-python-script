#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
var=temp
var_nic=SST
vlayer=$((${n_of_vlayer} - 1))

echo $window_v_max
for tt in $T
do
  python ./gmt-scripts/python_scripts/sch2xyv.py ../outputs ./  $var $tt $vlayer
  filename=${var}_t-${tt}_vl-$vlayer
  gmt begin ${var_nic}_t-${tt}
    gmt nearneighbor -R${window_x_min}/${window_x_max}/${window_y_min}/${window_y_max} -I${resolution}m -S${fixed_radius}k -G$filename.nc $filename.xyv
  	gmt grdimage $filename.nc -JM6i -Cseafloor -B
    gmt grdcontour $filename.nc -JM6i -C$v_interval -A0.06 -B
    gmt colorbar -DJRM+o1.5c/0+e+mc -By+0.0lm
  gmt end
done
