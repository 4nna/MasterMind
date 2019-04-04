#########################
#
#  created by 4NNA  2015 # 
#
#########################
import random
# import itertools
# import numpy as np
import pygame
import mastermind
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
#class MasterMindGame(pygame):
# init = session_start, set global vars,
# reset = start
# make menu: -> register with name?, select AI-agent?
#            -> see stats (last 10 games, all games, you comppared to average or median)
# or : when fist won : ask for name / option for changing name


def draw_background():
    # button grid
    for x in X_POS:
        for y in Y_POS:
            pygame.draw.circle(screen, GREY, [x, y], 10)

    # pin background grid
    pygame.draw.rect(screen, GREY, [250, 75, 50, 500])
    for y in Y_POS:
        pygame.draw.rect(screen, DARKGREY, [255, y - 21, 40, 40])
        draw_pinquarter(0, 0, 275, y)

    # solution base
    pygame.draw.rect(screen, GREY, [25, 25, 200, 40])

    # color buttons
    for k in range(1, 9):
        y = 50 + k * 60 
        pygame.draw.circle(screen, COLOR[k], [350, y], 12)

    # help icon
    myfont.set_bold(True)
    pygame.draw.circle(screen, COLOR[helpcolor], [350, 40], 26)
    # helpcircle = pygame.Circle(26)
    helplabel = myfont.render("?", 1, BLACK)
    textpos = helplabel.get_rect()
    textpos.centerx = 350  # screen.get_rect().centerx
    textpos.centery = 40  # screen.get_rect().centery
    screen.blit(helplabel, textpos)
    myfont.set_bold(False)

    # menu
    pygame.draw.rect(screen, (220, 220, 220), [0, 600, 400, 75])
    pygame.draw.rect(screen, BLACK, [0, 600, 400, 3])
    # check button
    myfont.set_bold(True)
    checklabel = myfont.render("Check!", 1, BLACK)
    screen.blit(checklabel, (20, 615))
    # start button
    startlabel = myfont.render("Start", 1, BLACK)
    screen.blit(startlabel, (100, 615))
    # toggle color repetition
    if repeat:
        repeatlabel = myfont.render("No unique", 1, BLACK)
        screen.blit(repeatlabel, (172, 607))
    if not repeat:
        repeatlabel = myfont.render("Unique", 1, BLACK)
        screen.blit(repeatlabel, (180, 607))
    repeatlabel = myfont.render("Color", 1, BLACK)
    screen.blit(repeatlabel, (180, 625))
    # leader board
    repeatlabel = myfont.render("Leader", 1, BLACK)
    screen.blit(repeatlabel, (260, 607))
    leaderlabel = myfont.render("board", 1, BLACK)
    screen.blit(leaderlabel, (260, 625))
    # AI
    ailabel = myfont.render("AI", 1, BLACK)
    screen.blit(ailabel, (340, 615))
    myfont.set_bold(False)
  #  # counter
  #  if run_time:
  #      t = time.time() - t1
  #  else:
  #      t = t2 - t1
  #  minut = int(t / 60)
  #  sec = int(t % 60)
  #  timestring = "{:}:{:0>2d}".format(minut, sec)
  #  timelabel = myfont.render(timestring, 1, BLACK)
  #  screen.blit(timelabel, (340, 615))
  #  myfont.set_bold(False)


def draw_game():
    # game action
    draw_pins()
    draw_buttons()
    draw_current_row()
    draw_current()
    # pop-up messages
    if mes['won'] is True:
        draw_messages('YOU WON')
        if not had_help:
            add_message('%i points (%i sec, %i moves)' % (score, t2-t1, row+1))
    elif mes['pins'] is True:
        draw_messages('Choose four colors')
    elif mes['lost'] is True:
        draw_messages('YOU LOST')
    elif mes['show_leader'] is True:
        show_leaderboard()
    # toggle solution and display of remaining possibilities
    if mes['show_solution'] is True:
        show_solution()
    else: 
        poslabel = myfont.render("%i possibilities" % (possibilities), 1, BLACK)
        screen.blit(poslabel, (40, 30))
        # counter
        if run_time:
            t = time.time() - t1
        else:
            t = t2 - t1
        minut = int(t / 60)
        sec = int(t % 60)
        timestring = "{:}:{:0>2d}".format(minut, sec)
        timelabel = myfont.render(timestring, 1, BLACK)
        screen.blit(timelabel, (170, 30))



