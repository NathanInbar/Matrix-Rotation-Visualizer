import pygame
from Matrix import SquareCellMatrix
from Animation import MatrixAnimationController
from TransformGenerators import rotateMatrix
from util import Header,Button

WIDTH = 800
HEIGHT = 600

clock = pygame.time.Clock()
FPS = 30
frame_count = 0
BKG_COLOR = (30,30,40)

drawRays = True

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Rotation Visualizer")


headers = [
    Header((WIDTH/2,HEIGHT-25),200,100, (255,255,255), "", "centered"),
    Header((10,10), 75,50, (25,25,25), "matrix size"),
]

matrix = SquareCellMatrix(N = 10, cell_size = 50, screen_width = WIDTH, screen_height = HEIGHT)
rotateAnimation = MatrixAnimationController(matrix.getMatrix(),rotateMatrix, headers[0].setText)

def toggleRays():
    drawRays = not drawRays
    update()


buttons = [
    Button( coordinates=(WIDTH-85,10), width=75,height=50, color=(100,50,100), \
                    text_string="quit", callback=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)) ),

    Button( coordinates=(WIDTH-85, 70), width=75, height=50, color=(50,50,50), \
                    text_string="reset", callback=lambda: print('reset') ),

    Button( coordinates=(WIDTH-85, 130), width=75, height=50, color=(50,75,100), \
                    text_string="step", callback=rotateAnimation.stepAnimation ),

    Button( coordinates=(WIDTH-85, 190), width=75, height=50, color=(100,50,50), \
                    text_string="rays", callback=toggleRays ),

    Button( coordinates=(60, 50), width=30, height=30, color=(255,255,255), \
                    text_string="<", font_color=(0,0,0), callback=rotateAnimation.stepAnimation ),

    Button( coordinates=(100, 50), width=30, height=30, color=(255,255,255), \
                    text_string=">", font_color=(0,0,0), callback=rotateAnimation.stepAnimation ),

]



def update():
    global frame_count
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.update()


    for i,row in enumerate(matrix.getMatrix()):
        for j,cell in enumerate(row):
            cell.update((i,j))

    render()
    clock.tick(FPS)
    frame_count+=1
    frame_count%=FPS
    return True

def render():
    win.fill(BKG_COLOR)
    
    for button in buttons:
        button.render(win)

    for header in headers:
        header.render(win)

    for i,row in enumerate(matrix.getMatrix()):
        for j,cell in enumerate(row):
            cell.render(win)

    if drawRays:
        for ray in rotateAnimation.getRays():
            start, dest = ray.getCoords()
            pygame.draw.aaline(win,ray.getColor(),start,dest)

    pygame.display.flip()

def main():
    while update():
        pass
        #print(frame_count)


class Main():
    


if __name__ == "__main__":
    main()