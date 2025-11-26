#!/usr/bin/python

#FILE DESCRIPTION=======================================================

# Python script to set up and run bread baking simulations according to 
# Zhang et al. https://doi.org/10.1002/aic.10518

# IMPORTS===============================================================
import sys
from OF_caseClass import OpenFOAMCase
import numpy as np
import math
from blockMeshDictClassV8 import *
from meshGeneration import *
import re
import os

# CASE FOLDERS==========================================================
baseCaseDir = '../tutorials/breadAx2D/' # -- base case for simulation
outFolder = '../ZZ_cases/00_breads/refZhangSim_new_4'

# WHAT TO SHOULD RUN====================================================
prepBlockMesh = True    # -- preparation of the blockMeshDict script
makeGeom = True # -- creation of the geometry for computation
runDynSim = True    # -- run simulation

# DEFINE PARAMETERS=====================================================
'''Geometry parameters'''
typeOfMesh = '2DZhang'
mSStep = 0.1e-2 # -- aproximate computational cell size
rLoaf = 3.6e-2  # -- loaf radius                
hLoaf = 3.5e-2  # -- loaf height
arcL = 0.008    # -- length of the arc at the side of the bread   

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

'''Mechanical properties'''
withDeformation = 1 # -- turn on (1) /off (0) deformation
nu = 0.15   # -- Poisson ratio
E = 12000   # -- Youngs modulus

'''Numerics'''
timeStep = 1    # -- computational time step
plusTime1 = 900 # -- how long to run with deformation
plusTime2 = 0 # -- how long to run without deformation
writeInt = 1   # -- how often to write results
nIter = 1  # -- number of iterations in each time step
dynSolver = 'breadBakingFoam'   # -- used solver
nCores = 1 # -- number of cores to run the simulation

# -- relaxation factors
DRelax = 0.1
DFinalRelax = 1

'''Boundary conditions'''
kG = 0.01   # -- external mass transfer coeficient
alphaG = 10 # -- external heat transfer coeficient 

# SCRIPT (DO NOT EDIT)==================================================                       
# -- create OpenFOAMCase object to change values in dictionaries
baseCase = OpenFOAMCase()
baseCase.loadOFCaseFromBaseCase(baseCaseDir)
baseCase.changeOFCaseDir(outFolder)
baseCase.copyBaseCase()

# OTHER COMPUTATIONS====================================================
dA = mSStep
dX, dY, dZ = dA, dA, dA                                  
x0 = y0 = z0 = 0.0      
grX = grY = grZ = "1.0"

# -- prepare blockMeshDict using luckas python class
if prepBlockMesh:
    if typeOfMesh == '2DZhang':
        prep2DMeshZhang(arcL, rLoaf, hLoaf, x0, y0, z0, dA, dX, dY, dZ, grX, grY, grZ, baseCase)

# 1) BOUNDARY CONDITIONS ###############################################
# -- for the different geometries different BC
# -- most of the BC are set directly in base case

# 2) constant/transportProperties ######################################
baseCase.setParameters(
    [
        ['constant/transportProperties', 'withDeformation', str(withDeformation), ''],
        ['constant/transportProperties', 'permGLViscG', str(perm), ''],
    ]
)

# 3) constant/thermophysicalProperties #################################
baseCase.setParameters(
    [
        ['constant/thermophysicalProperties', 'lambda', str(lambdaS), 'solid'],
        ['constant/thermophysicalProperties', 'rho', str(rhoS), 'solid'],
        ['constant/thermophysicalProperties', 'Cp', str(CpS), 'solid'],
        ['constant/thermophysicalProperties', 'rho', str(rhoL), 'liquid'],
        ['constant/thermophysicalProperties', 'Cp', str(CpL), 'liquid'],
        ['constant/thermophysicalProperties', 'Cp', str(CpG), 'CO2'],
        ['constant/thermophysicalProperties', 'Cp', str(CpVapor), 'vapor'],
        ['constant/thermophysicalProperties', 'D', str(DFree), 'transport'],
    ]
)

# 4) constant/reactiveProperties #######################################
# -- parameters for evaporation and CO2 generation
baseCase.setParameters(
    [
        ['constant/reactiveProperties', 'kMPCOpen', str(kMPC), 'evaporation'],
        ['constant/reactiveProperties', 'kMPCClosed', str(kMPC), 'evaporation'],
        ['constant/reactiveProperties', 'evCoef1', str(evCoef1), 'evaporation'],
        ['constant/reactiveProperties', 'evCoef2', str(evCoef2), 'evaporation'],
        ['constant/reactiveProperties', 'R0', str(R0), 'fermentation'],
        ['constant/reactiveProperties', 'Tm', str(Tm), 'fermentation'],
    ]
)
        
# 5 system/controlDict #############################################
baseCase.setParameters(
    [
        ['system/controlDict', 'endTime', str(plusTime1), ''],
        ['system/controlDict', 'deltaT', '%.5g'%timeStep, ''],
        ['system/controlDict', 'writeInterval', '%.5g'%writeInt, ''],
    ]
)

# 6) fvSolutions
baseCase.setParameters(
    [
        ['system/fvSolution', 'nOuterCorrectors', str(nIter), 'PIMPLE'],
        ['system/fvSolution', 'D', str(DRelax), 'fields'],
        ['system/fvSolution', 'DFinal', str(DFinalRelax), 'fields'],
    ]
)

# 7) mechanical properties 
baseCase.setParameters(
    [
        ['constant/mechanicalProperties', 'nu', str(nu), 'bread'],
        ['constant/mechanicalProperties', 'E', str(E), 'bread']
    ]
)

