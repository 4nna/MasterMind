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

##
# back -> bak to start screen, but save session and game
# --> add "continue" button to start screen, instead of start button
##

##
# start -> start new game
##

##
# stop -> stop game and return to start?
##
#
# also: show session variables like username, AI, multicolor and time
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
import text_inputbox
import mastermind
import mastermindgame2

from constants import *

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
        self.logfile = '.mastermind.log'
        #initiate screens

        #START
        self.select_username_button = button.Button(left, 50, width, height, GREY, BLACK, 'select username', BLACK)
        self.select_ai_button = button.Button(left, 150, width, height, GREY, BLACK, 'select AI', BLACK)
        self.toggle_color_button = button.Button(left, 250, width, height, GREY, BLACK, self.mode, BLACK)
        self.show_leaderboard_button = button.Button(left, 350, width, height, GREY, BLACK, 'show leaderboard', BLACK)
        self.start_game_button = button.Button(left, 450, width, height, GREY, BLACK, 'start game', BLACK)
        self.stop_game_button = button.Button(left, 550, width, height, GREY, BLACK, 'stop game', BLACK)

        #AI
        self.user_button = button.Button(left, 100, width, height, GREY, BLACK, 'user/no AI', BLACK)
        self.ai1_button = button.Button(left, 200, width, height, GREY, BLACK, 'simple AI', BLACK)
        self.ai2_button = button.Button(left, 300, width, height, GREY, BLACK, 'RL AI', BLACK)
        self.ai3_button = button.Button(left, 400, width, height, GREY, BLACK, 'RL DL AI', BLACK)
        self.back_button = button.Button(left, 500, width, height, GREY, BLACK, 'back', BLACK)

        #LEADERBOARD
        self.leadtable = leaderboard.Leaderboard()
        self.lb_show_button =  button.Button(60, 600, 130, 40, GREY, BLACK, 'stats', BLACK)
        self.lb_back_button =  button.Button(210, 600, 130, 40, GREY, BLACK, 'back', BLACK)
        self.lb_window = 'leaderboard'

        #USERNAME
        self.topnames = self.leadtable.top_names()
        self.username_list_buttons = []
        for i,key in enumerate(self.topnames):
            x = 150 + 100*i
            self.username_list_buttons.append(button.Button(left, x, width, height, GREY, BLACK, key, BLACK))

        self.text_input = text_inputbox.InputBox(200, 50, 150, 150, height, WHITE, BLACK, "enter username", BLACK, GREY)
        #self.ok_button = button.Button()

        #GAME
        self.thisgame = mastermindgame2.MastermindGame()


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
                    self.start_window(event)
                elif self.window == 'username':
                    self.username_window(event)
                elif self.window == 'ai':
                    self.ai_window(event)
                elif self.window == 'leaderboard':
                    self.leaderboard_window(event)
                elif self.window == 'game':
                    self.game_window(event)

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


    def start_window(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                pygame.quit()
        #elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            #print(event.pos)
        if self.select_username_button.clicked(event):
            self.window = 'username'
        elif self.select_ai_button.clicked(event):
            self.window = 'ai'
        elif self.toggle_color_button.clicked(event):
            self.toggle_multicolor()
            self.toggle_color_button.update_text(self.mode)
        elif self.show_leaderboard_button.clicked(event):
            self.window = 'leaderboard'
        elif self.start_game_button.clicked(event):
            self.window = 'game'
        elif self.stop_game_button.clicked(event):
            pygame.quit()

        self.select_username_button.draw(self.screen, self.myfont)
        self.select_ai_button.draw(self.screen, self.myfont)
        self.toggle_color_button.draw(self.screen, self.myfont)
        self.show_leaderboard_button.draw(self.screen, self.myfont)
        self.start_game_button.draw(self.screen, self.myfont)
        self.stop_game_button.draw(self.screen, self.myfont)

    def username_window(self, event):
        username = self.text_input.get_input(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if len(self.topnames)>2:
                self.topnames = self.topnames[0:2]
                self.username_list_buttons.pop()
            self.topnames.append(username)
            self.username_list_buttons.append(button.Button(left, 150+100*(len(self.topnames)-1), width, height, GREY, BLACK, username, BLACK))
            self.text_input.reset_input()

       # if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        for i,key in enumerate(self.topnames):
            if self.username_list_buttons[i].clicked(event):
                self.username = self.username_list_buttons[i].get_text()
        if self.back_button.clicked(event):
            self.window = 'start'

        for i,key in enumerate(self.topnames):
            if self.username_list_buttons[i].get_text() == self.username:
                self.username_list_buttons[i].active(RED)
            else:
                self.username_list_buttons[i].inactive(BLACK)

        self.text_input.draw(self.screen, self.myfont)
        for i,key in enumerate(self.topnames):
            self.username_list_buttons[i].draw(self.screen, self.myfont)
        self.back_button.draw(self.screen, self.myfont)


    def ai_window(self, event):

       #  if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if self.user_button.clicked(event):
            self.AI = 'user/no AI'
        elif self.ai1_button.clicked(event):
            self.AI = 'AI_1'
        elif self.ai2_button.clicked(event):
            self.AI = 'AI_2'
        elif self.ai3_button.clicked(event):
            self.AI = 'AI_3'
        elif self.back_button.clicked(event):
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


    def toggle_lb_window(self):
        if self.lb_window == 'leaderboard':
            self.lb_window = 'stats'
            self.lb_show_button.update_text('leaderboard')
        else:
            self.lb_window = 'leaderboard'
            self.lb_show_button.update_text('stats')


    def leaderboard_window(self, event):
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        #print(event.pos)
        if self.lb_back_button.clicked(event):
            self.window = 'start'
        elif self.lb_show_button.clicked(event):
            self.toggle_lb_window()
            self.leadtable.stats2()
        self.lb_show_button.draw(self.screen, self.myfont)
        self.lb_back_button.draw(self.screen, self.myfont)
        if self.lb_window=='leaderboard':
            self.draw_leaderboard()
        else:
            self.draw_stats()

    def draw_leaderboard(self):
        height = 400
        left = 60
        width = 280
        pygame.draw.rect(self.screen, BLACK, [left+3, 53, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 50, width, height])
        self.write("Leaderboard", left+width/2, 45, BLACK)
        self.write_table(self.leadtable.top(), left+10, 60, BLACK)


    def draw_stats(self):
        height = 320
        left = 40
        width = 320
        pygame.draw.rect(self.screen, BLACK, [left+3, 53, width, height])
        pygame.draw.rect(self.screen, GREY, [left, 50, width, height])
        self.write("Stats", left+width/2, 45, BLACK)
        statsImg = pygame.image.load('stats.png')
        self.screen.blit(statsImg, (left+10, 53))


    def game_window(self, event):
        if self.AI != 'user/no AI':
            self.username  = self.AI
        self.thisgame.run(event, self.screen, self.myfont, self.username, self.AI, self.mode)
        if self.thisgame.end(event):
            self.window = 'start'

    def toggle_multicolor(self):
        if self.mode == 'unique colors':
            self.mode = 'multicolor'
        else:
            self.mode = 'unique colors'




mysession = Gamesession()
mysession.run()







pygame.quit()