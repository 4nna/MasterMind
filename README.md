# MasterMind
MasterMind game, created using pygame

Remarks: so far there are still a few bugs, but it's functional.

to start the game, run: python mastermindgame.py

how to play: (http://en.wikipedia.org/wiki/Mastermind_(board_game) )
>> goal: guess pattern of 4 colours.
select the colours from the color pegs at the right. 
click on your selection to remove pegs again from  field.
press "check"- button to check the guess.
if it is correct, you win.
for every color peg that is correct (correct color, correct position) you get one black pin
for every color that is correct but in the wrong position you get one white pin.
MENU:
- "start": start game again
- "check": check guess
- "leader board": show leaderboard
- "unique colors": toggle unique colors
- "?": see if your guess follows logically from previous hints
you can toggle "unique colors" to guess solutions with only unique colors or with the possibilitiy of repeated colors
if you click the "?" help gets activated. If help is active, the "?" circle becomes yellow. Whenever your guess is incompatible with previous hints, the "? "- circle turns red. 


TODO:
- fix bugs
- option to include name in leaderboard
- prettify design
- implement the 'practice mode' 
- show stats
