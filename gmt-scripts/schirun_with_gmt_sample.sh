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
work_dir='/home/dbshin/01_WORKS/2020/tongyeong/14_sigma_elevbc_tide_tvd2_sflux_itur_off_itur_3KEKC/'
source ~/anaconda3/etc/profile.d/conda.sh

rm -rf $work_dir/gmt_outputs
mkdir $work_dir/gmt_outputs


# 3. GMT Run ------------------------------------------#
conda activate gmt_env
echo `which python`
cd $work_dir/gmt_outputs
cp -a $scrt_dir/gmt-scripts ./
ls ./gmt-scripts/python_scripts

sh ./gmt-scripts/01.ssh-gmt-test.sh

rm -rf ./gmt-scripts
conda deactivate

exit

#=============================================================================

# 1. Model Run ----------------------------------------#
export NNODE=`wc $PBS_NODEFILE|awk '{print $1}'`

rm -rf run_time.dat # log total calculation time. 
date > run_time.dat 
mpirun -n 20 -machinefile $PBS_NODEFILE ./model_intel.x
date >> run_time.dat

# 2. Combining outputs --------------------------------#       #How can define the last number?#
perl $work_dir/autocombine_MPI_elfe.pl 1 30 

# 3. GMT Run ------------------------------------------#
conda activate gmt_envs
cd $work_dir/gmt_outputs
cp -a $scrt_dir/gmt-scripts ./
sh ./gmt-scripts/01.ssh-gmt-test.sh
rm -rf ./gmt-scripts
conda deactivate gmt_envs
