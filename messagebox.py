import pygame
import button
from constants import *

class MessageBox():

    def __init__(self):

        self.text = ""
        self.x = 200
        self.y = 300
        self.top =0
        self.button_width = 60
        self.button_height = 22

        self.okbutton = button.Button(140, 270, 60, 22, (240, 150, 50), BLACK, 'OK', BLACK)



    def set_text(self, text):
        self.text = text

    def draw(self,screen, myfont, messagecolor=GREY):
        """"draws popup box and message text"""
        textrows = self.text.split('\n')
        h = 20
        w = 0
        for row in textrows:
            (wt, ht) = myfont.size(row)
            h = h + ht
            w = max(w, wt)
        w = max(w, self.button_width) + 20
        h = h + self.button_height + 20
        left = self.x - w/2
        top = self.y - h/2
        pygame.draw.rect(screen, messagecolor, [left, top, w, h])
        for i, row in enumerate(textrows):
            label = myfont.render(row, 1, BLACK)
            screen.blit(label, (left+10, top + i*20 + 10))
        self.okbutton.set_coords(self.x - self.button_width/2, top + (i+1)*20 + 30)
        self.okbutton.draw(screen, myfont)

    def clicked(self, event):
        return self.okbutton.clicked(event)