def draw_messages(text):
    """"draws popup box and message text"""
    pygame.draw.rect(screen, MESSAGECOLOR, [50, 200, 255, 100])
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (120, 220))
    pygame.draw.rect(screen, (240, 150, 50), [140, 270, 60, 22])
    label2 = myfont.render('OK', 1, BLACK)
    screen.blit(label2, (160, 270))


def add_message(text):  # hack for new line
    """ hack for second line of message"""
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (70, 250))


def show_leaderboard():
    # draw background
    pygame.draw.rect(screen, MESSAGECOLOR, [50, 100, 255, 200])
    # write 5 best entries of leaderboard
    myfont.set_bold(True)
    label = myfont.render("Leaderboard", 1, BLACK)
    screen.blit(label, (100, 107))
    myfont.set_bold(False)
    label = myfont.render("Date            Score", 1, BLACK)
    screen.blit(label, (100, 130))
    if os.path.exists('.mastermind.log'):
        # read in leaderboard
        leaderboard = pd.read_csv('.mastermind.log')
        # sort leaderboard
        leaderboard = leaderboard.sort_values(by=['score'], ascending=False)

        N = min(5, leaderboard.shape[0])
        for i in range(N):
            leaderline = "    ".join([str(entry)
                                     for entry in leaderboard.iloc[i, [0, 3]]])
            label = myfont.render(leaderline, 1, BLACK)
            screen.blit(label, (100, 150+i*20))
    pygame.draw.rect(screen, (240, 150, 50), [140, 270, 60, 22])
    label2 = myfont.render('OK', 1, BLACK)
    screen.blit(label2, (160, 270))


def show_solution():
    """shows solution, when game is over"""
    solution = [int(k) for k in this_mind.solution]
    y = 45
    for i in range(4):
        x = X_POS[i]
        pygame.draw.circle(screen, COLOR[solution[i]], [x, y], 10)


def draw_current_row():
    """draws little triangle to indicate current row"""
    # x = 10
    if row <= 9:
        y = Y_POS[row]
        pointlist = [(5, y-5), (10, y), (5, y+5)]
        pygame.draw.polygon(screen, BLACK, pointlist)


def draw_current():
    if row<= 9:
        pygame.draw.circle(screen, YELLOW,
                       [X_POS[column], Y_POS[row]], 12, 2)


def draw_pins():
    """draws correction of guess (black and white pins)"""
    x = 275
    for i in range(len(pin_grid)):
        (b, w) = pin_grid[i]
        y = Y_POS[i]
        draw_pinquarter(b, w, x, y)


def draw_pinquarter(b, w, x, y):
    pinc = []
    for i in range(b):
        pinc.append(BLACK)
    for i in range(w):
        pinc.append(WHITE)
    for i in range(4 - b - w):
        pinc.append(GREY)
    pygame.draw.circle(screen, pinc[0], [x - 10, y - 10], 5)
    pygame.draw.circle(screen, pinc[1], [x + 10, y - 10], 5)
    pygame.draw.circle(screen, pinc[2], [x - 10, y + 10], 5)
    pygame.draw.circle(screen, pinc[3], [x + 10, y + 10], 5)


def draw_buttons():
    """ draws game history, color button guesses"""
    for i in range(len(button_grid)):
        button_line = button_grid[i]
        for j in range(len(button_line)):
            col_code = button_line[j]    
            if col_code is not None:
                pygame.draw.circle(screen, COLOR[col_code], 
                                   [X_POS[j], Y_POS[i]], 11)


def toggle_message():
    global mes
    if mes['pins'] is True:
        mes['pins'] = False
    if mes['won'] is True:
        mes['won'] = False
        start()   
    if mes['lost'] is True:
        mes['lost'] = False
        start()             
    if mes['show_leader'] is True:
        mes['show_leader'] = False
    if mes['show_solution'] is True:
        mes['show_solution'] = False


def incurrent_row(pos):
    x = pos[0]
    y = pos[1]
    ylim = Y_POS[row]
    return -15 < y - ylim < 15 and min(X_POS) < x < max(X_POS)


