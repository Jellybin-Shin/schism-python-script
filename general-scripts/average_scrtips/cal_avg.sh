source ~/anaconda3/etc/profile.d/conda.sh
vs='/home/dbshin/01_WORKS/git/schism-related-script/visit-scripts'

for fn in 904 905 #510 511 512 513 514
do
  ffn=./${fn}_*
  echo $ffn
  cd ./$ffn
    cd ./outputs
      for ii in `ls schout_[1-99].nc`
      do
        ncwa -b -a time $ii ${ii}_avg.nc
      done
      cd ..
    cd ..
done

