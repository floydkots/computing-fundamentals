# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

range_is = None

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global range_is
    global guesses_left
    
    if not range_is:
        range_is = 100
    
    guesses_left = int(math.ceil(math.log(range_is, 2)))
    secret_number = random.randrange(0, range_is) 
    print("Range is [%s,%s)" % (0, range_is))
    check_n_print_guesses_left()
    


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range_is
    range_is = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range_is
    range_is = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global guesses_left
    global secret_number
    
    guess = int(guess)
    print "Guess was", guess
    
    if (guess < secret_number):
        print("Lower")
        guesses_left -= 1
        check_n_print_guesses_left()
        
    elif (guess > secret_number):
        print("Higher")
        guesses_left -= 1
        check_n_print_guesses_left()
        
    elif (guess == secret_number):
        print("Correct\n")
        new_game()
   
            
def check_n_print_guesses_left():
    print("Number of guesses left: %s\n" % guesses_left)
    if (guesses_left < 1):
        new_game()

    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)", range100, 100)
frame.add_button("Range is [0, 1000)", range1000, 100)
frame.add_input("Your guess?", input_guess, 100)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
