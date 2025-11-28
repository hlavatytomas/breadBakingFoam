# Case description and setup
This tutorial shows a two-dimensional internal simulation of the bread in the oven. External transport is resolved by custom mixed boundary conditions. The tutorial is located in `tutorials/breadAx2D` and can be:
1. run directly as prepared by `Allrun` script in `tutorials/breadAx2D`folder, or
2. modified and run by `runBreadAx2D.py` in `pyCtrlScripts/breadAx2D`.

## Geometry and computational mesh description
<img alt="twoBreadsLength" src="twoBreadsLength.png" />

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
The parameters for the internal transfer in the bread can be changed directly in the `constant/transportProperties` and `constant/thermophysicalProperties` or in `'''Internal transport parameters'''` section of the control python script (`pyCtrlScripts/runBreadAx2D.py`).

```
'''Internal transport parameters'''
# -- free volumetric difusivity of the water vapors in CO2 at 300 K
DFree = 2.22e-6 

# -- heat conductivity of the dough material with porosity 0, i.e. the 
# -- absolute term in equation (5) in 
# -- https://doi.org/10.1016/j.fbp.2008.04.002
lambdaS = 0.447 

perm = 0.9e-12  # -- bread permeability 

# -- heat capacities for the individual phases
CpS = 700   # -- solid phase
CpG = 853  # -- CO2
CpVapor = 1878 # -- water vapors
CpL = 4200  # -- liquid phase

# -- mass densities for the individual phases
rhoS = 700  # -- solid density    
rhoL = 1000  # -- liquid density   
```

`DFree` parameter sets up the free volumetric diffusivity of the water vapors in carbon dioxide. The temperature and composition dependence of the effective difusivity is then calculated directly in the solver. `lambdaS` sets up the heat conductivity of the dough material with zero porosity, i.e. the absolute term in equation (5) in https://doi.org/10.1016/j.fbp.2008.04.002 that is used for calculation of the effective heat conductivity. Specific heat capacities and mass densities can be then changed by `Cp` and `rho` parameters.

## Evaporation and fermentation
Evaporation is calculated using Hertz-Knudsen equation while the needed water activity is calculated using Oswin model with parameters measured in https://doi.org/10.1016/0260-8774(91)90020-S. Fermentation kinetics is taken directly from equation (32) in https://doi.org/10.1002/aic.10518. The paramters for all the relations for evaporation and fermentation evaluation can be changed in `constant/reactiveProperties` file or in `'''Evaporation and CO2 generation parameters'''` section of the control python script (`pyCtrlScripts/runBreadAx2D.py`).
```
'''Evaporation and CO2 generation parameters'''
# -- evaporation / condensation coeficient in Hertz-Knudsen equation
kMPC = 0.42

# -- parameters for Oswin model (https://doi.org/10.1016/0260-8774(91)90020-S)
evCoef1 = -0.0056
evCoef2 = 5.5

# -- pre-exponential factor and Tm in CO2 generation kinetics 
# -- in equation (32) in https://doi.org/10.1002/aic.10518
R0 = 22e-4 
Tm = 314
```
`kMPC` sets up the evaporation coefficient in the Hertz-Knudsen formula. `evCoef1` and `evCoef` are the coefficients for the Oswin model for water activity. Finally, `R0` and `Tm` are the pre-exponential factor and temperature of the fermentation maximum in CO2 generation kinetics.

## Mechanical properties
Bread Youngs modulus and Poisson ratio can be changed directly in `constant/mechanicalProperties` file or in `'''Mechanical properties'''` section of the control python script (`pyCtrlScripts/runBreadAx2D.py`).
```
'''Mechanical properties'''
withDeformation = 1 # -- turn on (1) /off (0) deformation
nu = 0.15   # -- Poisson ratio
E = 12000   # -- Youngs modulus
```

# Running the tutorial
As written above, the tutorial can be either run directly by `Allrun` script in tutorial directory `tutorials/breadAx2D` or by control python script `pyCtrlScripts/runBreadAx2D.py` which allows further setup. 
```
# CASE FOLDERS==========================================================
baseCaseDir = '../tutorials/breadAx2D/' # -- base case for simulation
outFolder = '../ZZ_cases/00_breads/breadAx2D/'

# WHAT SHOULD RUN=======================================================
prepBlockMesh = True    # -- preparation of the blockMeshDict script
makeGeom = True # -- creation of the geometry for computation
runDynSim = True    # -- run simulation
runPostProcess = True   # -- run post-processing
```
`baseCaseDir` sets up the tutorial directory, `outFolder` specifies path where the tutorial will be copied, modified and run. 

# Post-processing
For the post-processing, it is possible to use prepared `pyCtrlScripts/runBreadAx2D.py` script, which compares the results directly with the experimental data by generation of the following graph. 