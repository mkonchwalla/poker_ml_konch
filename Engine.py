"""This is just a script i am using to append a log that i can use to keep track of the changes, only use with hydrogen in atom
This does not run in the regular python terminal

from datetime import datetime

outfile=open("/Users/Mohammed/Desktop/Python/Poker_python3/Engine_log.txt","a")

text= ''':

Showing anmol the code

'''

outfile.write("\nNew log entry - Date and time is " + str(datetime.now()) +  text + "\n\n\n")
outfile.close()

"""

import sys
import random
import Evaluator
import itertools


class Deck(object):

    standard_deck= []
    for number in "2 3 4 5 6 7 8 9 T J Q K A"[::-1].split():
        for suit in "c d h s".split():
            standard_deck.append(str(number)+str(suit))

    def __init__(self):
        #if you want to add customisation to the deck, add it here
        self.deck=Deck.standard_deck[:]
        random.shuffle(self.deck)

    def remove_cards(self,hand): #remove cards from deck
        for card in hand:
            self.deck.remove(card)

    def reset(self):
        self.deck= Deck.standard_deck[:] # Why can i not use Deck.standard deck instead. Why does when i use this command, i change Deck.standard_deck

    def select_community(self,number): #number is the number of cards to come
        return random.sample(self.deck,number)

    def shuffle(self):
        random.shuffle(self.deck)

class Player(object):

    total_number_of_players = 0

    def __init__(self,name,position,stack=200,hand=[]): # add position later
        self.hand=hand
        self.stack= stack
        self.name=name
        if position in ["Button","Big blind"]:
            self.position=position
        else:
            raise (ValueError,"Invalid entry")
        Player.total_number_of_players+=1

    def blind(self,bet):
            self.stack-= bet
            Engine.pot+=bet
            Engine.current_bet=bet

    def call(self):
        self.stack-= Engine.current_bet
        Engine.pot+= Engine.current_bet
        print("The %s has called %.2f \n " % (self.position,Engine.current_bet))
        Engine.current_bet=0
        Engine.players_to_act-=1
        Engine.switch_action()

    def bet(self,bet):
        self.stack-= bet
        Engine.pot+=bet
        Engine.current_bet = bet - Engine.current_bet
        Engine.players_to_act = Player.total_number_of_players - 1
        print("The "+ str(self.position)+ " has bet " + str(Engine.current_bet)+ ". \n ")
        Engine.switch_action()

    def fold(self):
        players=[Engine.player_1,Engine.player_2]
        Engine.loser = players.pop(players.index(self))
        Engine.winner = players[0]
        Engine.winner.stack+=Engine.pot
        Engine.new_hand()

    def all_in(self):
        print( "%s has gone all in!!! " % Engine.action.name)
        players=[Engine.player_1,Engine.player_2]
        players.remove(self)
        Engine.not_me = players[0]

        if self.stack > Engine.not_me.stack:
            self.bet(min(Engine.player_1.stack , Engine.player_2.stack)+Engine.current_bet) # I think this should cover the larger stack bet issue
        else:
            self.bet(min(Engine.player_1.stack , Engine.player_2.stack))

    def reset(self):
        self.hand=[]

    def check(self):
        if float(Engine.current_bet) == 0.:
            Engine.players_to_act-=1
            Engine.switch_action()
            print( "The %s has checked \n " % self.position)

        else:
            print( "The current bet is not zero")

    def calc_equity(self,N=1000,range="full_deck"):

        hands_iterated_through = 0
        iterations=0
        enemy_count=0
        me_wins=0
        total_wins=0
        ties=0
        deck=Engine.deck.deck[:] #In this current state, we are going to have to recreate the deck as we do not know the other persons cards, Do it so that we add the opponents cards or we just remove ours/the boards
        #Method 1
        players=[Engine.player_1,Engine.player_2]
        players.remove(self)
        Engine.not_me = players[0]
        deck+= Engine.not_me.hand
        if range=="full_deck":
            range=itertools.combinations(deck,2)

        for enemy in range:
            iteration_deck=deck[:]
            for card in enemy:
                iteration_deck.remove(card)
            iterations=0
            while iterations<1000:
                hands_iterated_through+=1
                iterations+=1
                temp_community=random.sample(iteration_deck,5-len(Engine.community_cards))
                me_rank=0

                for hand in itertools.combinations(temp_community+self.hand+Engine.community_cards,5):
                    if Evaluator.evaluator(hand)[1] > me_rank:
                        me_hand,me_rank = Evaluator.evaluator(hand)
                not_me_rank=0
                for hand in itertools.combinations(temp_community+list(enemy)+Engine.community_cards,5):
                    if Evaluator.evaluator(hand)[1] > not_me_rank:
                        not_me_hand,not_me_rank = Evaluator.evaluator(hand)

                if me_rank>not_me_rank:
                    me_wins+=1
                elif not_me_rank>me_rank:
                    not_me_rank+=1
                elif me_rank==not_me_rank:
                    ties+=1

        print(me_wins/hands_iterated_through)




        #Method 2
        # standard_deck= [] #Testing alternative methods
        # for number in "2 3 4 5 6 7 8 9 T J Q K A"[::-1].split():
        #     for suit in "c d h s".split():
        #         standard_deck.append(str(number)+str(suit))
        #
        # community_cards=Engine.community_cards[:]
        # for card in community_cards+self.hand:
        #     standard_deck.remove(card)





