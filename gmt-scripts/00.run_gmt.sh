#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
T=86400 #"1200 2400 14400 15600 259200 270000"
n_of_vlayer=48
window_x_min=126.0
window_x_max=143.0
window_y_min=33.0
window_y_max=52.0

resolution=5.0
fixed_radius=20.0


# Sea Surface Hegith
window_v_min=-1.5
window_v_max=1.5
v_interval=0.1
. ./gmt-scripts/01.ssh-gmt.sh

# Sae Surface Temperature
window_v_min=0.0
window_v_max=25.
v_interval=1.0
. ./gmt-scripts/02.sst-gmt.sh


exit
