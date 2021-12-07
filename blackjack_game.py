# Python, text-based, object oriented Blackjack game by Aaron Baumgartner 12/06/2021
# Project/guidance from Pierian Data "Complete Python 3 bootcamp" on Udemy.com

import random

# set up cards
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __repr__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
                
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        return self.all_cards.pop()

# each player and the dealer will have their own hand
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + card.value
        if card.rank == 'Ace':
            self.aces = self.aces + 1
    
    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 0:
            self.value = self.value - 10
            self.aces = self.aces - 1

# the player will have chips to bet with during the game
class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total = self.total + self.bet
        
    def lose_bet(self):
        self.total = self.total - self.bet

# set up functions that will run the game 

def take_bet():
    bet = input("How much would you like to bet? ")
    return int(bet)

def hit(deck,hand):
    hand.add_card(deck.deal_one())

def hit_or_stand(deck,hand):
    global playing
    result = input("Hit(y/n)? ")
    if result.lower() == 'y':
        hit(deck,hand)
    else:
        playing = False

def show_some(player,dealer):
    print("Player cards: " + str(player.cards) + " total: " + str(player.value) + " Dealer: " + str(dealer.cards[1]))
    
def show_all(player,dealer):
    print("Player cards: " + str(player.cards) + " total: " + str(player.value) + " Dealer: " + str(dealer.cards) + " total: " + str(dealer.value))

# set up end game conditions

def player_busts(player,dealer,chips):
    if player.value > 21:
        show_all(player,dealer)
        print("Player busts, dealer wins")
        chips.lose_bet()

def player_wins(player,dealer,chips):
    if player.value > dealer.value and player.value <= 21:
        show_all(player,dealer)
        print("Player wins!")
        chips.win_bet()
        
def dealer_busts(player,dealer,chips):
    if dealer.value > 21:
        show_all(player,dealer)
        print("Dealer busts, player wins")
        chips.win_bet()
        
def dealer_wins(player,dealer,chips):
    if dealer.value >= player.value and dealer.value <= 21:
        show_all(player,dealer)
        print("Dealer wins!")
        chips.lose_bet()

# set up the game

player = Chips()
while True:
    print("Welcome to blackjack!")
    
    # Create the deck and deal out cards
    deck = Deck()
    deck.shuffle()
    playerHand = Hand()
    dealerHand = Hand()
    playerHand.add_card(deck.deal_one())
    playerHand.add_card(deck.deal_one())
    dealerHand.add_card(deck.deal_one())
    dealerHand.add_card(deck.deal_one())
    
    player.bet = take_bet()
    while player.bet > player.total:
    	print("You don't have that many chips to bet")
    	player.bet = take_bet()
    
    show_some(playerHand,dealerHand)
    
    while playing:
        hit_or_stand(deck,playerHand)
        show_some(playerHand,dealerHand)
        playerHand.adjust_for_ace()
        
        if playerHand.value > 21:
            player_busts(playerHand,dealerHand,player)
            break
            
    if playerHand.value <= 21:
        while dealerHand.value <= 17:
            hit(deck,dealerHand)
            dealerHand.adjust_for_ace()
        
        show_all(playerHand,dealerHand)
        player_wins(playerHand,dealerHand,player)
        dealer_busts(playerHand,dealerHand,player)
        dealer_wins(playerHand,dealerHand,player)
    
    print("Current chips total: " + str(player.total))
    if player.total == 0:
    	print("Looks like you are all out of chips, better luck next time")
    	break
    
    if input("Play again(y/n)? ").lower() !='y':
        break
    else:
        playing = True