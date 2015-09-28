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
score = 0
DECK = 0
playerhand = 0
dealerhand = 0

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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object"
        self.card = []
        
    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.card)):
            ans += str(self.card[i]) + " "
        return "Hand contains " + ans
    def add_card(self, card):
        # add a card object to a hand
        return self.card.append(card)
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        sum = 0
        acecounter = 0
        for card in self.card:
            if card.get_rank() != 'A':
                sum += VALUES[card.get_rank()]
            else:
                sum += VALUES[card.get_rank()]
                if sum + 10 <= 21:
                    sum += 10
                else:
                    sum += 0
                acecounter += 1
        if acecounter == 2 and sum > 21:
            sum -= 10
        if acecounter == 1 and sum > 21:
            sum -= 10
        return sum
#            print 'card rank is', card.get_rank()
#            print 'card value is', VALUES[card.get_rank()]
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in self.card:
            i.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        return random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        removedcard = self.deck.pop()
        return removedcard
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " "
        return "Deck contains " + ans

#define event handlers for buttons
def deal():
    global outcome, in_play, my_deck, my_hand, your_hand, score
    my_deck = Deck()
    my_deck.shuffle()
    my_hand = Hand()
    my_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
    your_hand = Hand()
    your_hand.add_card(my_deck.deal_card())
    your_hand.add_card(my_deck.deal_card())
    outcome = 'Hit or Stand?'
#    print my_deck
#    print "MY " + str(my_hand)
#    print "YOUR " + str(your_hand)
    if in_play == True:
        score -= 1
        outcome = 'Last game counted as loss. New game?'
    
    # your code goes here
    in_play = True

def hit():
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global score, in_play, outcome
    if in_play == False:
#        print 'no hitting, current round is over'
        pass
    else:
        your_hand.add_card(my_deck.deal_card())
#        print "YOUR " + str(your_hand)
        if your_hand.get_value() > 21:
            score -= 1
            in_play = False
            outcome = 'You lose. New game?'
def stand():
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global score, in_play, outcome
    if in_play == False:
#        print 'no standing, current round is over'
        pass
    else:
        while my_hand.get_value() < 17:
            my_hand.add_card(my_deck.deal_card())
#        print "MY " + str(my_hand)
        if my_hand.get_value() > 21:
            outcome = 'You won! New game?'
        else:
            if your_hand.get_value() > my_hand.get_value():
                score += 1
                in_play = False
                outcome = 'You won! New game?'
            if my_hand.get_value() >= your_hand.get_value():
                score -= 1
                in_play = False
                outcome = 'You lose. New game?'
                
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global my_hand, your_hand, outcome, in_play, card_back, CARD_BACK_SIZE, CARD_BACK_CENTER
    canvas.draw_text('Score: ' + str(score), (300, 150), 50, 'Black')
    canvas.draw_text('Blackjack', (300, 50), 50, 'Black')
    canvas.draw_text('Dealer Hand', (50, 175), 35, 'Black')
    canvas.draw_text('Your Hand', (50, 375), 35, 'Black')
    canvas.draw_text(str(outcome), (50, 550), 35, 'Black')
        
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])
    your_hand.draw(canvas, [50, 400])
    my_hand.draw(canvas, [50, 200])
    if in_play == True:
        canvas.draw_image(card_back, (36, 48), (72, 96), (85, 249), (72, 96))
# initialization frame
frame = simplegui.create_frame("Blackjack", 650, 600)
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