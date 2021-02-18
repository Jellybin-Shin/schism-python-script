#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
#TT=10800 21600 32400 43200 54000 64800 75600 86400 97200 108000 118800 129600 140400 151200 162000 172800 183600 194400 205200 216000 226800 237600 248400 259200 270000
n_of_vlayer=11
window_x_min=128.35
window_x_max=128.85
window_y_min=34.85
window_y_max=35.25

resolution=0.10
fixed_radius=1.0

coastfile='/home/dbshin/01_workon/01_SCHISM_model/02_Application/03_JinhaeBay/000.first_grid/004.barotropic_ts/gmt_outputs/Jinhae_shorelines/shoreline_ll.gmt'

for T in `seq 7200 10800 1296000`
do
echo " "
echo DRAWING FIGS AT $T
echo " "

## Sea Surface Hegith
#window_v_min=-1
#window_v_max=1
#v_interval=0.1
#. ./01.scripts/01.ssh-gmt.sh

# Sea Surface Temperature
window_v_min=20.
window_v_max=26.
v_interval=1.0
. ./01.scripts/02.sst-gmt.sh

# Sea Surface UV
window_v_min=0.
window_v_max=0.5
v_interval=0.05
. ./01.scripts/03.hvel-gmt.sh
done

exit