class Engine(object):

    @classmethod
    def __init__(cls):
        cls.player_1=Player("Sindre","Button",stack=200)
        cls.player_2=Player("Ryan","Big blind",stack=200)
        cls.total_number_of_players = Player.total_number_of_players
        cls.button=cls.player_1
        cls.big_blind=cls.player_2
        cls.no_of_hands=0
        cls.deck=Deck()
        cls.pot=0.
        cls.community_cards=[]

    @staticmethod
    def new_hand():
        print( "\n \n \n \n \n ")
        Engine.pot=0.
        Engine.community_cards=[]
        Engine.deck.reset()
        Engine.deck.shuffle()
        Engine.big_blind.reset()
        Engine.button.reset()
        Engine.no_of_hands+=1
        Engine.current_bet=0.

        if Engine.no_of_hands%2==0: #Alternates position
            Engine.button= Engine.player_1
            Engine.player_1.position="Button"
            Engine.big_blind= Engine.player_2
            Engine.player_2.position = "Big blind"
        else:
            Engine.button=Engine.player_2
            Engine.big_blind=Engine.player_1
            Engine.player_2.position= "Button"
            Engine.player_1.position = "Big blind"

        if Engine.player_1.stack<=0:
            print(Engine.player_2.name + " wins")
            sys.exit(0)
        elif Engine.player_2.stack<=0:
            print( Engine.player_1.name + " wins")
            sys.exit(0)
        Engine.preflop()

    @classmethod
    def actions(cls):
        while cls.players_to_act!=0:

            inpt=input("Action is on  "+str(cls.action.name) +" in the "+ str(cls.action.position)+" and has hand "+" ".join(cls.action.hand)+ ". The pot is "+str(Engine.pot)+ " and the current bet is " + str(Engine.current_bet)+".  \n >").strip()
            if inpt=='call':
                if Engine.action.stack<=0:  print("%s has gone all in!!! " % Engine.action.name)()
                cls.action.call()

            elif inpt=='bet':
                while True:
                    if Engine.current_bet>=cls.action.stack:
                        print("All in to call, bet is disabled")
                        break

                    amount=input("Amount?  ")
                    try :
                        amount = float(amount)
                        if amount > 0 and amount >= cls.current_bet+1 and amount <= min(cls.player_1.stack,cls.player_2.stack)+Engine.current_bet:
                            # if amount == min(cls.player_1.stack,cls.player_2.stack)+Engine.current_bet:
                            #     print("%s has gone all in!!! " % Engine.action.name)
                            cls.action.bet(amount)
                            break
                        else:
                            print("Invalid amount - The minimum bet is %.2f  and the max bet is %.2f" % (cls.current_bet+1,min(cls.player_1.stack,cls.player_2.stack)+Engine.current_bet))

                    except:
                        print( "Invalid amount")
                        break

            elif inpt=="fold":
                cls.action.fold()
                break

            elif inpt == "pot":
                print( Engine.pot)

            elif inpt == "stack":
                print( cls.action.stack)

            elif inpt == "hand":
                print(cls.action.hand)

            elif inpt == "all":
                if Engine.current_bet>=cls.action.stack:
                    print("All in to call, All in is disabled")
                else:
                    cls.action.all_in()

            elif inpt == "all in":
                if Engine.current_bet>=cls.action.stack:
                    print("All in to call, All in is disabled")
                else:
                    cls.action.all_in()
            elif inpt=="check":
                cls.action.check()

            elif inpt=="quit":
                sys.exit(0)

            elif inpt == "options":
                print( "Options are: " + "call, bet, fold , pot , stack , hand , all , all in , check, quit, equity")

            elif inpt=="equity":
                cls.action.calc_equity()
            elif inpt=="community":
                print(cls.community_cards)

            else:
                print( "Invalid Entry")

    @classmethod
    def preflop(cls):

        print( "The big blind, %s ,has %.2f and the button, %s , has %.2f " %(cls.big_blind.name,cls.big_blind.stack,cls.button.name,cls.button.stack) )
        cls.street= "pre flop"
        cls.big_blind.blind(1)

        print( "Blinds posted\n")

        for i in range(2):
            cls.big_blind.hand.append(cls.deck.deck.pop(0))
            cls.button.hand.append(cls.deck.deck.pop(0))
        print( "Hands are dealt\n")

        print( "The big blind, %s ,has %.2f and has hand %s" % (cls.big_blind.name,cls.big_blind.stack," ".join(cls.big_blind.hand)) )
        print( "The button , %s , has %.2f and has hand %s" % (cls.button.name,cls.button.stack," ".join(cls.button.hand)) )

        Engine.players_to_act = Player.total_number_of_players

        Engine.action=cls.button
        cls.actions()
        cls.flop()


    @classmethod
    def switch_action(cls):

        if cls.action.position == cls.big_blind.position:
            cls.action = cls.button

        elif cls.action.position == cls.button.position:
            cls.action = cls.big_blind

    @classmethod
    def flop(cls):
        for i in range(3):
            cls.community_cards.append(cls.deck.deck.pop(0))
        print( cls.community_cards)
        print( "\n")

        Engine.players_to_act = Player.total_number_of_players
        Engine.action=cls.big_blind

        if cls.big_blind.stack>0 and cls.button.stack>0:
            cls.actions()

        cls.turn()

    @classmethod
    def turn(cls):

        cls.community_cards.append(cls.deck.deck.pop(0))
        print( cls.community_cards )
        print( "\n")
        Engine.players_to_act = Player.total_number_of_players

        Engine.action=cls.big_blind

        if cls.big_blind.stack>0 and cls.button.stack>0:
            cls.actions()

        cls.river()

    @classmethod
    def river(cls):
        cls.community_cards.append(cls.deck.deck.pop(0))
        print( cls.community_cards ) ; print( "\n" )
        Engine.players_to_act = Player.total_number_of_players

        Engine.action=cls.big_blind

        if cls.big_blind.stack>0 and cls.button.stack>0:
            cls.actions()

        cls.showdown()


    @classmethod
    def showdown(cls):
        bb_rank=0
        for hand in itertools.combinations(cls.big_blind.hand+cls.community_cards,5):
            if Evaluator.evaluator(hand)[1] > bb_rank:
                bb_hand,bb_rank = Evaluator.evaluator(hand)
        but_rank=0
        for hand in itertools.combinations(cls.button.hand+cls.community_cards,5):
            if Evaluator.evaluator(hand)[1] > but_rank:
                but_hand,but_rank = Evaluator.evaluator(hand)

        if but_rank>bb_rank:
            print( "%s in the button wins with %s over %s" % (Engine.button.name ,but_hand , bb_hand) )
            Engine.winner=Engine.button
            Engine.winner.stack+=Engine.pot

        if but_rank<bb_rank:
            print( "%s in the big blind wins with %s over %s" % ( Engine.big_blind.name ,bb_hand , but_hand) )
            Engine.winner=Engine.big_blind
            Engine.winner.stack+=Engine.pot

        if bb_rank==but_rank:
            print( "Split pot: %s" %bb_hand )
            Engine.button.stack+= Engine.pot / 2.
            Engine.big_blind.stack+= Engine.pot / 2.
        cls.new_hand()
    #pre - flop

eng=Engine()
eng.new_hand()
