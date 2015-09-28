#imported functions
import random
import simplegui
import math
# global variables
guess = 0
secret_number = 0
guesses_left = 0
#rangeswitch is what I used to check whether the user
#picked range100 or range1000
rangeswitch = 0

def new_game():
    range100()

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number, guesses_left, rangeswitch
    secret_number = random.randrange(1,100)
    guesses_left = 7
    rangeswitch = 0
    return secret_number

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number, guesses_left, rangeswitch
    secret_number = random.randrange(1,1000)
    guesses_left = 10
    rangeswitch = 1
    return secret_number
    
def input_guess(guess):
    # main game logic goes here
    global guesses_left, secret_number, rangeswitch
    guess_number = int(guess)
    print "Guess is", guess_number
    if guess_number > secret_number:
        print "Lower"
        guesses_left = guesses_left - 1
        print "You have", guesses_left, "guesses left"
    elif guess_number < secret_number:
        print "Higher"
        guesses_left = guesses_left - 1
        print "You have", guesses_left, "guesses left"
    elif guess_number == secret_number:
        print "Correct"
        if rangeswitch == 0:
            range100()
        elif rangeswitch == 1:
            range1000()
        print
    else:
        print "Error"
    if guesses_left == 0 and rangeswitch == 0:
        range100()
    elif guesses_left == 0 and rangeswitch == 1:
        range1000()
    print

    
    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements and start frame
frame.add_input("Enter a Guess", input_guess, 100)
frame.add_button("Range is[0,100]", range100, 100)
frame.add_button("Range is[0,1000]", range1000, 100)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