def in_help_area(pos):
    x = pos[0]
    y = pos[1]
    return 30 < y < 50 and 330 < x < 370


def in_color_area(pos):
    x = pos[0]
    y = pos[1]
    return 60 < y < 600 and 300 < x < 400
 
def in_ai_area(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and 300 < x < 400

def in_ok_area(pos):
    x = pos[0]
    y = pos[1]
    return 240 < y < 320 and 130 < x < 210


def in_checkbutton_area(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and x < 90  


def in_start_area(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and 100 < x < 170


def in_toggle_repeat_area(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and 180 < x < 260


def in_leader_board_area(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and 250 < x < 340


def get_color(pos):
    c = get_color_code(pos)
    return COLOR[c]


def get_color_code(pos):
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


def remove_pin_from_grid(pos):
    global column, row, button_grid
    x = pos[0]
    diffx = [abs(x - x2) for x2 in X_POS]
    column = diffx.index(min(diffx))
    button_grid[row][column] = None


def undo_last():
    global column, row, button_grid
    column -= 1
    column = column % 4
    button_grid[row][column] = None

def update_grid(color):
    global column, row, button_grid
    button_grid[row][column] = color
    column += 1
    column = column % 4

def fill_row_automatically(possibilities):
    one_option = random.sample(possibilities,1)[0]
    one_option = [int(k) for k in one_option]
    button_grid[row] = one_option




def archive():
    """ write score into leader board"""
    global score
    zeit = t2 - t1
    score = int(500000. / zeit / (row + 1))
    if not os.path.exists('.mastermind.log'):
        with open('.mastermind.log', 'w') as f:
            f.write('date,rows,time,score,repeat \n')
    with open('.mastermind.log', 'a') as f:
        f.write(time.strftime("%Y-%m-%d") + ', ' 
                + str(row+1) + ', ' 
                + str(zeit) + ', ' 
                + str(score) + ', ' 
                + str(repeat) + '\n')

# initialize game when starting mastermind, from logs.
def archive_sessions( game, dt, colors, pins, remaining_possibilities, name='Guest'):
    """ write all steps and choices and results for statistics"""
    global sessionlogfile
    with open(sessionlogfile,'a') as f:
        f.write(time.strftime("%Y-%m-%d") + ', '
                + str(game) + ', '
                + str(repeat) + ', '
                + str(name) + ', '
                + str(dt) + ', '
                + str(row + 1) + ', '
                + str(colors) + ', '
                + str(pins) + ', '
                + str(remaining_possibilities) + '\n')

def stats():
    pdf = pd.read_csv(sessionlogfile, header=None)
    pdf.columns = ['date', 'game', 'repeat', 'name','dt', 'steps', 'col1','col2','col3','col4', 'pin_black','pin_white', 'reduced_possibilities']
    gdf = pdf.groupby(['game'])['steps','dt'].max()
    print(gdf.head())
    print('min steps:', gdf.steps.min())
    print('median steps:', gdf.steps.median())
    print('min time:', gdf.dt.min())
    print('median time:', gdf.dt.median() )
    plt.plot(pdf.steps, pdf.reduced_possibilities)
    plt.show()
#    ndf = pdf.groupby(['name'])['steps','dt','game'].agg([min, min, nunique()]
# possibility reduction per step
# number of steps until solution
# time until solution
# number of incompatible moves (i.e. not fitting to pins) - this is not necessarily bad..
#give each AI agent a name... for stats...

def event_button_pressed():
    """ check guess/ solution """
    global column, row, button_grid, pin_grid 
    global this_mind, mes, possibilities, t1, t2, run_time, name
    mes['pins'] = False
    this_guess = button_grid[row]
    this_guess = [str(k) for k in this_guess]
    # check if all 4 color buttons have a color
    for buttoncolor in this_guess:
        if buttoncolor == 'None':
            mes['pins'] = True
            return()
    # get correction for guess
    (b, w) = this_mind.get_pins(this_guess)
    pin_grid.append((b, w))
    this_mind.store_guess(this_guess)
    this_mind.update_possibilities()
    archive_sessions(game,
                     time.time() - t1,
                     ",".join(this_guess),
                     ",".join([str(b), str(w)]),
                     possibilities-this_mind.remaining_possibilities(),
                     name=name)
    if b == 4:
        mes['won'] = True
        t2 = time.time()
        run_time = False
        mes['show_solution'] = True
        if not had_help:
            archive()
        return()

    possibilities = this_mind.remaining_possibilities()
    row += 1       
    if row > 9:
        mes['lost'] = True
        mes['show_solution'] = True
        t2 = time.time()
        run_time = False
    column = 0


def compatible_guess(this_guess, this_mind):

    for guess in this_mind.possibles:
        if ((guess[0] == this_guess[0] or this_guess[0] == 'None') and 
            (guess[1] == this_guess[1] or this_guess[1] == 'None') and 
            (guess[2] == this_guess[2] or this_guess[2] == 'None') and 
            (guess[3] == this_guess[3] or this_guess[3] == 'None') ):
            return True
    return False


def start():
    """ initiate game, reset all"""
    global column, row, pin_grid, button_grid 
    global this_mind, possibilities, t1, repeat, run_time
    global helpcolor, help_active, had_help, game
    helpcolor = 1
    help_active = 0
   # repeat = False
    had_help = False
    # stores all correction pins (black and white)
    pin_grid = []

    # stores all color guesses
    button_grid = [[None]*4 for _ in range(10)]

    # starting row and column
    row = 0
    column = 0

    # initiate mastermind session
    this_mind = mastermind.Mastermind(repeat=repeat)
    possibilities = this_mind.remaining_possibilities()

    # start timer
    t1 = time.time()
    t2 = None
    run_time = True
    game += 1
#global variables and their defaults
helpcolor = 1
help_active = 0
repeat = False
had_help = False
# stores all correction pins (black and white)
pin_grid = []

# stores all color guesses
button_grid = [[None] * 4 for _ in range(10)]

# starting row and column
row = 0
column = 0

this_mind = mastermind.Mastermind(repeat=repeat)
possibilities = this_mind.remaining_possibilities()

# start timer
t1 = time.time()
t2 = None
run_time = True

game = 0 #read from sessionlog
name = 'anna'
sessionlogfile = '.mastermind_session.log'

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

# some toggle messages
mes = {}
mes['won'] = False
mes['pins'] = False
mes['lost'] = False
mes['show_leader'] = False
mes['show_solution'] = False

# start pygame and set initial conditions
#session_start()
start()
pygame.init()

# choose font
myfont = pygame.font.SysFont("arial", 17)

# start window
size = (400, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My MasterMind")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                if run_time:
                    event_button_pressed()
                else:
                    toggle_message()
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]: #\
#                    or event.key in [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8]:
                update_grid(event.key-48)
            elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                undo_last()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            if in_color_area(event.pos):
                color = get_color_code(event.pos)
                update_grid(color)
            elif in_checkbutton_area(event.pos) and run_time:
                event_button_pressed()
            elif in_start_area(event.pos):
                start()
            elif in_toggle_repeat_area(event.pos):
                repeat = not repeat
                start()
            elif in_leader_board_area(event.pos):
                mes['show_leader'] = True
                stats()
            elif in_ai_area(event.pos):
                #fill_row_automatically(this_mind.possibles)
                #had_help = True
                # start self run via AI.
                # set name=AI
                pass
            elif in_ok_area(event.pos):
                toggle_message()
            elif incurrent_row(event.pos):
                remove_pin_from_grid(event.pos)
            elif in_help_area(event.pos):
                #implement here: the row-help via AI. i.e.
                # if color is red and clicked again: set via AI.
                help_active = 1 - help_active 
                helpcolor = help_active + 1
                had_help = True
    if help_active:
        this_guess = button_grid[row]
        this_guess = [str(k) for k in this_guess]
        if 'None' in this_guess:
            if compatible_guess(this_guess, this_mind):
                helpcolor = 2
            else:
                helpcolor = 4
        if 'None' not in this_guess:
            # this_guess = [str(k) for k in this_guess]
            if this_guess not in this_mind.possibles:
                helpcolor = 4
            else:
                helpcolor = 2
        # else:
            # helpcolor = 2

    # --- Drawing 
    screen.fill(BACKGROUND)
    draw_background()
    draw_game()


    # ---  update the screen .
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
