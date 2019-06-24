#Currently evaluates at 204,000 hands per seconds
from datetime import datetime
import time
import itertools
import operator
import os.path
import numpy as np
from functools import reduce


if  __name__ == "Evaluator":
    print("Importing Evaluator")

if not os.path.isfile("table_3.txt"): #Checks if the file exists
    print("File \" table_4.txt\" not detected")
    import generate_table_4

else:
    if __name__=="__main__":
        if "y" in input("Do you wish to overwrite and generate a new file?   "):
            print( "Overwriting...")
            import generate_table_4

def prod(iterable):
    return reduce(operator.mul, iterable)

deck= []
for number in "2 3 4 5 6 7 8 9 T J Q K A"[::-1].split():
    for suit in "c d h s".split():
        deck.append(str(number)+str(suit))


table_1= dict(zip(deck[::-1],range(52)))
table_2 = dict(zip(range(13),[2,3,5,7,11,13,17,19,23,29,31,39,41]))
table_4={}

infile=open("table_4.txt","r")

for line in infile:
    l=eval(line) #When incorparating into the engine, we will use classes instead of global variables
    table_4[l[0]]=tuple(l[1][2:4])

def evaluator(hand): #Hand is going to be in the form of a list with 5 card e.g. [Ac,Ad,Ah,Ts,2c]
    global table_4 #When incorparating into the engine, we will use classes instead of global variables
    value=[]
    suits=[]
    for card in hand:
        #hand[hand.index(card)]=table_1[card]  #calculates product
        value.append(table_2[table_1[card]//4])
        suits.append(table_1[card] % 4)

    if max([suits.count(i)>4 for i in set(suits)]): #Calculates whether we have a flush or not
        flush="y"
    else:
        flush="n"

    return table_4[(prod(value),flush)]

if __name__=="__main__":
    startTime = time.time()
    print( "Evaluating hands")
    list_temp = list(itertools.combinations(deck,7))[:2600000]
    for hand in list_temp:
        print(evaluator(hand))
    print(  "Evaluated all 2.6 million combinations in %.6f seconds" % (time.time() - startTime))
