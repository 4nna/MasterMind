#########################
#
#  created by 4NNA  2015 # 
#
#########################
import random
import itertools
import pygame
import mastermind
import time
import os
def draw_background():
    #button grid
    for x in X_POS:
        for y in Y_POS:
            pygame.draw.circle(screen, GREY, [x, y], 10)

    #pin background grid
    pygame.draw.rect(screen, GREY, [250, 75, 50, 500 ])
    for y in Y_POS:
        pygame.draw.rect(screen, DARKGREY, [255, y - 21, 40, 40])
        draw_pinquarter(0, 0, 275, y)

    #solution base
    pygame.draw.rect(screen, GREY, [25, 25, 200, 40])

    #color buttons
    for k in range(1, 9):
        y = 50 + k * 60 
        pygame.draw.circle(screen, COLOR[k], [350, y], 12)

    #help icon
    myfont.set_bold(True)
    pygame.draw.circle(screen, COLOR[helpcolor], [350,40],26)
 #   helpcircle = pygame.Circle(26)
    helplabel = myfont.render("?", 1, BLACK)
    textpos = helplabel.get_rect()
    textpos.centerx = 350 #screen.get_rect().centerx
    textpos.centery = 40 #screen.get_rect().centery
    screen.blit(helplabel, textpos)
    myfont.set_bold(False)

    #menu
    pygame.draw.rect(screen, (220, 220, 220), [0, 600, 400, 75 ])
    pygame.draw.rect(screen, BLACK, [0, 600, 400, 3])
    #check button 
    myfont.set_bold(True)
    checklabel = myfont.render("Check!", 1, BLACK)
    screen.blit(checklabel, (20, 615))
    #start button
    startlabel = myfont.render("Start", 1, BLACK)
    screen.blit(startlabel, (100, 615))
    #toggle color repetition
    if repeat == 1:
        repeatlabel = myfont.render("No unique", 1, BLACK)
        screen.blit(repeatlabel, (172, 607))
    if repeat == 0:
        repeatlabel = myfont.render("Unique", 1, BLACK)
        screen.blit(repeatlabel, (180, 607))
    repeatlabel = myfont.render("Color", 1, BLACK)
    screen.blit(repeatlabel, (180, 625))
    #leader board
    repeatlabel = myfont.render("Leader", 1, BLACK)
    screen.blit(repeatlabel, (260, 607))
    leaderlabel = myfont.render("board", 1, BLACK)
    screen.blit(leaderlabel, (260, 625))
    #counter
    if run_time == True:
        t = time.time() - t1
    else:
        t = t2 - t1
    minut = int(t / 60)
    sec = int(t%60)
    timestring = "{:}:{:0>2d}".format(minut, sec)
    timelabel = myfont.render(timestring, 1, BLACK)
    screen.blit(timelabel, (340, 615))
    myfont.set_bold(False)


def draw_game():
    #game action
    draw_pins()
    draw_buttons()
    draw_currentRow()
    #pop-up messages
    if mes['won'] == True:
        draw_messages('YOU WON')
        if not had_help:
            add_message('%i points (%i sec, %i moves)'%(score, t2-t1, row+1))
    elif mes['pins'] == True:
        draw_messages('Choose four colors')
    elif mes['lost'] == True:
        draw_messages('YOU LOST')
    elif mes['show_leader'] == True:
        show_leaderboard()
    #toggle solution and display of remaining possibilities
    if mes['show_solution'] == True:
        show_solution()
    else: 
        poslabel = myfont.render("%i possibilities"%(possibilities), 1, BLACK)
        screen.blit(poslabel, (40, 30))


def draw_messages(text):
    """"draws popup box and message text"""
    pygame.draw.rect(screen, MESSAGECOLOR, [50, 200, 255, 100])
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (120, 220))
    pygame.draw.rect(screen, (240, 150, 50), [140, 270 ,60, 22])
    label2 = myfont.render('OK', 1, BLACK)
    screen.blit(label2, (160, 270))


