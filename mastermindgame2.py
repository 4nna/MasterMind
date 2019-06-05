import pygame
import time
import os
import mastermind
import button
from constants import *





class MastermindGame():

    def __init__(self):
        self.screen  = None
        self.myfont = None
        self.username = None
        self.AI = None
        self.mode = None
        self.repeat = None
        self.sessionlogfile = '.mastermind_session.log'
        self.logfile = '.mastermind.log'
        self.t_start = None
        self.t = None
        self.running = False
        self.active = False
        self.row = 0
        self.column = 0
        self.thismind = None
        self.possibilities = None
        self.pin_grid = []
        self.button_grid = [[None] * 4 for _ in range(10)]
        self.game = 0
        self.had_help = 0
     #BOARD
        self.checkbutton = button.Button(0, 600, 100, 50, GREY, BLACK, 'Check!', BLACK)
        self.startbutton = button.Button(100, 600, 100, 50, GREY, BLACK, 'Start', BLACK)
        self.stopbutton = button.Button(200, 600, 100, 50, GREY, BLACK, 'End', BLACK)
        #self.backbutton = button.Button(300, 600, 100, 50, GREY, BLACK, 'Back', BLACK)
        self.helpbutton = button.RoundButton(350, 40, 26, YELLOW, BLACK, '?', BLACK)

    def reset(self):
        self.row = None
        self.column = None
        self.thismind = None
        self.possibilities = None
        self.pin_grid = []
        self.button_grid = [[None] * 4 for _ in range(10)]

    def run(self, event, screen, myfont, username, ai, mode):
        self.screen = screen
        self.myfont = myfont
        self.username = username
        self.AI = ai
        self.mode = mode
        if self.mode == 'multicolor':
            self.repeat = True
        else:
            self.repeat = False
        if self.startbutton.clicked(event):
            self.start(event)
        if self.running:
            if self.checkbutton.clicked(event) or \
                    ((event.type == pygame.KEYDOWN) and
                     (event.key == pygame.K_KP_ENTER or
                      event.key == pygame.K_RETURN)):
                self.check_solution()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1,
                                 pygame.K_2,
                                 pygame.K_3,
                                 pygame.K_4,
                                 pygame.K_5,
                                 pygame.K_6,
                                 pygame.K_7,
                                 pygame.K_8]:
                    self.update_grid(event.key-48)
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    self.undo_last()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if self.in_color_area(event.pos):
                    color = self.get_color_code(event.pos)
                    self.update_grid(color)
                elif self.incurrent_row(event.pos):
                    self.remove_pin_from_grid(event.pos)
        self.draw_background()
        if self.active:
            self.draw_game()

    def end(self, event):
        return self.stopbutton.clicked(event)

    def start(self, event):
        # initiate mastermind session
        self.this_mind = mastermind.Mastermind(repeat=self.repeat)
        self.possibilities = self.this_mind.remaining_possibilities()
        self.start_timer()
        self.row = 0
        self.column = 0
        self.active = True

    def start_timer(self):
        self.t_start = time.time()
        self.running = True

    def draw_background(self):
        # button grid
        for x in X_POS:
            for y in Y_POS:
                pygame.draw.circle(self.screen, GREY, [x, y], 10)
        # pin background grid
        pygame.draw.rect(self.screen, GREY, [250, 75, 50, 500])
        for y in Y_POS:
            pygame.draw.rect(self.screen, DARKGREY, [255, y - 21, 40, 40])
            self.draw_pinquarter(0, 0, 275, y)
        # solution base
        pygame.draw.rect(self.screen, GREY, [25, 25, 200, 40])
        # color buttons
        for k in range(1, 9):
            y = 50 + k * 60
            pygame.draw.circle(self.screen, COLOR[k], [350, y], 12)
        # help icon
        self.myfont.set_bold(True)
        #pygame.draw.circle(self.screen, COLOR[2], [350, 40], 26)
        # helpcircle = pygame.Circle(26)
        #helplabel = self.myfont.render("?", 1, BLACK)
        #textpos = helplabel.get_rect()
        #textpos.centerx = 350  # self.screen.get_rect().centerx
        #textpos.centery = 40  # self.screen.get_rect().centery
        #self.screen.blit(helplabel, textpos)
        self.helpbutton.draw(self.screen, self.myfont)
        self.checkbutton.draw(self.screen, self.myfont)
        self.startbutton.draw(self.screen, self.myfont)
        self.stopbutton.draw(self.screen, self.myfont)
        #self.backbutton.draw(self.screen, self.myfont)
        self.myfont.set_bold(False)
        pygame.draw.rect(self.screen, GREY, [300, 600, 400, 3])
        selectlabel = self.myfont.render(self.username, 1, BLACK)
        selectRect = selectlabel.get_rect()
        selectRect.center = (350, 610)
        self.screen.blit(selectlabel, selectRect)

    def draw_pinquarter(self, b, w, x, y):
        pinc = []
        for i in range(b):
            pinc.append(BLACK)
        for i in range(w):
            pinc.append(WHITE)
        for i in range(4 - b - w):
            pinc.append(GREY)
        pygame.draw.circle(self.screen, pinc[0], [x - 10, y - 10], 5)
        pygame.draw.circle(self.screen, pinc[1], [x + 10, y - 10], 5)
        pygame.draw.circle(self.screen, pinc[2], [x - 10, y + 10], 5)
        pygame.draw.circle(self.screen, pinc[3], [x + 10, y + 10], 5)

    def draw_game(self):
        # game action
        self.draw_pins()
        self.draw_buttons()
        self.draw_current_row()
        self.draw_current()
        self.draw_solution_area()

    def draw_solution_area(self):
        if self.running:
            poslabel = self.myfont.render("%i possibilities" % self.possibilities, 1, BLACK)
            self.screen.blit(poslabel, (40, 30))
            timestring = self.get_time()
            timelabel = self.myfont.render(timestring, 1, BLACK)
            self.screen.blit(timelabel, (170, 30))
        else:
            self.show_solution()

    def get_time(self):
        if self.running:
            self.t = time.time() - self.t_start
        minut = int(self.t / 60)
        sec = int(self.t % 60)
        timestring = "{:}:{:0>2d}".format(minut, sec)
        return timestring

    def draw_pins(self):
        """draws correction of guess (black and white pins)"""
        x = 275
        for i in range(len(self.pin_grid)):
            (b, w) = self.pin_grid[i]
            y = Y_POS[i]
            self.draw_pinquarter(b, w, x, y)

    def draw_buttons(self):
        """ draws game history, color button guesses"""
        for i in range(len(self.button_grid)):
            button_line = self.button_grid[i]
            for j in range(len(button_line)):
                col_code = button_line[j]
                if col_code is not None:
                    pygame.draw.circle(self.screen, COLOR[col_code],
                                       [X_POS[j], Y_POS[i]], 11)

    def draw_current_row(self):
        """draws little triangle to indicate current row"""
        if self.row <= 9:
            y = Y_POS[self.row]
            pointlist = [(5, y-5), (10, y), (5, y+5)]
            pygame.draw.polygon(self.screen, BLACK, pointlist)

    def draw_current(self):
        if self.row <= 9:
            pygame.draw.circle(self.screen, YELLOW,
                               [X_POS[self.column], Y_POS[self.row]], 12, 2)

    def draw_messages(self, text):
        """"draws popup box and message text"""
        pygame.draw.rect(self.screen, MESSAGECOLOR, [50, 200, 255, 100])
        label = self.myfont.render(text, 1, BLACK)
        self.screen.blit(label, (120, 220))
        pygame.draw.rect(self.screen, (240, 150, 50), [140, 270, 60, 22])
        label2 = self.myfont.render('OK', 1, BLACK)
        self.screen.blit(label2, (160, 270))
        # ok button

    def show_solution(self):
        """shows solution, when game is over"""
        solution = [int(k) for k in self.this_mind.solution]
        y = 45
        for i in range(4):
            x = X_POS[i]
            pygame.draw.circle(self.screen, COLOR[solution[i]], [x, y], 10)

    def warning(self, text):
        pass

    def in_color_area(self, pos):
        return 300 < pos[0] < 400 and 60 < pos[1] < 600

    def get_color_code(self, pos):
        """ select Color for guess"""
        x = pos[0]
        y = pos[1]
        if x > 400 or x < 300:
            return None
        c = (y - 25) / 60
        c = int(c)
        if c in range(1, 9):
            return c
        else:
            return None

    def incurrent_row(self, pos):
        ylim = Y_POS[self.row]
        return -15 < pos[1] - ylim < 15 and min(X_POS) < pos[0] < max(X_POS)

    def remove_pin_from_grid(self, pos):
        x = pos[0]
        diffx = [abs(x - x2) for x2 in X_POS]
        column = diffx.index(min(diffx))
        self.button_grid[self.row][self.column] = None

    def update_grid(self, color):
        self.button_grid[self.row][self.column] = color
        self.column += 1
        self.column = self.column % 4

    def undo_last(self):
        self.column -= 1
        self.column = self.column % 4
        self.button_grid[self.row][self.column] = None

    def check_solution(self):
        """ check guess/ solution """
        this_guess = self.button_grid[self.row]
        this_guess = [str(k) for k in this_guess]
        # check if all 4 color buttons have a color
        for buttoncolor in this_guess:
            if buttoncolor == 'None':
                self.warning('')
                return()
        # get correction for guess
        (b, w) = self.this_mind.get_pins(this_guess)
        self.pin_grid.append((b, w))
        self.this_mind.store_guess(this_guess)
        self.this_mind.update_possibilities()
        self.archive_sessions(time.time() - self.t_start,
                         ",".join(this_guess),
                         ",".join([str(b), str(w)]),
                         self.possibilities-self.this_mind.remaining_possibilities())
        if b == 4:
            #mes['won'] = True
            self.running = False
            if not self.had_help:
                self.archive()
            return()
        self.possibilities = self.this_mind.remaining_possibilities()
        self.row += 1
        if self.row > 9:
            #mes['lost'] = True
            self.running = False
        self.column = 0

    def archive_sessions(self, dt, colors, pins, remaining_possibilities):
        """ write all steps and choices and results for statistics"""
        with open(self.sessionlogfile, 'a') as f:
            f.write(time.strftime("%Y-%m-%d") + ', '
                    + str(self.game) + ', '
                    + str(self.repeat) + ', '
                    + str(self.username) + ', '
                    + str(dt) + ', '
                    + str(self.row + 1) + ', '
                    + str(colors) + ', '
                    + str(pins) + ', '
                    + str(remaining_possibilities) + '\n')

    def archive(self):
        """ write score into leader board"""
        score = int(500000. / self.t / (self.row + 1))
        if not os.path.exists('.mastermind.log'):
            with open('.mastermind.log', 'w') as f:
                f.write('date,name,rows,time,score,repeat\n')  # no whitespaces in column names..
        with open('.mastermind.log', 'a') as f:
            f.write(time.strftime("%Y-%m-%d") + ', '
                    + str(self.username) + ', '
                    + str(self.row+1) + ', '
                    + str(self.t) + ', '
                    + str(score) + ', '
                    + str(self.repeat) + '\n')

