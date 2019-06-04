import pygame

class Button():

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

    def clicked(self, pos):
        return self.left<pos[0]<self.left+self.width and self.top<pos[1]<self.top+self.height

    def active(self, color):
        self.bordercolor = color

    def inactive(self, color):
        self.bordercolor=color

    def update_text(self, text):
        self.text = text