#########################
#
#  created by 4NNA  2015 # 
#
#########################
import random
import itertools


class Mastermind:

    def __init__(self, colors=8, bins=4, repeat=False):
        self.history = []
        # number of fields for solution (4)
        self.bins = bins
        # number of colors to choose from (8)
        self.colors = [str(k) for k in range(1, colors + 1)]
        # repeated colors? ( False by default)
        self.repeat = repeat
        # initialize solution
        if not repeat:
            self.solution = random.sample(self.colors, self.bins)
            self.possibles = list(itertools.permutations(self.colors, self.bins))
            self.possibles = [list(sam) for sam in self.possibles]
        else:
            self.solution = [str(random.randint(1, colors)) for _ in range(bins)]
            self.possibles = [[str(i), str(j), str(k), str(l)] 
                                for i in range(1, colors + 1) 
                                  for j in range(1, colors + 1) 
                                    for k in range(1, colors + 1) 
                                      for l in range(1, colors + 1)]
        # practice mode
        self.practice = False  

    def remaining_possibilities(self):
        """ number of remaining possible solutions """
        return len(self.possibles)

    def update_possibilities(self):
        """ number of remaining possibile solutions 
            get reduced with each new game step"""
        newpossibles = []
        for sam in self.possibles:   
            if self.could_be_solution(sam):
                newpossibles.append(sam)
        self.possibles = newpossibles

    def wrong_input(self, my_sol):
        """ function for practice mode: 
            tells if the played guess is incongruent with earlier game steps"""
        if my_sol not in self.possibles:
            print('not possible, try again')
            return True
        return False

    def get_guess(self, smart=False):
        """function for walkthrough mode: game guesses itself. 
            smart guess: only choose from remaining possible solutions
            not so smart guess: randomly guess """
        if smart:
            guess = random.sample(self.possibles, 1)[0]
        else:
            guess = random.sample(self.colors, self.bins)
        return guess

    def could_be_solution(self, sam):
        """ is the guess congruent with the given information 
            from earlier game steps? given the previous information, 
            could it be a solution?"""
        sol = self.solution
        for hsam in self.history:        
            if (self.get_pin_numbers(hsam, sam) != self.get_pin_numbers(hsam, sol) or
                self.get_black_pins(hsam, sam) != self.get_black_pins(hsam, sol)):
                return False    
        return True
       
    def write_pins(self, blackpins, whitepins):
        """ print black (X) and white (O) pins to std out """
        if blackpins + whitepins > self.bins: 
            return 'error'
        nopins = self.bins - (blackpins + whitepins)
        print('X' * blackpins + 'W' * whitepins + 'O' * nopins)

    def write_solution(self):
        """ print solution to std.out """
        solutionstring = "".join(self.solution)
        print(solutionstring)

    def get_black_pins(self, my_sol, solution):
        """ get the number of correct pins (color and position is correct)"""
        blackpins = 0
        for i in range(self.bins):
            if my_sol[i] == solution[i]:
                blackpins += 1
        return blackpins 

    def get_pin_numbers(self, my_sol, solution):
        """ get the total number of pins (color is in the solution)"""
        tempsolution = solution[:]
        pins = 0 
        for s in my_sol:
            if s in tempsolution:
                pins += 1
                tempsolution.pop(tempsolution.index(s))
        return pins

    def get_pins(self, my_sol):
        """get the number of black and white pins"""
        allpins = self.get_pin_numbers(my_sol, self.solution)
        blackpins = self.get_black_pins(my_sol, self.solution)
        whitepins = allpins - blackpins
        return blackpins, whitepins

    def is_correct(self, my_sol):
        """ you found the correct solution"""
        return my_sol == self.solution

    def store_guess(self, guess):
        """ write guess to history, 
            in order to calculate remaining possible solutions """
        self.history.append(guess)
        return self.is_correct(guess)

    def start(self):

        # you have 10 trials
        for count in range(1, 11):

            # prompt for solution
            my_sol = input('<%i>| '%(count))
            my_sol = [k for k in my_sol]

            # in practice mode: try again until your guess makes sense
            if self.practice:
                while (self.wrong_input(my_sol)):
                    my_sol = input('<%s>| '%(count))
                    my_sol = [k for k in my_sol]

            self.store_guess(my_sol)
            if my_sol == self.solution:
                print('you won')
                self.write_solution()
                return()

            # calculate black and white pins
            (blackpins, whitepins) = self.get_pins(my_sol)
            # write black and white pins
            self.write_pins(blackpins, whitepins)
            # calculate possibilities
            self.update_possibilities()
            left = self.remaining_possibilities()
            print(left, ' possibilities remain')
        print('you lost')
        self.write_solution()

if __name__ == '__main__':
    main()
