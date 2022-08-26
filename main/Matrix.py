import pygame
from util import getRectCenter, invertColor, ColorGenerator, UIComponent, TextComponent

class Cell(TextComponent):
    '''
    contains pygame information for a square Rect
    '''
    
    def __init__(self, id, coordinates, size, w_offset, h_offset, color):
        TextComponent.__init__(self, text_string=str(id), font_name="consolas", text_color=invertColor(color))
        self.id = id
        self.position = coordinates
        self.coordinates = None
        self.w_offset = w_offset
        self.h_offset = h_offset
        self.size = size
        self.rect = self.update(coordinates)
        self.color = color
    
    def update(self, coordinates):
        self.position = coordinates #comment for cells to maintain original coordinate data
        #modify coordinates so cells position themselves left to right:
        self.coordinates = (coordinates[1]* self.size + self.w_offset, coordinates[0]*self.size + self.h_offset)
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], self.size, self.size)

    def getID(self):
        return self.id

    def getCenter(self):
        return getRectCenter(self.coordinates,self.size)

    def render(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        centeredText = self.getTextCenter(self.coordinates, (self.size, self.size))
        win.blit(self.text, centeredText )

    def __str__(self):
        return f"{self.position}"

class SquareCellMatrix():
    '''
    generates a uniform matrix of Cell objects
    '''
    CELL_RATIO = 12
    def __init__(self, N, cell_size, screen_width, screen_height):
        self.N = N
        self.cell_size = screen_height//self.CELL_RATIO if screen_height <= screen_width else screen_width//self.CELL_RATIO
        self.w_offset = screen_width//2 - (N*cell_size)//2
        self.h_offset = screen_height//2 - (N*cell_size)//2
        self.colorgenerator = ColorGenerator("gradient")
        self.idGen = self.getNextID()
        #lastly, generate the matrix
        self.matrix = self.generateMatrix()

    def getNextID(self):
        for i in range(1,self.N*self.N+1):
            yield i

    def generateMatrix(self):
        self.matrix = [ [Cell(next(self.idGen), (i,j), self.cell_size, self.w_offset, self.h_offset, self.colorgenerator.getNextColor() ) for j in range(self.N)] for i in range(self.N) ]
        return self.matrix

    def getMatrix(self):
        return self.matrix

    def printMatrix(self):
        [print(str(cell) for cell in row) for row in self.matrix]