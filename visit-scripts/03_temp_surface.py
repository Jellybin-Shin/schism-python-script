'''
This script needs : 
  - visit
  - python 2.7
  - numpy  
'''
## LIBRARIES AND LAUNCH VISIT ##
import sys, os, numpy as np
visit_dir = "/home/dbshin/03_utility/visit2.10.2" 
sys.path.append("{}/2.10.2/linux-x86_64/lib/site-packages".format(visit_dir))

from visit import *
Launch()
# ========  Templetes  ======== #
elev = PseudocolorAttributes()
elev.min, elev.minFlag = -1.0, 1
elev.max, elev.maxFlag = 1.0, 1

hvelm = PseudocolorAttributes()
hvelm.min, hvelm.minFlag = 0.0, 1
hvelm.max, hvelm.maxFlag = 1.25, 1

zs = SliceAttributes()
zs.originType = zs.Point
zs.originPoint = (0,0,-5)
zs.normal = (0,0,1)
zs.axisType = zs.ZAxis


hvel = VectorAttributes()
hvel.min, hvel.minFlag = 0.0, 1
hvel.max, hvel.maxFlag = 1.25, 1
hvel.colorByMag = 0
#hvel.scaleByMagnitude = 1
#hvel.scale = 0.2
hvel.useStride = 1
hvel.stride = 10

save = SaveWindowAttributes()
save.fileName = "temp_surface"
save.width, save.height = 1024,768
save.screenCapture = 0

# ============================= #

for ii in np.arange(1,182,5):
  # Step 1: Open a database
  #OpenDatabase("../schout_*.nc database")
  OpenDatabase("../schout_{}.nc".format(ii))

  # Step 2: Add plots
  AddPlot("Pseudocolor", "temp_surface")
  # SetPlotOptions(elev)
  # AddOperator("Slice")
  # SetOperatorOptions(zs)

  # Step 3: Draw the plots
  DrawPlots()
  v = GetView2D()

  # Step 4: Set time
  # SetSaveWindowAttributes(save)
  # T = TimeSliderGetNStates()
  # for tt in np.arange(T):
  #   SetTimeSliderState(T)
  #   SaveWindow()
  #   DeleteActivePlots()
  #   DeleteActivePlots()
  SetTimeSliderState(0)
  SetSaveWindowAttributes(save)
  SaveWindow()
  DeleteActivePlots()
