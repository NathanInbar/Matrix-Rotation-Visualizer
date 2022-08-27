import pygame
from Matrix import SquareCellMatrix
from math import floor
from Animation import MatrixAnimationController
from TransformGenerators import rotateMatrix
from util import Header,Button


class Main():
    WIDTH = 800
    HEIGHT = 600

    clock = pygame.time.Clock()
    FPS = 60
    frame_count = 0
    BKG_COLOR = (30,30,40)

    win = pygame.display.set_mode((WIDTH, HEIGHT))


    def __init__(self):
        self.drawRays = True
        self.frame_count = 0

        self.headers = self.initHeaders()

        self.matrixSize = 3

        self.colorMode = "gradient"
        self.colorModeIndex = 1

        self.matrix = SquareCellMatrix(N = self.matrixSize, cell_size = 50, screen_width = self.WIDTH, screen_height = self.HEIGHT, colorMode=self.colorMode)

        self.rotateAnimation = MatrixAnimationController(self.matrix.getMatrix(), rotateMatrix, self.headers[0].setText)

        self.buttons = self.initButtons()

        pygame.display.set_caption("Matrix Rotation Visualizer")

        #  - - - run main loop
        self.start()


    def initHeaders(self):
        headers = [
            Header((self.WIDTH/2,self.HEIGHT-25),200,100, (255,255,255), "", "centered"),
            Header((10,10), 75,50, (25,25,25), "matrix size"),
        ]
        return headers

    def initButtons(self):
        buttons = [
            Button( coordinates=(self.WIDTH-85,10), width=75,height=50, color=(100,50,100), \
                            text_string="quit", callback=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)) ),

            Button( coordinates=(self.WIDTH-85, 70), width=75, height=50, color=(50,50,50), \
                            text_string="reset", callback= self.resetState ),

            Button( coordinates=(self.WIDTH-85, 130), width=75, height=50, color=(50,75,100), \
                            text_string="step", callback=self.rotateAnimation.stepAnimation ),
            
            Button( coordinates=(self.WIDTH-85, 190), width=75, height=50, color=(50,75,100), \
                            text_string="play", callback=lambda: self.rotateAnimation.playOnTimer(1, self.getCyclesFor1Rotation()*3, self.update ) ),

            Button( coordinates=(self.WIDTH-85, 250), width=75, height=50, color=(50,75,100), \
                            text_string="color", callback=self.rotateColorMode ),

            Button( coordinates=(self.WIDTH-85, 310), width=75, height=50, color=(100,50,50), \
                            text_string="rays", callback= self.toggleRays ),

            Button( coordinates=(60, 50), width=30, height=30, color=(255,255,255), \
                            text_string="<", font_color=(0,0,0), callback=self.decreaseMatrixSize ),

            Button( coordinates=(100, 50), width=30, height=30, color=(255,255,255), \
                            text_string=">", font_color=(0,0,0), callback=self.increaseMatrixSize ),

        ]
        return buttons

    def update(self):
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.update()


        for i,row in enumerate(self.matrix.getMatrix()):
            for j,cell in enumerate(row):
                cell.update((i,j))

        self.render()
        self.clock.tick(self.FPS)
        self.frame_count+=1
        self.frame_count%=self.FPS
        return True

    def render(self):
        self.win.fill(self.BKG_COLOR)
        
        for button in self.buttons:
            button.render(self.win)

        for header in self.headers:
            header.render(self.win)

        for i,row in enumerate(self.matrix.getMatrix()):
            for j,cell in enumerate(row):
                cell.render(self.win)

        if self.drawRays:
            for ray in self.rotateAnimation.getRays():
                start, dest = ray.getCoords()
                pygame.draw.aaline(self.win,ray.getColor(),start,dest)

        pygame.display.flip()

    def toggleRays(self):
        self.drawRays = not self.drawRays
        self.update()

    def resetState(self):
        
        self.resetMatrix()
        self.rotateAnimation.resetAnimation(self.matrix.getMatrix(), rotateMatrix)
        self.headers[0].setText("") #dont toucha my spaghett
        self.update()

    def resetMatrix(self):
        self.matrix = SquareCellMatrix(N = self.matrixSize, cell_size = 50, screen_width = self.WIDTH, screen_height = self.HEIGHT, colorMode=self.colorMode)
        self.update()

    def decreaseMatrixSize(self):
        if self.matrixSize > 1:
            self.matrixSize-=1
            self.resetState()

    def increaseMatrixSize(self):
        if self.matrixSize < 10:
            self.matrixSize+=1
            self.resetState()
            
    def rotateColorMode(self):

        self.colorModeIndex +=1

        if self.colorModeIndex == 1:
            self.colorMode = "gradient"
        elif self.colorModeIndex == 2:
            self.colorMode = "rainbow"
        else:
            self.colorMode = "random"
            self.colorModeIndex = 0

        self.matrix.setColorMode(self.colorMode)
        self.update()

    def getCyclesFor1Rotation(self):
        cycles = 0
        incr = 0
        for i in range(self.matrixSize-1):
            if i % 2 == 0:
                incr+=1
            cycles += incr
        return cycles

    def start(self):
        while self.update():
            pass


if __name__ == "__main__":
    main = Main()