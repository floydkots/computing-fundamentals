"""Floyd Kots ~ github.com/floydkots"""
# implementation of card game - Memory

import simplegui
import random

CWIDTH = 50
CHEIGHT = 100

# helper to get card polygon coordinates
def card_at(index):
    return [[0 + (index * 50),0],
            [50 + (index * 50),0],
            [50 + (index * 50),100],
            [0 + (index * 50),100]]  
    
# helper function to initialize globals
def new_game():
    global deck, exposed, state, card1, card2, turns
    card1 = None
    card2 = None
    clicked = []
    state = 0
    turns = 0
    exposed = [False] * 16
    deck = range(8) + range(8)
    random.shuffle(deck)
    
    

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1, card2, turns
    index = pos[0] // 50
    if (state == 0):
        exposed[index] = True
        card1 = index
        state = 1
    elif (state == 1):
        exposed[index] = True
        card2 = index
        state = 2
        turns += 1
    else:
        if (not exposed[index]):
            exposed[index] = True
            if (deck[card1] != deck[card2]):
                exposed[card1] = False
                exposed[card2] = False
            card1 = index
            card2 = None
            state = 1
        
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = %s" % turns)
    for index, card in enumerate(deck):
        if (exposed[index]):
            canvas.draw_text(str(card), [CWIDTH * index, CHEIGHT * .75], 70, "White")
        else:
            canvas.draw_polygon(card_at(index), 1, "Black", "Green")



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric