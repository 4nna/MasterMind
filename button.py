import pygame
from constants import *
#class Box():


class Button() :

    def __init__(self, left, top, width, height, color, bordercolor, text, textcolor):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.bordercolor = bordercolor
        self.text = text
        self.textcolor = textcolor
        self.X = self.left + self.width/2
        self.Y = self.top + self.height/2

    def draw(self, screen, myfont):
        pygame.draw.rect(screen, self.bordercolor, [self.left+3, self.top+3, self.width, self.height])
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        selectlabel = myfont.render(self.text, 1, self.textcolor)
        selectRect = selectlabel.get_rect()
        selectRect.center = (self.X , self.Y)
        screen.blit(selectlabel, selectRect)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN) and \
               (event.button == LEFT) and \
               (self.left < event.pos[0] < self.left+self.width) and \
               (self.top < event.pos[1] < self.top+self.height)

    def active(self, color):
        self.bordercolor = color

    def inactive(self, color):
        self.bordercolor=color

    def get_text(self):
        return self.text

    def update_text(self, text):
        self.text = text


class RoundButton(Button):

    def __init__(self, x, y, r, color, bordercolor, text, textcolor):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.bordercolor = bordercolor
        self.text = text
        self.textcolor = textcolor
        self.X = self.left + self.width/2
        self.Y = self.top + self.height/2

    def draw(self, screen, myfont):
        pygame.draw.circle(screen, self.bordercolor, [self.x+2, self.y+2], self.r+2)
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.r)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN) and \
               (event.button == LEFT) and \
               self.x<event.pos[0]<self.x+self.r and \
               self.y<event.pos[1]<self.y+self.r

    def active(self, color):
        self.bordercolor = color

    def inactive(self, color):
        self.bordercolor = color

    def get_color(self):
        return self.color

    def get_text(self):
        return self.text
