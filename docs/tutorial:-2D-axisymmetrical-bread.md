# Case description
This tutorial shows a two-dimensional internal simulation of the bread in the oven. External transport is resolved by custom mixed boundary conditions. The tutorial is located in `tutorials/breadAx2D` and can be:
1. run directly as prepared by `Allrun` script in `tutorials/breadAx2D`folder, or
2. modified and run by `runBreadAx2D.py` in `pyCtrlScripts/breadAx2D`.

## Geometry and computational mesh description
<img width="1687" height="450" alt="twoBreadsLength" src="https://github.com/hlavatytomas/breadBakingFoam/blob/main/docs/twoBreadsLength.png" />

Geometry for the tutorial is taken from the work of Zhang (https://doi.org/10.1002/aic.10518). The computational mesh is prepared using `system/blockMeshDict`, which is pre-prepared in the tutorial case. `blockMeshDict` file with the modified dimesions (radius, height and lenght of the arc) or the computational cell size can be generated using `pyCtrlScripts/runBreadAx2D.py` script by changing `'''Geometry parameters'''` part:
```
'''Geometry parameters'''
typeOfMesh = '2DZhang'
mSStep = 0.1e-2 # -- aproximate computational cell size
rLoaf = 3.6e-2  # -- loaf radius                
hLoaf = 3.5e-2  # -- loaf height
arcL = 0.008    # -- length of the arc at the side of the bread
```

There are three diferent types of the geometry boundaries:
* wedge (depicted in green),
* bottom (depicted in blue), and 
* side (depicted in red).

## Boundary conditions


## Internal transfer parameters
