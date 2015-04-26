#########################
#
#  created by 4NNA  2015 # 
#
#########################
import random
import itertools


class Mastermind:

    def __init__(self, colors = 8 , bins = 4, repeat = False):
        self.history = []
        #number of fields for solution (4)
        self.bins = bins
        #number of colors to choose from (8)
        self.colors = [str(k) for k in range(1, colors + 1)]
        #repeated colors? ( False by default)
        self.repeat = repeat
        # initialize solution
        if repeat == False:
            self.solution = random.sample(self.colors, self.bins)
            self.possibles = list(itertools.permutations(self.colors, self.bins))
            self.possibles = [list(sam) for sam in self.possibles]
        else:
            self.solution = [str(random.randint(1, colors)) for i in range(bins)]
            self.possibles = [[str(i), str(j), str(k), str(l)] 
                                for i in range(1, colors + 1) 
                                  for j in range(1, colors + 1) 
                                    for k in range(1, colors + 1) 
                                      for l in range(1, colors + 1)]
        #practice mode
        self.practice = False  
    

    def remainingPossibilities(self):
        """ number of remaining possible solutions """
        return len(self.possibles)


    def updatePossibilities(self):
        """ number of remaining possibile solutions 
            get reduced with each new game step"""
        newpossibles = []
        for sam in self.possibles:   
            if self.couldBeSolution(sam):
                newpossibles.append(sam)
        self.possibles = newpossibles


    def wrongInput(self, my_sol):
        """ function for practice mode: 
            tells if the played guess is incongruent with earlier game steps"""
        if my_sol not in self.possibles:
            print 'not possible, try again'
            return True
        return False


    def getGuess(self, smart = False):
        """function for walkthrough mode: game guesses itself. 
            smart guess: only choose from remaining possible solutions
            not so smart guess: randomly guess """
        if smart == True:
            guess = random.sample(self.possibles, 1)[0]
        else:
            guess = random.sample(self.colors, self.bins)
        return guess


    def couldBeSolution(self, sam):
        """ is the guess congruent with the given information 
            from earlier game steps? given the previous information, 
            could it be a solution?"""
        sol = self.solution
        for hsam in self.history:        
            if (self.getPinNumbers(hsam, sam) != self.getPinNumbers(hsam, sol) or\
                self.getBlackPins(hsam, sam) != self.getBlackPins(hsam, sol)):
                return False    
        return True
       

    def writePins(self, blackpins, whitepins):
        """ print black (X) and white (O) pins to std out """
        if blackpins + whitepins > self.bins: 
            return('error')
        nopins = self.bins - (blackpins + whitepins)
        print 'X' * blackpins + 'W' * whitepins + 'O' * nopins


    def writeSolution(self):
        """ print solution to std.out """
        solutionstring = "".join(self.solution)
        print(solutionstring)


    def getBlackPins(self, my_sol, solution):
        """ get the number of correct pins (color and position is correct)"""
        blackpins = 0
        for i in range(self.bins):
            if my_sol[i] == solution[i]:
                blackpins += 1
        return blackpins 


    def getPinNumbers(self, my_sol, solution):
        """ get the total number of pins (color is in the solution)"""
        tempsolution = solution[:]
        pins = 0 
        for s in my_sol:
            if s in tempsolution:
                pins += 1
                tempsolution.pop(tempsolution.index(s))
        return pins

    
    def getPins(self, my_sol):
        """get the number of black and white pins"""
        allPins = self.getPinNumbers(my_sol, self.solution)
        blackPins = self.getBlackPins(my_sol, self.solution)
        whitePins = allPins - blackPins
        return (blackPins, whitePins)


    def isCorrect(self, my_sol):
        """ you found the correct solution"""
        return my_sol == self.solution


    def storeGuess(self, guess):
        """ write guess to history, 
            in order to calculate remaining possible solutions """
        self.history.append(guess)
        return self.isCorrect(guess)


    def start(self):

        #you have 10 trials
        for count in range(1, 11):

            #prompt for solution
            my_sol = raw_input('<%i>| '%(count))
            my_sol = [k for k in my_sol]

            #in practice mode: try again until your guess makes sense
            if self.practice == True:
                while (self.wrongInput(my_sol)):
                    my_sol = raw_input('<%s>| '%(count))
                    my_sol = [k for k in my_sol]

            self.storeGuess(my_sol)
            if my_sol == self.solution:
                print ('you won')
                self.writeSolution()
                return()

            #calculate black and white pins
            (blackpins, whitepins) = self.getPins(my_sol)
            # write black and white pins
            self.writePins(blackpins, whitepins)
            #calculate possibilities
            self.updatePossibilities()
            left = self.remainingPossibilities()
            print left, ' possibilities remain'
        print ('you lost')
        self.writeSolution()

if __name__ == '__main__':
    main()
