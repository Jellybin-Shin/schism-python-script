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

wvelm = PseudocolorAttributes()
wvelm.min, wvelm.minFlag = 0.0, 1
wvelm.max, wvelm.maxFlag = 12, 1

zs = SliceAttributes()
zs.originType = zs.Point
zs.originPoint = (0,0,-5)
zs.normal = (0,0,1)
zs.axisType = zs.ZAxis


wvel = VectorAttributes()
wvel.min, wvel.minFlag = 0.0, 1
wvel.max, wvel.maxFlag = 12, 1
wvel.colorByMag = 0
wvel.scaleByMagnitude = 1
wvel.scale = 0.1
wvel.useStride = 1
wvel.stride = 1

save = SaveWindowAttributes()
save.fileName = "wind_vector"
save.width, save.height = 1024,768
save.screenCapture = 0
# ============================= #

# Step 1: Open a database
OpenDatabase("../schout_*.nc database")

# Step 2: Add plots
AddPlot("Pseudocolor", "wind_speed_magnitude")
SetPlotOptions(wvelm)
SetOperatorOptions(zs)

AddPlot("Vector", "wind_speed")
SetPlotOptions(wvel)
SetOperatorOptions(zs)


# Step 3: Draw the plots
DrawPlots()

# Step 4: Animate through time and asve images
tstride = 11
time   = np.arange(1,TimeSliderGetNStates(),tstride)
SetSaveWindowAttributes(save)
for state in time:
  SetTimeSliderState(state)
  SaveWindow()

# SetTimeSliderState(time[ii]); ii = ii +1
