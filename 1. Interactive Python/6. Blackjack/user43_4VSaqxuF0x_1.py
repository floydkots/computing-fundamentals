# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
status = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)
        

class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        return "Hand contains " + " ".join(str(card) for card in self.cards)

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
        print str(self), "value:", self.get_value()

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total = 0
        has_ace = False
        for card in self.cards:
            total += VALUES[card.get_rank()]
            if not has_ace and card.get_rank() == 'A':
                has_ace = True
        return total + 10 if has_ace and total + 10 <= 21 else total
                
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for index, card in enumerate(self.cards): 
            card.draw(canvas,[index * CARD_SIZE[0] + pos[0],
                              CARD_SIZE[1] + pos[1]])
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck 
        return "Deck contains " + " ".join(str(card) for card in self.cards)



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score
    global status
    
    if in_play:
        status = "Player lost the round"
        score -= 1
    else:
        status = ""
        
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    dealer = Hand()
    
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    
    print "Dealer", str(dealer)
    print "Player", str(player)
    
    outcome = "Hit or stand?"
    in_play = True

def hit():
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global in_play, score, outcome, status
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
        if player.get_value() > 21:
            status = "Player has busted!"
            score -= 1
            in_play = False
            outcome = "New Deal?"
                
def stand():
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome, in_play, score, status
    if not in_play:
        status = "Player has busted"
    else:
        in_play = False
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            score += 1
            status = "Dealer has busted"
        else:
            if player.get_value() <= dealer.get_value():
                status = "Dealer has won!"
                score -= 1
            else:
                status = "Player has won!"
                score += 1
    outcome = "New deal?"
    
# draw handler    
def draw(canvas):
    canvas.draw_text("BLACKJACK", [150, 50], 50, "Black")
    canvas.draw_text("Score: " + str(score), [450, 130], 30, "White")
    canvas.draw_text("Dealer", [50, 130], 30, "White")
    dealer.draw(canvas, [50, 50])
    canvas.draw_text(outcome, [300, 300], 30, "Blue")
    canvas.draw_text("Player", [50, 330], 30, "White")
    player.draw(canvas, [50, 250])
    canvas.draw_text(status, [200, 550], 30, "Black")
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [50 + CARD_BACK_CENTER[0], 145 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)
        
    
    
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric