#PBS -S /bin/sh
#PBS -l nodes=1:ppn=20
#PBS -q batch
#PBS -N schism_TY_icst2
#PBS -V

# CASEs directories 
  #for work_dir in '/home/dbshin/01_WORKS/2020/tongyeong/14_sigma_elevbc_tide_tvd2_sflux_itur_off_itur_3KEKC/' 
  #do
  #done
scrt_dir='/home/dbshin/git/schism-related-script-master'

#work_dir='/home/dbshin/01_workon/01_SCHISM_model/02_Application/01_EastSea/600_alongTopo/628_monthlyERA5_monthlyHYCOM_nudge_island_refine_for_comparing_to_zgrid/'
work_dir='/home/dbshin/01_workon/01_SCHISM_model/02_Application/01_EastSea/600_alongTopo/999_hycom_intit_visit_tmp'

rm -rf $work_dir/hyc-bc
mkdir $work_dir/hyc-bc


# 3. Scripts Run ------------------------------------------#
echo `which python`

cd $work_dir/hyc-bc
cp -a $scrt_dir/hyc-scripts ./
cd ./hyc-scripts/3D

perl ./hycom_gara_pic.auto.pl	

cd ../../../
#rm -rf ./hyc-bc
