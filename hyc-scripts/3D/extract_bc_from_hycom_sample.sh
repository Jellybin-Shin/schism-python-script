#PBS -S /bin/sh
#PBS -l nodes=1:ppn=20
#PBS -q batch
#PBS -N schism_TY_icst2
#PBS -V

# CASEs directories 
  #for work_dir in '/home/dbshin/01_WORKS/2020/tongyeong/14_sigma_elevbc_tide_tvd2_sflux_itur_off_itur_3KEKC/' 
  #do
  #done
scrt_dir='/home/dbshin/01_WORKS/git/schism-related-script'
#work_dir='/home/dbshin/01_WORKS/2020/tongyeong/14_sigma_elevbc_tide_tvd2_sflux_itur_off_itur_3KEKC/'
#work_dir='/home/Work2/home/dbshin/2020/eastsea/00_modelsetting/00_SET/'
work_dir='/home/Work2/home/dbshin/2020/eastsea/02_openbc1/'
rm -rf $work_dir/hyc-bc
mkdir $work_dir/hyc-bc


# 3. Scripts Run ------------------------------------------#
echo `which python`

cd $work_dir/hyc-bc
cp -a $scrt_dir/hyc-scripts ./
cd ./hyc-scripts/3D

perl ./auto.pl	

cd ../../../
rm -rf ./hyc-bc
