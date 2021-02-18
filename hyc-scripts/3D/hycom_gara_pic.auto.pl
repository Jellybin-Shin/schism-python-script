#! /usr/bin/perl -w

#load some functions
use File::Copy qw(copy);
use File::Copy qw(move);
use Cwd;

print("You may need to recompile 'gen_hot_3Dth_from_hycom.f90',\n");
print("see an example compiling cmd in the source code.\n");
print("Make sure you have netcdf libraries\n");
#{
#  local( $| ) = ( 1 );
#  print "Press <Enter> or <Return> to continue: \n";
#  my $resp = <STDIN>;
#}

#dirs
#$hycom_dir="/home/Work2/home/dbshin/99_EXT_DATAS/HYCOM_DATA";
$hycom_dir="/home/dbshin/01_workon/01_SCHISM_model/02_Application/01_EastSea/401_eastSeaOnly/501_hycom_monthly_data/OUT/hycom_tmp_visit/";
#$hycom_dir="/home1/ext_datas/HYCOM/2017_schism/merge/";
$thisdir=cwd();

#UTM grid
system("ln -sf ../../../hgrid.* .");
system("ln -sf ../../../vgrid.in .");
system("ln -sf $hycom_dir/*.nc .");


system("./gen_gr3.pl");
system("echo done with gen_gr3.pl");

#generate hotstart.nc and *D.th.nc
system("./gen_hot_3Dth_from_hycom");


system("cp *D.th.nc ../../../");
system("cp hotstart.nc ../../../");

unlink("../*D.th.nc");
unlink("./hotstart.nc");

print(" Done.\n")
