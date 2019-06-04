#start screen select:

###
# show selected username:  select username -> go to username selection / enter new username
###

###
# show AI/noAI:  select AI -> go to AI selection  #no ai when username is selected and vice versa
###

###
# toggle multi color vs unique color
###

####
# start game  -> go to game screen
###

###
# show leaderboard  -> go to leaderboard
###

###
# quit
###

# select username:

###
# list of last 3 usernames shown.. can scroll through and select any username  (taken from mastermindlog) (only real usernames, no AI-usernames)
###

###
# create new user: -> window to enter new username
###

###
# back
###


# select AI:

#select AI or no-AI

##
# back
##


# show leaderboard:

#leaderboard

###
# show stats
###

###
# show leaderboard
###

###
# back -> back to start-screen
###

# game:



#create gui-class

#def start:
#run pygame
#depending on class-settings, display different windows.
import random
import time
import os
import pandas as pd
import pygame
import leaderboard
import button
import mastermind


def in_username_area(pos):
    return left < pos[0] < left+width and 50 < pos[1] < 50+height

def in_AI_area(pos):
    return left < pos[0] < left+width and 150 < pos[1] < 150+height

def in_color_area(pos):
    return left < pos[0] < left+width and 250 < pos[1] < 250+height

def in_leaderboard_area(pos):
    return left < pos[0] < left+width and 350 < pos[1] < 350+height

def in_game_area(pos):
    return left < pos[0] < left+width and 450 < pos[1] < 450+height

def in_quit_area(pos):
    return left < pos[0] < left+width and 550 < pos[1] < 550+height

def in_back_area(pos):
    return 210 < pos[0] < 380 and  600 < pos[1] < 640

def in_stats_area(pos):
    return 20 < pos[0] < 190 and  600 < pos[1] < 640

