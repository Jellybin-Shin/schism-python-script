'''
This script needs : 
  - visit
  - python 2.7
  - numpy  
'''
## LIBRARIES AND LAUNCH VISIT ##
import sys, os, numpy as np
visit_dir = "/home/dbshin/99_libraries/visit" 
# visit_dir = "/home/dbshin/03_utility/visit2.10.2"  server80
sys.path.append("{}/2.10.2/linux-x86_64/lib/site-packages".format(visit_dir))

from visit import *
Launch()
# ========  Templetes  ======== #
elev = PseudocolorAttributes()
elev.min, elev.minFlag = -1.0, 1
elev.max, elev.maxFlag = 1.0, 1

hvelm = PseudocolorAttributes()
hvelm.min, hvelm.minFlag = 0.0, 1
hvelm.max, hvelm.maxFlag = 0.5, 1

zs = SliceAttributes()
zs.originType = zs.Point
zs.originPoint = (0,0,-5)
zs.normal = (0,0,1)
zs.axisType = zs.ZAxis


hvel = VectorAttributes()
hvel.min, hvel.minFlag = 0.0, 1
hvel.max, hvel.maxFlag = 0.5, 1
hvel.colorByMag = 0
hvel.scaleByMagnitude = 1
hvel.scale = 0.25
hvel.useStride = 1
hvel.stride = 1

save = SaveWindowAttributes()
save.fileName = "vector"
save.width, save.height = 1024,768
save.screenCapture = 0
# ============================= #

# Step 1: Open a database
OpenDatabase("../schout_*.nc database")

# Step 2: Add plots
AddPlot("Pseudocolor", "hvel_magnitude")
SetPlotOptions(hvelm)
AddOperator("Slice")
SetOperatorOptions(zs)

AddPlot("Vector", "hvel")
SetPlotOptions(hvel)
AddOperator("Slice")
SetOperatorOptions(zs)


# Step 3: Draw the plots
DrawPlots()

# Step 4: Animate through time and asve images
tstride = 10
time   = np.arange(1,TimeSliderGetNStates(),tstride)
SetSaveWindowAttributes(save)
for state in time:
  SetTimeSliderState(state)
  SaveWindow()

# SetTimeSliderState(time[ii]); ii = ii +1
