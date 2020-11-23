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
$hycom_dir="/home/Work2/home/dbshin/99_EXT_DATAS/HYCOM_DATA/20200922";

$thisdir=cwd();

#UTM grid
system("ln -sf ../../../hgrid.* .");
system("ln -sf ../../../vgrid.in .");
system("ln -sf $hycom_dir/*.nc .");


system("./gen_gr3.pl");

#generate hotstart.nc and *D.th.nc
system("./gen_hot_3Dth_from_hycom.exe");


system("cp *D.th.nc ../../../");
system("cp hotstart.nc ../../../");

unlink("../*D.th.nc");
unlink("./hotstart.nc");

print(" Done.\n")