# -- prepare geom
if makeGeom:
    if typeOfMesh == '2DZhang':
        baseCase.runCommands(
            [
                'chmod 755 ./* -R',
                'blockMesh > log.blockMesh',
                'rm -rf 0',
                'cp -r 0.org 0',
                'paraFoam -touch',
            ]
        )

# -- run the simulation
if runDynSim:
    if nCores > 1:
        baseCase.setParameters(
            [
                ['system/decomposeParDict', 'numberOfSubdomains', str(nCores), '']
            ]
        )
        baseCase.runCommands(
            [
                'decomposePar > log.decomposePar',
                'foamJob -parallel -screen %s > log.%s' %(dynSolver,dynSolver),
            ]
        )
    else:
        baseCase.runCommands(
            [
                '%s > log.%s' %(dynSolver,dynSolver),
            ]
        )

    # -- run the rest of the simualation without further deformation
    if plusTime2 > plusTime1:
        baseCase.setParameters(
            [
                ['system/controlDict', 'endTime', str(plusTime1 + plusTime2), ''],
                ['constant/transportProperties', 'withDeformation', '0', '']
            ]
        )
        if nCores > 1:
            baseCase.runCommands(
                [
                    'foamJob -parallel -screen %s > log.%s_2' %(dynSolver,dynSolver),
                ]
            )
        else:
            baseCase.updateTimes()
            baseCase.runCommands(
                [
                    '%s > log.%s_2' %(dynSolver,dynSolver),
                ]
            )

exp = np.loadtxt('plots/exp_mouk_center.dat', delimiter=';')
exp2 = np.loadtxt('plots/exp_mouk_surface.dat', delimiter=';')
expD = np.loadtxt('plots/exp_zhang_D.dat', skiprows=1)
baseCase.updateTimes()
baseCase.runCommands(
    [
        'postProcess -func "probeZhang" -dict system/probeZhang > log.postProcess',
        'rm -rf 0',
        'intMoisture > log.intMoisture',
        'intVolume > log.intVolume',
    ]
)
rows = []
lines = []
D = []
with open(baseCase.dir + '/postProcessing/probeZhang/%d/D'%baseCase.latestTime, 'r') as fl:
    lines = fl.readlines()
    lines = lines[nProbes+2:]
    # print(lines)
    for line in lines:
        parts = line.split(") (")
        first_entry = parts[0].split(maxsplit=1)
        vectors = [first_entry[1]] if len(first_entry) > 1 else []
        vectors.extend(parts[1:])

        vectors = [
            tuple(map(float, vec.replace("(", "").replace(")", "").split()))
            for vec in vectors
        ]
        rows.append(vectors)

# Convert to numpy array
D = np.array(rows)
# print(D)
    
# -- load prof
probesT = np.loadtxt(baseCase.dir + '/postProcessing/probeZhang/%d/T'%baseCase.latestTime, skiprows=3)

point1 = probesT[0:,1]
point2 = probesT[0:,2]

time = (probesT[0:,0])/60

# Read the file
file_path = "%s/log.intMoisture" %baseCase.dir
skiprows = 26
with open(file_path, "r") as file:
    lines = file.readlines()

# Extract all numbers using regex
numbers = []
for lineI in range(skiprows, len(lines)):
    line = lines[lineI]
    matches = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)  # Matches integers and decimals
    numbers.extend(map(float, matches))  # Convert to float and add to the list

# Convert the list to a NumPy array
moistureSim = np.array(numbers).reshape(-1,2)
# if not os.path.exists(vystupy + vystup):
#     os.makedirs(vystupy + vystup)
# np.savetxt(vystupy + vystup + '/moisture.dat', moistureSim, header="time\tmoisture", comments="", delimiter="\t")
# np.savetxt(vystupy + vystup + '/temps.dat', probesT, header="time\tcenter\tsurface", comments="", delimiter="\t")


moistureExp = np.loadtxt('plots/liquidMassExp.dat', skiprows=1, delimiter=';')

# Read the file
file_path = "%s/log.intVolume" %baseCase.dir
skiprows = 26
with open(file_path, "r") as file:
    lines = file.readlines()

# Extract all numbers using regex
numbers = []
for lineI in range(skiprows, len(lines)):
    line = lines[lineI]
    matches = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)  # Matches integers and decimals
    numbers.extend(map(float, matches))  # Convert to float and add to the list

# Convert the list to a NumPy array
volumeSim = np.array(numbers).reshape(-1,2)
# np.savetxt(vystupy + vystup + '/volume.dat', volumeSim, header="time\tmoisture", comments="", delimiter="\t")

volumeExp = np.loadtxt('plots/volumeExp.dat', skiprows=1, delimiter=';')
                                    
simAsExpT1 = np.interp(exp[1:,0], time, point1)
simAsExpT2 = np.interp(exp[1:,0], time, point2)
simAsExpDX = np.interp(expD[:,0] / 60, time[1:], D[:, 2, 0])
simAsExpDY = np.interp(expD[:,0] / 60, time[1:], D[:, 1, 1])
simAsExpWat = np.interp(moistureExp[:,0], moistureSim[:-1,0] / 60, moistureSim[:-1,1])
errorT1 = np.linalg.norm((exp[1:,1] - simAsExpT1 + 273) / (exp[1:, 1] + 273))
errorT2 = np.linalg.norm((exp2[1:,1] - simAsExpT2 + 273) / (exp2[1:, 1] + 273))
errorWat = np.linalg.norm((moistureExp[:, 1] - simAsExpWat) / moistureExp[:, 1])
errorDX = np.linalg.norm((expD[:,1] - simAsExpDX) / expD[:,1])
errorDY = np.linalg.norm((expD[:,2] - simAsExpDY) / expD[:,2])

# ovError = errorT1 + errorT2 + errorWat + errorDX + errorDY
ovError = errorT1 + errorT2 + errorWat