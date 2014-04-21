from random import choice as rc
import sys


chips=100 

print "                                 "
print "                                 "
print "********************************"
print "WELCOME TO THE GAME OF BLACKJACK"
print "********************************"
print "RULES>>>>"
print "1. Players win if their hand has a greater total point value than the dealers, without going over 21"
print "2. The best possible hand is called a blackjack and it consists of an ace and any 10-point card. A winning blackjack pays 2:1"
print "3. If both the player and the dealer have a tie, including a blackjack tie, it is a 'push' and money is neither lost, nor paid "
print "4. All other winning hands pay even money, 1:1"
print "5. If either the player or the dealer exceed 21 or 'bust' the hand automatically loses."
print "6. If both the dealer and player bust, the player loses."
print "RULES>>>>"
print "********************************"
print "                                 "
print "                                 "

def compute_total(hand):
    # how many Aces in the hand
    Aces = hand.count(11)
    # to complicate things a little the ace can be 11 or 1
    # this while loop figures it out for you
    t = sum(hand)
    # you have gone over 21 but there is an ace
    if t > 21 and Aces > 0:
        while Aces > 0 and t > 21:
        # this will switch the ace from 11 to 1
            t -= 10
            for index,value in enumerate(hand):
                if value==11:
                    hand[index]=1
                    break

    Aces -= 1
    return t


def player_wins_pay_even(bet,chips_available):
    #winning hands pay even money, 1:1, 
    #This win is not a BlackJack as we have to give 2:1
    winner_paid=bet
    print "Player's bet: %i, wins: %i"%(bet,winner_paid)
    chipsleft=chips_available+winner_paid+bet
    #print "chips available: ",chipsleft
    return chipsleft


def BlackJack(bet,chips_available):
    #A player winning blackjack gets 2:1
    winner_paid=2*bet
    print "Player's bet: %i, wins: %i"%(bet,winner_paid)
    chipsleft=chips_available+winner_paid+bet
    #print "chips available: ",chipsleft
    return chipsleft



def place_bet(chip):
    #A function to ask for the player's bet     
    current_bet = raw_input("How many chips would you like to bet? ")
    if current_bet =='':
        print "Switching to minimum bet of 1 chip"
        current_bet='1' 
    elif int(current_bet) <1:
        print "Switching to minimum bet of 1 chip"
        current_bet='1'  
    elif int(current_bet) > chip:
        print "current bet is more than the available chips. Switching bet to maximum available value %i"%chips
        current_bet=str(chip)
    return current_bet
         

# a suit of cards in blackjack assume the following values
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

# there are 4 suits per deck and usually several decks
# this way one can assume the cards list to be an unlimited pool
dealer_wins = 0 # dealer win counter
player_wins = 0 # player win counter

while True:
    player = []

    #Placing a bet and chekcing if that satisfies all the conditions.
    if chips >0:
        #if dealer_wins or player_wins: print_message()
        print "*****************************"
        print "chips available for betting: ",chips
        print "*****************************"
        chips_this_hand=place_bet(chips)
        chips=chips-int(chips_this_hand)
        #print "chips left after your bet: ",chips
    else: 
        print "********************************"
        print "Oops! You ran out of chips"
        print "********************************"
        hs = raw_input("Would you like to buy another 100 chips? (y or n): ").lower()
        if 'y' in hs:
            chips =100
            print "Great! Lets continue playing"
            print "*****************************"
            print "chips available for betting: ",chips
            print "*****************************"
            chips_this_hand=place_bet(chips)
            chips=chips-int(chips_this_hand)
            #print "chips left after your bet: ",chips

        else:           
            print "********************************************"
            print "THANK YOU FOR PLAYING THE GAME OF BLACKJACK"
            print "********************************************"
     
            sys.exit("Thanks for playing BlackJack")



    # draw 2 cards for the player to start
    player.append(rc(cards))
    player.append(rc(cards))
    pbust = False # player busted flag
    cbust = False # computer busted flag
    player_BJack = False


    while True:
        # loop for the player's play ...
        total_player = compute_total(player)
        print "The player has these cards %s with a total value of %d" % (player, total_player)
        if total_player > 21:
            print "********************************************"
            print "--> The player is busted!"
            print "********************************************"
            pbust = True
            break
        elif total_player == 21 and len(player)==2 :
            print "********************************************"
            print "\a BLACKJACK!!!"
            print "********************************************"
            player_BJack = True
            break

        else:
            hitstand = raw_input("Hit or Stand/Done (h or s): ").lower()
            if 'h' in hitstand:
                player.append(rc(cards))
            else:
                break

    while True:
        # loop for the dealer's play ...
        comp = []
        comp.append(rc(cards))
        comp.append(rc(cards))
        # dealer stands at 17 or greater 
        while True:
            total_dealer = compute_total(comp)
            if total_dealer < 17:
                comp.append(rc(cards))
            else:
                break
        print "the dealer has %s for a total of %d" % (comp, total_dealer)

        # now figure out who won ...
        if total_dealer > 21:
            print "********************************************"
            print "--> The dealer is busted!"
            print "********************************************"
            cbust = True
            if pbust == False:
                player_wins += 1
                if player_BJack:
                    chips=BlackJack(int(chips_this_hand),chips)
                else:    
                    chips=player_wins_pay_even(int(chips_this_hand),chips)

        elif total_dealer > total_player:
            print "********************************************"
            print "The dealer wins!"
            print "********************************************"
            dealer_wins += 1
        elif total_dealer == total_player:
            print "********************************************"
            print "It's a PUSH!"
            print "********************************************"
            chips=chips+int(chips_this_hand)

        elif total_player > total_dealer:
            if pbust == False:
                print "********************************************"
                print "The player wins!"
                print "********************************************"
                if player_BJack:
                    chips=BlackJack(int(chips_this_hand),chips)
                else:    
                    chips=player_wins_pay_even(int(chips_this_hand),chips)

                player_wins += 1
            elif cbust == False:
                print "********************************************"
                print "The dealer wins!"
                print "********************************************"
                dealer_wins += 1
        break
    print "                                                "
    print "************************************************"
    print "Wins, player = %d dealer = %d chips left = %d" % (player_wins, dealer_wins, chips)
    print "************************************************"
    print "                                                "
    print "                                                "
    exit = raw_input("Press Enter (q to quit): ").lower()
    if 'q' in exit:
        break
    print
print
print "********************************************"
print "Thanks for playing blackjack!"
print "********************************************"