class Gamesession:
    global width
    width= 200
    global height
    height= 60
    global   left
    left= 100

    def __init__(self):
        self.window = 'start'
        self.username = 'anna'
        self.AI = 'user/no AI'
        self.mode = 'unique colors'


        self.sessionlogfile = '.mastermind_session.log'
        #initiate screens

        #AI
        self.user_button = button.Button(left, 100, width, height, GREY, BLACK, 'user/no AI', BLACK)
        self.ai1_button = button.Button(left, 200, width, height, GREY, BLACK, 'simple AI', BLACK)
        self.ai2_button = button.Button(left, 300, width, height, GREY, BLACK, 'RL AI', BLACK)
        self.ai3_button = button.Button(left, 400, width, height, GREY, BLACK, 'RL DL AI', BLACK)
        self.back_button = button.Button(left, 500, width, height, GREY, BLACK, 'back', BLACK)


        # initiate game, reset all
        pygame.init()

        # choose font
        self.myfont = pygame.font.SysFont("arial", 17)
        size = (400, 650)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("My MasterMind")



    def run(self):

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():  # User did something
            # --- Main event loop
                self.get_events(event)
            # --- Drawing
                self.screen.fill(BACKGROUND)
                if self.window=='start':
                    self.get_start_events(event)
                    self.draw_start()
                elif self.window == 'username':
                    self.get_username_events(event)
                    self.draw_username()
                elif self.window == 'ai':
                    self.ai_window(event)
                elif self.window == 'leaderboard':
                    self.get_leaderboard_events(event)
                    self.draw_leaderboard()
                elif self.window == 'stats':
                    self.get_stats_events(event)
                    self.draw_stats()
                elif self.window == 'game':
                    #self.get_game_events(event)
                    #self.draw_game()
                    pass
            # ---  update the screen .
                pygame.display.flip()

                # --- Limit to 60 frames per second
            clock.tick(60)

    def get_events(self, event):
        if event.type == pygame.QUIT:  # If user clicked close
            pygame.quit()


    def write(self, text, X, Y, color):
        selectlabel = self.myfont.render(text, 1, color)
        selectRect = selectlabel.get_rect()
        selectRect.center = (X , Y)
        self.screen.blit(selectlabel, selectRect)

    def write_table(self, toptable, X, Y, color):
        N = toptable.shape[0]
        for i in range(N):
            line = "    ".join([str(entry)
                                     for entry in toptable.iloc[i]])
            label = self.myfont.render(line, 1, BLACK)
            self.screen.blit(label, (X, Y+i*20))

    def draw_start(self):
        # start window
        #select username
        width = 200
        height = 60
        left = 100
        pygame.draw.rect(self.screen, BLACK, [left+3, 53, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 50, width, height])
        self.write("select username", left+width/2, 50+height/2 - 20, BLACK)
        self.write(self.username, left+width/2, 50+height/2, RED)

        #show AI
        pygame.draw.rect(self.screen, BLACK, [left+3, 153, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 150,  width, height])
        self.write("select AI", left+width/2, 150+height/2 - 20, BLACK)
        self.write(self.AI, left+width/2, 150+height/2, RED)

        #toggle unique/multi
        pygame.draw.rect(self.screen, BLACK, [left+3, 253, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 250, width, height])
        self.write(self.mode, left+width/2, 250+height/2, RED)

        #show leaderboard
        pygame.draw.rect(self.screen, BLACK, [left+3, 353, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 350, width, height])
        self.write("show leaderboard", left+width/2, 350+height/2, BLACK)

        #start game
        pygame.draw.rect(self.screen, BLACK, [left+3, 453, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 450, width, height])
        self.write("start game", left+width/2, 450+height/2, BLACK)

        #quit game
        pygame.draw.rect(self.screen, BLACK, [left+3, 553, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 550, width, height])
        self.write("stop game", left+width/2, 550+height/2, BLACK)

    def get_start_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            #print(event.pos)
            if in_username_area(event.pos):
                self.window = 'username'
            elif in_AI_area(event.pos):
                self.window = 'ai'
            elif in_color_area(event.pos):
                self.toggle_multicolor()
            elif in_leaderboard_area(event.pos):
                self.window = 'leaderboard'
            elif in_game_area(event.pos):
                self.window = 'game'
            elif in_quit_area(event.pos):
                pygame.quit()

    def get_username_events(self, event):
        pass

    def draw_username(self):
        pass

    def ai_window(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            if self.user_button.clicked(event.pos):
                self.AI = 'user/no AI'
            elif self.ai1_button.clicked(event.pos):
                self.AI = 'AI_1'
            elif self.ai2_button.clicked(event.pos):
                self.AI = 'AI_2'
            elif self.ai3_button.clicked(event.pos):
                self.AI = 'AI_3'
            elif self.back_button.clicked(event.pos):
                self.window = 'start'

        if self.AI == 'user/no AI':
            self.user_button.active(RED)
        else:
            self.user_button.inactive(BLACK)
        if self.AI == 'AI_1':
            self.ai1_button.active(RED)
        else:
            self.ai1_button.inactive(BLACK)
        if self.AI == 'AI_2':
            self.ai2_button.active(RED)
        else:
            self.ai2_button.inactive(BLACK)
        if self.AI == 'AI_3':
            self.ai3_button.active(RED)
        else:
            self.ai3_button.inactive(BLACK)


        self.user_button.draw(self.screen, self.myfont)
        self.ai1_button.draw(self.screen, self.myfont)
        self.ai2_button.draw(self.screen, self.myfont)
        self.ai3_button.draw(self.screen, self.myfont)
        self.back_button.draw(self.screen, self.myfont)


    def get_leaderboard_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            #print(event.pos)
            if in_back_area(event.pos):
                self.window = 'start'
            elif in_stats_area(event.pos):
                self.window = 'stats'

    def draw_leaderboard(self):
        height = 400
        left = 60
        width = 280
        pygame.draw.rect(self.screen, BLACK, [left+3, 53, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 50, width, height])
        self.write("Leaderboard", left+width/2, 45, BLACK)
        leadtable = leaderboard.Leaderboard()
        self.write_table(leadtable.top(), left+10, 60, BLACK)

        height = 40
        pygame.draw.rect(self.screen, BLACK, [left+3, 603, width/2-10, height])
        pygame.draw.rect(self.screen, GREY, [left, 600, width/2-10, height])
        self.write("Stats", left+width/4, 620, BLACK)
        pygame.draw.rect(self.screen, BLACK, [left+3+width/2+10, 603, width/2-10, height])
        pygame.draw.rect(self.screen, GREY, [left+width/2+10, 600, width/2-10, height])
        self.write("Back", left+3*width/4, 620, BLACK)


    def get_stats_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            #print(event.pos)
            if in_back_area(event.pos):
                self.window = 'start'
            elif in_stats_area(event.pos):
                self.window = 'leaderboard'

    def draw_stats(self):
        height = 320
        left = 40
        width = 320
        pygame.draw.rect(self.screen, BLACK, [left+3, 53, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 50, width, height])
        self.write("Stats", left+width/2, 45, BLACK)
        leadtable = leaderboard.Leaderboard()
        leadtable.stats()
        statsImg = pygame.image.load('stats.png')
        self.screen.blit(statsImg, (left+10, 53))

        height = 40
        pygame.draw.rect(self.screen, BLACK, [left+3, 603, width/2-10, height])
        pygame.draw.rect(self.screen, GREY, [left, 600, width/2-10, height])
        self.write("Leaderboard", left+width/4, 620, BLACK)
        pygame.draw.rect(self.screen, BLACK, [left+3+width/2+10, 603, width/2-10, height])
        pygame.draw.rect(self.screen, GREY, [left+width/2+10, 600, width/2-10, height])
        self.write("Back", left+3*width/4, 620, BLACK)


    def toggle_multicolor(self):
        if self.mode == 'unique colors':
            self.mode = 'multicolor'
        else:
            self.mode = 'unique colors'

# Define some colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 125, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (125, 125, 25)
BLACK = (0, 0, 0)
GREY = (170, 170, 170)
DARKGREY = (150, 150, 150)
BACKGROUND = (200, 200, 200)
MESSAGECOLOR = (220, 200, 30)

COLOR = {}
COLOR[1] = WHITE
COLOR[2] = YELLOW
COLOR[3] = ORANGE
COLOR[4] = RED
COLOR[5] = GREEN
COLOR[6] = BLUE
COLOR[7] = BROWN
COLOR[8] = BLACK

# Define mouse buttons
LEFT = 1

# guess positions:
X_POS = [50, 100, 150, 200]
Y_POS = range(550, 99, -50)

mysession = Gamesession()
mysession.run()







pygame.quit()