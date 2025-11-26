#!/usr/bin/python

#FILE DESCRIPTION=======================================================

# Python script to create blockMeshDict for bread geometry generation

# IMPORTS===============================================================
import numpy as np
import math
from blockMeshDictClassV8 import *

def prep2DMeshZhang(obloukL, rLoaf, hLoaf, x0, y0, z0, dA, dX, dY, dZ, grX, grY, grZ, baseCase):
    
    if not obloukL == 0:
        wAng = 5
        # -- preparation of the blockMeshDictFile for geometry generation
        yMax = dZ/math.atan(wAng/180*math.pi*0.5)                   # -- yMax from wedge angle
        fvMesh = mesh()                                             # -- create mesh
        nCZ = 1                                                     # -- wedge

        posunBodu1 = -1e-3
        posunBodu2 = -3e-3
        p1 = 0.5
        
        # viceNaKraji = 5
        # viceNaKraji2 = 2
        
        viceNaKraji = 2
        viceNaKraji2 = 1.5
        
        r1 = rLoaf - obloukL 
        h1 = hLoaf - obloukL
        
        bod1 = [h1-posunBodu1, r1 - posunBodu1]
        
        h2 = hLoaf - 3 * obloukL
        
        body = np.array([
            [hLoaf / 2 - obloukL, 0],                                #0
            [hLoaf / 2 - obloukL - posunBodu1, r1 - posunBodu1],                               #1
            [h2 / 2 - posunBodu2, r1 + obloukL / 2- posunBodu2/5],                 #2
            [hLoaf / 2 - obloukL, rLoaf],               #3
            [hLoaf / 2 - obloukL / 2, 0],                  #4
            [hLoaf / 2 - obloukL / 2 - posunBodu2/5, rLoaf - 1.5 * obloukL- posunBodu2],   #5
            # [hLoaf / 2 - obloukL / 2, rLoaf - obloukL /2], #6
            [hLoaf / 2 - obloukL + math.sin(math.pi/4) * obloukL, rLoaf - obloukL  + math.sin(math.pi/4) * obloukL], #6
            [hLoaf / 2, rLoaf - obloukL],                   #7
            [hLoaf / 2, 0]                                  #8
        ])
        
        bodyArc = np.array([
            [hLoaf / 2 - obloukL + math.cos(3*math.pi/4) * obloukL, rLoaf - obloukL + math.sin(3*math.pi/4) * obloukL],
            [hLoaf / 2 - obloukL + math.cos(math.pi/8) * obloukL, rLoaf - obloukL + math.sin(math.pi/8) * obloukL],
            # [hLoaf / 2 - obloukL + math.cos(math.pi/8) * obloukL, rLoaf - obloukL + math.sin(math.pi/8)],
            # [hLoaf / 2 - obloukL + math.sin(math.pi/4) * obloukL, rLoaf - obloukL + math.sin(math.pi/4)],
        ])
        body = np.append(body, body, axis=0)
        body[9:,0] = -body[9:,0]
        bodyArc = np.append(bodyArc, bodyArc, axis=0)
        bodyArc[2:,0] = -bodyArc[2:,0]

        gr1 = "1"
        # gr1 = "0.75"
        # gr2 = "2"
        nCX = int(round(abs(body[0][0]-body[9][0])/dX))
        nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        nCX0 = nCX
        nCY1 = nCY
        
        nCY = int(round(2**0.5*abs(body[1][1]-body[2][1])/dY))
        nCY2 = nCY * viceNaKraji2
        
        nCX = int(round(abs(body[6][0]-body[1][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        # nCY1 = nCY
        nCX2 = nCX * viceNaKraji
        
        nCX = int(round(abs(body[0][0]-body[4][0])/dX))
        nCX1 = nCX * viceNaKraji
    
        #### 1
        # vertices
        vertices = [
            [body[9][0],  body[9][1], z0-body[9][1]/yMax*dZ],
            [body[0][0],  body[0][1], z0-body[0][1]/yMax*dZ],
            [body[1][0],  body[1][1], z0-body[1][1]/yMax*dZ],
            [body[10][0], body[10][1],z0-body[10][1]/yMax*dZ],
            [body[9][0],  body[9][1], z0+body[9][1]/yMax*dZ],
            [body[0][0],  body[0][1], z0+body[0][1]/yMax*dZ],
            [body[1][0],  body[1][1], z0+body[1][1]/yMax*dZ],
            [body[10][0], body[10][1],z0+body[10][1]/yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[0][0]-body[9][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        # nCX0 = nCX
        # nCY1 = nCY
        nCells = [nCX0, nCY1, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block1 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        #### 2
        # vertices
        vertices = [
            [body[10][0], body[10][1], z0-body[10][1] /yMax*dZ],
            [body[1][0],  body[1][1],  z0-body[1][1]  /yMax*dZ],
            [body[2][0],  body[2][1],  z0-body[2][1]   /yMax*dZ],
            [body[11][0], body[11][1],z0 -body[11][1]   /yMax*dZ],
            [body[10][0], body[10][1],z0 +body[10][1]  /yMax*dZ],
            [body[1][0],  body[1][1] , z0+body[1][1]   /yMax*dZ],
            [body[2][0],  body[2][1] , z0+body[2][1]   /yMax*dZ],
            [body[11][0], body[11][1],z0 +body[11][1]  /yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells

        nCells = [nCX0, nCY2, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block2 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        #### 3
        # vertices
        vertices = [
            [body[11][0], body[11][1], z0-body[11][1] /yMax*dZ],
            [body[2][0],  body[2][1],  z0-body[2][1]  /yMax*dZ],
            [body[3][0],  body[3][1],  z0-body[3][1]   /yMax*dZ],
            [body[12][0], body[12][1],z0 -body[12][1]   /yMax*dZ],
            [body[11][0], body[11][1],z0 +body[11][1]  /yMax*dZ],
            [body[2][0],  body[2][1],  z0+body[2][1]   /yMax*dZ],
            [body[3][0],  body[3][1],  z0+body[3][1]   /yMax*dZ],
            [body[12][0], body[12][1],z0 +body[12][1]  /yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[6][0]-body[1][0])/dX))
        # # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        # # nCY1 = nCY
        # nCX2 = nCX * viceNaKraji
        nCells = [nCX0, nCX2, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block3 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")

        #### 4
        # vertices
        vertices = [
            [body[0][0], body[0][1], z0-body[0][1]/yMax*dZ],
            [body[4][0], body[4][1], z0-body[4][1]/yMax*dZ],
            [body[5][0], body[5][1], z0-body[5][1]/yMax*dZ],
            [body[1][0], body[1][1], z0-body[1][1]/yMax*dZ],
            [body[0][0], body[0][1], z0+body[0][1]/yMax*dZ],
            [body[4][0], body[4][1], z0+body[4][1]/yMax*dZ],
            [body[5][0], body[5][1], z0+body[5][1]/yMax*dZ],
            [body[1][0], body[1][1], z0+body[1][1]/yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells

        nCells = [nCX1, nCY1, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block4 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        
        #### 5
        # vertices
        vertices = [
            [body[1][0], body[1][1], z0-body[1][1]/yMax*dZ],
            [body[6][0], body[6][1], z0-body[6][1]/yMax*dZ],
            [body[3][0], body[3][1], z0-body[3][1]/yMax*dZ],
            [body[2][0], body[2][1], z0-body[2][1]/yMax*dZ],
            [body[1][0], body[1][1], z0+body[1][1]/yMax*dZ],
            [body[6][0], body[6][1], z0+body[6][1]/yMax*dZ],
            [body[3][0], body[3][1], z0+body[3][1]/yMax*dZ],
            [body[2][0], body[2][1], z0+body[2][1]/yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(2**0.5*abs(body[1][1]-body[5][1])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        # nCY1 = nCY
        # nCX2 = nCX
        nCells = [nCX2, nCY2, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block5 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        fvMesh.addEdge("arc", block5.retEXEZ0(), [(bodyArc[0][0], bodyArc[0][1], z0-bodyArc[0][1]/yMax*dZ)])
        fvMesh.addEdge("arc", block5.retEXEZE(), [(bodyArc[0][0], bodyArc[0][1], z0+bodyArc[0][1]/yMax*dZ)])
        
        
        #### 6
        # vertices
        vertices = [
            [body[5][0], body[5][1], z0-body[5][1]/yMax*dZ],
            [body[7][0], body[7][1], z0-body[7][1]/yMax*dZ],
            [body[6][0], body[6][1], z0-body[6][1]/yMax*dZ],
            [body[1][0], body[1][1], z0-body[1][1]/yMax*dZ],
            [body[5][0], body[5][1], z0+body[5][1]/yMax*dZ],
            [body[7][0], body[7][1], z0+body[7][1]/yMax*dZ],
            [body[6][0], body[6][1], z0+body[6][1]/yMax*dZ],
            [body[1][0], body[1][1], z0+body[1][1]/yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells
        nCX = int(round(abs(body[6][0]-body[1][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        # nCY1 = nCY
        # nCX2 = nCX
        nCells = [nCX2, nCX1, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block6 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        fvMesh.addEdge("arc", block6.retEXEZ0(), [(bodyArc[1][0], bodyArc[1][1], z0-bodyArc[1][1]/yMax*dZ)])
        fvMesh.addEdge("arc", block6.retEXEZE(), [(bodyArc[1][0], bodyArc[1][1], z0+bodyArc[1][1]/yMax*dZ)])
        # fvMesh.addEdge("arc", block6.retEY0ZE(), [(bodyArc[1][0], bodyArc[1][1], z0+bodyArc[1][1]/yMax*dZ)])
        # fvMesh.addEdge("arc", block7.retEXEZE(), [(xE4, yE4, z0+yE4/yMax*dZ)])


        
        #### 7
        # vertices
        vertices = [
            [body[4][0], body[4][1], z0-body[4][1]/yMax*dZ],
            [body[8][0], body[8][1], z0-body[8][1]/yMax*dZ],
            [body[7][0], body[7][1], z0-body[7][1]/yMax*dZ],
            [body[5][0], body[5][1], z0-body[5][1]/yMax*dZ],
            [body[4][0], body[4][1], z0+body[4][1]/yMax*dZ],
            [body[8][0], body[8][1], z0+body[8][1]/yMax*dZ],
            [body[7][0], body[7][1], z0+body[7][1]/yMax*dZ],
            [body[5][0], body[5][1], z0+body[5][1]/yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[4][0]-body[8][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        nCells = [nCX2, nCY1, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block7 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        #### 8
        # vertices
        vertices = [
            [body[13][0]  , body[13][1]   ,  z0-body[13][1]/yMax*dZ],
            [body[9][0]   , body[9][1]    ,  z0-body[9][1] /yMax*dZ],
            [body[10][0]  , body[10][1]   ,  z0-body[10][1]/yMax*dZ],
            [body[14][0]  , body[14][1]   ,  z0-body[14][1]/yMax*dZ],
            [body[13][0] ,  body[13][1]    , z0+body[13][1]/yMax*dZ],
            [body[9][0]  ,  body[9][1]     , z0+body[9][1] /yMax*dZ],
            [body[10][0] ,  body[10][1]    , z0+body[10][1]/yMax*dZ],
            [body[14][0] ,  body[14][1]    , z0+body[14][1]/yMax*dZ],
        ]
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[4][0]-body[8][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        nCells = [nCX1, nCY1, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block8 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        #### 9
        # vertices
        vertices = [
            [body[14][0]   , body[14][1]   ,   z0-body[14][1]/yMax*dZ],
            [body[10][0]   , body[10][1]   ,   z0-body[10][1]/yMax*dZ],
            [body[15][0]   , body[15][1]   ,   z0-body[15][1]/yMax*dZ],
            [body[16][0]   , body[16][1]   ,   z0-body[16][1]/yMax*dZ],
            [body[14][0]   , body[14][1]   ,   z0+body[14][1]/yMax*dZ],
            [body[10][0]   , body[10][1]   ,   z0+body[10][1]/yMax*dZ],
            [body[15][0]   , body[15][1]   ,   z0+body[15][1]/yMax*dZ],
            [body[16][0]   , body[16][1]   ,   z0+body[16][1]/yMax*dZ],
        ]  
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[4][0]-body[8][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        nCells = [nCX1, nCX2, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block9 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        fvMesh.addEdge("arc", block9.retEYEZ0(), [(bodyArc[3][0], bodyArc[3][1], z0-bodyArc[3][1]/yMax*dZ)])
        fvMesh.addEdge("arc", block9.retEYEZE(), [(bodyArc[3][0], bodyArc[3][1], z0+bodyArc[3][1]/yMax*dZ)])
    
        #### 10
        # vertices
        vertices = [
            [body[10][0]   , body[10][1]   ,   z0-body[10][1]/yMax*dZ],
            [body[11][0]   , body[11][1]   ,   z0-body[11][1]/yMax*dZ],
            [body[12][0]   , body[12][1]   ,   z0-body[12][1]/yMax*dZ],
            [body[15][0]   , body[15][1]   ,   z0-body[15][1]/yMax*dZ],
            [body[10][0]   , body[10][1]   ,   z0+body[10][1]/yMax*dZ],
            [body[11][0]   , body[11][1]   ,   z0+body[11][1]/yMax*dZ],
            [body[12][0]   , body[12][1]   ,   z0+body[12][1]/yMax*dZ],
            [body[15][0]   , body[15][1]   ,   z0+body[15][1]/yMax*dZ],
        ]  
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[4][0]-body[8][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        nCells = [nCY2, nCX2, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block10 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        fvMesh.addEdge("arc", block10.retEYEZ0(), [(bodyArc[2][0], bodyArc[2][1], z0-bodyArc[2][1]/yMax*dZ)])
        fvMesh.addEdge("arc", block10.retEYEZE(), [(bodyArc[2][0], bodyArc[2][1], z0+bodyArc[2][1]/yMax*dZ)])
        
        #### 11
        # vertices
        vertices = [
            [body[17][0]   , body[17][1]   ,   z0-body[17][1]/yMax*dZ],
            [body[13][0]   , body[13][1]   ,   z0-body[13][1]/yMax*dZ],
            [body[14][0]   , body[14][1]   ,   z0-body[14][1]/yMax*dZ],
            [body[16][0]   , body[16][1]   ,   z0-body[16][1]/yMax*dZ],
            [body[17][0]   , body[17][1]   ,   z0+body[17][1]/yMax*dZ],
            [body[13][0]   , body[13][1]   ,   z0+body[13][1]/yMax*dZ],
            [body[14][0]   , body[14][1]   ,   z0+body[14][1]/yMax*dZ],
            [body[16][0]   , body[16][1]   ,   z0+body[16][1]/yMax*dZ],
        ]  
        # neighbouring blocks
        neighbours = []
        # number of cells
        # nCX = int(round(abs(body[4][0]-body[8][0])/dX))
        # nCY = int(round(abs(body[0][1]-body[1][1])/dY))
        nCells = [nCX2, nCY1, nCZ]
        # grading
        grading = [grX, grY, grZ]
        # create the block
        block11 = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = "bread1")
        
        bottom = list()
        bottom.append(block11.retFYZ0())
        fvMesh.addPatch("bottom", "patch", bottom)
        
        sides = list()
        sides.append(block9.retFXZE())
        sides.append(block10.retFXZE())
        sides.append(block3.retFXZE())
        sides.append(block5.retFYZE())
        sides.append(block6.retFYZE())
        sides.append(block7.retFYZE())
        fvMesh.addPatch("sides", "patch", sides)
        
        wedgeZ0 = list()
        for block in fvMesh.blocks:
            wedgeZ0.append(block.retFXY0())

        fvMesh.addPatch("wedgeZ0", "wedge", wedgeZ0)
        wedgeZE = list()
        for block in fvMesh.blocks:
            wedgeZE.append(block.retFXYE())

        fvMesh.addPatch("wedgeZE", "wedge", wedgeZE)
        
        ### WRITE ###
        fvMesh.writeBMD("%s/system/" % baseCase.dir)

    else:
        raise ValueError('Dough arc length cannot be 0.')