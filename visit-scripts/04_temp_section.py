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
zs.originPoint = (700000, 4000000, 0)
zs.axisType = zs.Arbitrary  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
upAxis = (2, -1, 0)


hvel = VectorAttributes()
hvel.min, hvel.minFlag = 0.0, 1
hvel.max, hvel.maxFlag = 1.25, 1
hvel.colorByMag = 0
#hvel.scaleByMagnitude = 1
#hvel.scale = 0.2
hvel.useStride = 1
hvel.stride = 10

temp = PseudocolorAttributes()
temp.min, temp.minFlag = 0.0,1 

save = SaveWindowAttributes()
save.fileName = "vector"
save.width, save.height = 1024,768
save.screenCapture = 0

# ============================= #

for ii in np.arange(1,2):#182,5):
  # Step 1: Open a database
  #OpenDatabase("../schout_*.nc database")
  OpenDatabase("../schout_{}.nc".format(ii))

  # Step 2: Add plots
  AddPlot("Pseudocolor", "temp")
  SetPlotOptions(temp)
  AddOperator("Slice")
  SetOperatorOptions(zs)

  # AddOperator("Slice")
  # SetOperatorOptions(zs)

  # Step 3: Draw the plots
  DrawPlots()

  # Step 4: Set time
  # SetSaveWindowAttributes(save)
  # T = TimeSliderGetNStates()
  # for tt in np.arange(T):
  #   SetTimeSliderState(T)
  #   SaveWindow()
  #   DeleteActivePlots()
  #   DeleteActivePlots()
  SetTimeSliderState(0)
  SaveWindow()
  DeleteActivePlots()
