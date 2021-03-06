#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:30:54 2021

@author: tonytang
"""

import random

suits =  ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks =  ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True


class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank+' of '+self.suit
    

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()
    
    
class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0   # start with zero value
        self.aces = 0    
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if values[card.rank] == 'Ace':
            self.aces+=1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.values -= 10
            self.aces -= 1
            
            
class Chips:
    
    def __init__(self):
        self.total = 100  
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total-=self.bet
        
        
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except :
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
    
def hit_or_stand(deck,hand):
    global playing  
    while True:
        x=input('You want hit or stand, H or S?').upper()
        if x.upper()=='H':
            hit(deck,hand)
        elif x.upper()=='S':
            print('Player stand')
            playing = False
        else:
            print('Please try again!!')
            continue
        break


def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print(dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards)
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards)
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards)
    print("Player's Hand =",player.value)


def player_busts(player,dealer,chips):
    print('Player bust!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player win!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('dealer bust!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('dealer win!')
    chips.lose_bet()
    
def push():
    print("Dealer and Player tie! It's a push.")
    


while True:
    print('Welcome to Blackjack game!')
    deck = Deck()
    deck.shuffle()
    
    player_hand=Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand=Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())    
    # Set up the Player's chips
    player_chips=Chips()
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing: 
        
        hit_or_stand(deck,player_hand)
        
        show_some(player_hand,dealer_hand)
       
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17 or dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)
            
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    print('The player have',player_chips.total)
    # Ask to play again
    play_game=input('Do you want to play again, Y or N?').upper()
    if play_game == 'Y':
        playing = True
        continue
    else:
        print('Thanks for playing')
        break
