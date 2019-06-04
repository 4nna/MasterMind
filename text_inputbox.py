import pygame

class InputBox():

    def __init__(self, left, top, width, width2, height, color, bordercolor, text, textcolor, textinputcolor):
        self.left = left
        self.top = top
        self.width = width
        self.width2 = width2
        self.height = height
        self.color = color
        self.bordercolor = bordercolor
        self.text = text
        self.name = ''
        self.textcolor = textcolor
        self.textinputcolor = textinputcolor
        self.X = self.left - self.width2/2
        self.Y = self.top + self.height/2
        self.X_input = self.left + self.width/2
        self.Y_input = self.top + self.height/2

    def draw(self, screen, myfont):
        pygame.draw.rect(screen, self.bordercolor, [self.left+1, self.top+1, self.width+2, self.height+2])
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        selectlabel = myfont.render(self.text, 1, self.textcolor)
        selectRect = selectlabel.get_rect()
        selectRect.center = (self.X , self.Y)
        screen.blit(selectlabel, selectRect)
        selectlabel_input = myfont.render(self.name, 1, self.textinputcolor)
        selectRect_input = selectlabel_input.get_rect()
        selectRect_input.center = (self.X_input , self.Y_input)
        screen.blit(selectlabel_input, selectRect_input)

    def get_input(self, event):

        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                if len(self.name)<8:
                    self.name += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
        return self.name

