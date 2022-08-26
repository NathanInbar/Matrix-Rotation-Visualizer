import random
from typing import Tuple
import pygame

def getRectCenter( pos,width,height=None ):
    if not height: height = width
    return (pos[0]+width/2,pos[1]+height/2)

def invertColor( color ):
    COL_MAX = 255
    return tuple([ abs(COL_MAX-val) for val in color ])

class ColorGenerator():
    COL_MAX = 255

    def __init__(self, mode="gradient"):

        self.mode = mode

        #create the generator
        self.colorGen = self.colorGenerator()

    def colorGenerator(self):
        r,g,b = 0,0,0

        while True:
            if self.mode == "random":
                rIncr, gIncr, bIncr = random.randrange(0,self.COL_MAX),random.randrange(0,self.COL_MAX),random.randrange(0,self.COL_MAX)
            else:
                rIncr, gIncr, bIncr = 5,5,5

            r,g,b = r+rIncr,g+gIncr,b+bIncr
            r,g,b = r%self.COL_MAX, b%self.COL_MAX, g%self.COL_MAX
            yield (r,g,b)

    def getNextColor(self):
        return next(self.colorGen)



# UI

class UIComponent():

    def __init__(self, coordinates:Tuple[int,int], width:int, height:int, color:Tuple[int,int,int]):
        pygame.init()

        self.coordinates = coordinates
        self.width, self.height = width, height
        self.rect = pygame.Rect(coordinates[0], coordinates[1], width, height)
        self.color = color

    def isClicked(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            return True
        

class TextComponent():

    def __init__(self, text_string, font_name="Arial", font_size=30, text_color=(255,255,255)):
        pygame.font.init()
        self.text_string = text_string
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = self.font.render(text_string,1,text_color)

    def getTextCenter(self, container_coords:Tuple[int,int], container_size:Tuple[int,int])-> Tuple[int,int]:
        '''find the centered position for text in a rect '''

        rectCenter = getRectCenter(container_coords, container_size[0], container_size[1])
        textDim = self.font.size(self.text_string)
        textDim = getRectCenter((0,0),textDim[0], textDim[1])
        return (rectCenter[0]-textDim[0], rectCenter[1]-textDim[1])


class Header(UIComponent, TextComponent):

    def __init__(self, coordinates, width, height, color, text_string="", alignment="", font_name="consolas", font_size=30):
        UIComponent.__init__(self, coordinates, width, height, color)
        TextComponent.__init__(self, text_string, font_name=font_name, font_size=font_size)
        self.alignment = alignment

    def setText(self, text_string):
        self.text_string = text_string
        self.text = self.font.render(text_string,1,self.text_color)

    def render(self, win):
        if self.alignment == "centered":
            textDim = self.font.size(self.text_string)
            textDim = getRectCenter((0,0),textDim[0], textDim[1])
            win.blit(self.text,  (self.coordinates[0]-textDim[0], self.coordinates[1]-textDim[1]))
        else:
            win.blit(self.text, self.coordinates)

class Button(UIComponent, TextComponent):

    def __init__(self, coordinates: Tuple[int,int], width, height, color, \
                         text_string, callback, font_name="Arial", font_size=30, font_color=(255,255,255)):

        UIComponent.__init__(self,coordinates, width, height, color)
        TextComponent.__init__(self,text_string,font_name, font_size, font_color)

        self.callback = callback

    def update(self):

        if (self.isClicked()):
            self.callback()

    def render(self,win):
        pygame.draw.rect(win,self.color,self.rect)
        centeredText = self.getTextCenter(self.coordinates, (self.width, self.height))
        win.blit(self.text, centeredText )


# class TextBox(UIComponent, TextComponent):

#     def __init__(self, coordinates, width, height, color, max_width, font=None, font_size=None):
#         UIComponent.__init__(self,coordinates, width, height, color)
#         self.user_text = ''
#         TextComponent.__init__(self,self.user_text)
#         self.max_width = max_width
#         self.rect = pygame.Rect(coordinates[0], coordinates[1], width, height)

#         if not font or font_size:
#             self.font = pygame.font.SysFont("Arial",15)
#         else: self.font = pygame.font.SysFont(font, font_size)

#     def update(self):
#         #self.rect.w = max(self.max_width, self.width)
#         pass

#     def render(self, win):
#         win.blit(self.color, self.rect)