def add_message(text): #hack for new line
    """ hack for second line of message"""
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (70, 250))


def show_leaderboard():
    import pandas as pd
    #draw background
    pygame.draw.rect(screen, MESSAGECOLOR, [50, 100, 255, 200])
    #write 5 best entries of leaderboard
    myfont.set_bold(True)
    label = myfont.render("Leaderboard", 1, BLACK)
    screen.blit(label, (100, 107))
    myfont.set_bold(False)
    label = myfont.render("Date            Score", 1, BLACK)
    screen.blit(label, (100, 130))
    if os.path.exists('.mastermind.log'):
        #read in leaderboard
        leaderboard = pd.read_csv('.mastermind.log')
        #sort leaderboard
        leaderboard = leaderboard.sort_values(by=['score'], ascending = False)

        N = min (5, leaderboard.shape[0])
        for i in range(N):
            leaderline = "    ".join([ str(entry) 
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


def draw_currentRow():
    """draws little triangle to indicate current row"""
    x = 10
    if row <= 9:
        y = Y_POS[row]
        pointlist = [(5, y-5), (10, y),(5, y+5)]
        pygame.draw.polygon(screen, BLACK, pointlist)


def draw_pins():
    """draws correction of guess (black and white pins)"""
    x = 275
    for i in range(len(pin_grid)):
        (b, w) = pin_grid[i]
        y = Y_POS[i]
        draw_pinquarter(b, w, x, y)


def draw_pinquarter(b, w, x, y):
    pinc=[]
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
            if col_code != None:
                pygame.draw.circle(screen, COLOR[col_code], 
                                   [X_POS[j], Y_POS[i]], 11)


def toggleMessage():
    global mes
    if mes['pins'] == True:
        mes['pins'] = False
    if mes['won'] == True:
        mes['won'] = False
        start()   
    if mes['lost'] == True:
        mes['lost'] = False
        start()             
    if mes['show_leader'] == True:
        mes['show_leader'] = False
    if mes['show_solution'] == True:
        mes['show_solution'] = False


def inCurrentRow(pos):
    x = pos[0]
    y = pos[1]
    ylim = Y_POS[row]
    return (y < ylim + 15 and  y > ylim - 15 and x < max(X_POS) and x > min(X_POS)) 


def inHelpArea(pos):
    x = pos[0]
    y = pos[1]
    return( y > 30 and y < 50 and x > 330 and x < 370)


def inColorArea(pos):
    x = pos[0]
    y = pos[1]
    return y > 60 and x < 400 and x > 300 
 

def inOKArea(pos):
    x = pos[0]
    y = pos[1]
    return y > 240 and y < 320 and x < 210 and x > 130 


def inCheckButtonArea(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and x < 90  


def inStartArea(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and x > 100 and x < 170  


def inToggleRepeatArea(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and x > 180 and x < 260  


def inLeaderBoardArea(pos):
    x = pos[0]
    y = pos[1]
    return y > 600 and x > 250 and x < 340  


def getColor(pos):
    c = getColorCode(pos)
    return COLOR[c]


def getColorCode(pos):
    """ select Color for guess"""
    x = pos[0]
    y = pos[1]
    if x > 400 or x < 300: 
        return None
    c = (y - 25) /60
    c = int(c)
    if c in range(1, 9):
        return c
    else:
        return None


def removePinFromGrid(pos):
    global column, row, button_grid
    x = pos[0]
    diffx = [abs(x - x2) for x2 in X_POS]
    column = diffx.index(min(diffx))
    button_grid[row][column] = None


def updateGrid(pos):
    global column, row, button_grid
    column = column % 4
    button_grid[row][column] = getColorCode(pos)
    column += 1


def archive():
    """ write score into leader board"""
    global score
    zeit = t2 - t1
    score = int(500000. / zeit / (row + 1))
    if not os.path.exists('.mastermind.log'):
        with open('.mastermind.log','w') as f:
            f.write('date,rows,time,score,repeat \n')
    with open('.mastermind.log', 'a') as f:
        f.write(time.strftime("%Y-%m-%d") + ', ' 
                + str(row+1) + ', ' 
                + str(zeit) + ', ' 
                + str(score) + ', ' 
                + str(repeat) + '\n')
        

def eventButtonPressed():
    """ check guess/ solution """
    global column, row, button_grid, pin_grid 
    global this_mind, mes, possibilities, t2, run_time
    mes['pins'] = False
    this_guess = button_grid[row]
    this_guess = [str(k) for k in this_guess]
    #check if all 4 color buttons have a color
    for buttoncolor in this_guess:
        if buttoncolor == 'None':
            mes['pins'] = True
            return()
    #get correction for guess
    (b, w) = this_mind.getPins(this_guess)
    pin_grid.append((b, w))
    this_mind.storeGuess(this_guess)
    if b == 4:
        mes['won'] = True
        t2 = time.time()
        run_time = False
        mes['show_solution'] = True
        if not had_help:
            archive()
        return()
    this_mind.updatePossibilities()
    possibilities = this_mind.remainingPossibilities()
    row += 1       
    if row > 9:
        mes['lost'] = True
        mes['show_solution'] = True
        run_time = False
    column = 0


def compatibleGuess(this_guess, this_mind):

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
    global helpcolor, help_active, had_help
    helpcolor = 1
    help_active = 0
    repeat = 0
    had_help = False
    # stores all correction pins (black and white)
    pin_grid = []

    # stores all color guesses
    button_grid = [[None]*4 for k in range(10)]

    #starting row and column
    row = 0
    column = 0

    #initiate mastermind session
    this_mind = mastermind.Mastermind(repeat = repeat)
    possibilities = this_mind.remainingPossibilities()

    #start timer
    t1 = time.time()
    t2 = None
    run_time = True
 

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
COLOR[1] =   WHITE 
COLOR[2] =   YELLOW 
COLOR[3] =   ORANGE 
COLOR[4] =   RED 
COLOR[5] =   GREEN 
COLOR[6] =   BLUE  
COLOR[7] =   BROWN 
COLOR[8] =   BLACK 

# Define mouse buttons
LEFT = 1

# guess positions:
X_POS = [50, 100, 150, 200]
Y_POS = range(550, 99, -50) 

#some toggle messages
mes = {}
mes['won'] = False
mes['pins'] = False
mes['lost'] = False
mes['show_leader'] = False
mes['show_solution'] = False

#start pygame and set initial conditions
start()
pygame.init()

#choose font
myfont = pygame.font.SysFont("arial", 17)

#start window
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

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            if inColorArea(event.pos):
                updateGrid(event.pos)
            elif inCheckButtonArea(event.pos):
                eventButtonPressed()
            elif inStartArea(event.pos):
                start()
            elif inToggleRepeatArea(event.pos):
                repeat = 1 - repeat
                start()
            elif inLeaderBoardArea(event.pos):
                mes['show_leader'] = True               
            elif inOKArea(event.pos):
                toggleMessage()
            elif inCurrentRow(event.pos):
                removePinFromGrid(event.pos)
            elif inHelpArea(event.pos):
                help_active = 1 - help_active 
                helpcolor = help_active + 1
                had_help = True


    if help_active:
        this_guess = button_grid[row]
        this_guess = [str(k) for k in this_guess]
        if 'None' in this_guess:
            if compatibleGuess(this_guess, this_mind):
                helpcolor = 2
            else:
                helpcolor = 4
        if not 'None' in this_guess:
        #    this_guess = [str(k) for k in this_guess]
            if this_guess not in this_mind.possibles:
                helpcolor = 4
            else:
                helpcolor = 2
 #       else:
 #           helpcolor = 2

    # --- Drawing 
    screen.fill(BACKGROUND)
    draw_background()
    draw_game()

    # ---  update the screen .
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
