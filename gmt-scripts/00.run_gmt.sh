#!/bin/sh
#start at ./work_dir/gmt-outputs

# Variable
T=14400 #"1200 2400 14400 15600 259200 270000"
n_of_vlayer=6
window_x_min=128.35
window_x_max=128.85
window_y_min=34.85
window_y_max=35.25

resolution=0.05
fixed_radius=1.5


# Sea Surface Hegith
window_v_min=0.0
window_v_max=0.2
v_interval=0.02
. ./gmt-scripts/01.ssh-gmt.sh

# Sae Surface Temperature
window_v_min=20.0
window_v_max=21.
v_interval=0.2
. ./gmt-scripts/02.sst-gmt.sh


exit
