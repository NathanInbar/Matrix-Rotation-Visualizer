import pygame
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Ray():

    start: Tuple[int,int]
    dest: Tuple[int,int]
    color: Tuple[int,int,int]
    
    def getColor(self):
        return self.color
    
    def getCoords(self):
        return (self.start,self.dest)

class MatrixAnimationController():

    def __init__(self, matrix, transformGenerator, textUpdate=None):
        pygame.init()
        self.matrix = matrix
        self.transformGenerator = transformGenerator(matrix)
        self.step = 0
        self.rayPool = []

        if textUpdate:
            self.textUpdate = textUpdate

    def newRay(self, cell1, cell2, color = (255,50,50)):

        self.rayPool.append(Ray(cell1.getCenter(),cell2.getCenter(), color))

    def stepTransform(self):
        try:
            return next(self.transformGenerator)
        except StopIteration:
            return None

    def stepAnimation(self, steps=1, stepDelayMS=0):
        ''' 
        steps transform and creates new ray between the returned cells
        returns False if transform generator is done, else True
        '''

        for i in range(steps):
            cell_delta = self.stepTransform()
            if not cell_delta: #animation is finished
                return False

            if self.textUpdate:
                self.textUpdate(f"{cell_delta[0].getID()} <-> {cell_delta[1].getID()}")


            self.newRay(cell_delta[0],cell_delta[1])
            self.step+=1

        return True

    def resetAnimation(self, matrix, transformGenerator):
        self.matrix = matrix
        self.transformGenerator = transformGenerator(matrix)
        self.rayPool = []
        self.step = 0


    def playOnTimer(self, stepDelayInMS, steps, updateFunc):
        for i in range(steps):
            self.stepAnimation()
            updateFunc()
            pygame.time.wait(stepDelayInMS)

    def getRays(self):
        return self.rayPool

