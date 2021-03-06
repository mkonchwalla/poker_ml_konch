import numpy
import operator
from datetime import datetime
import itertools
from functools import reduce
from pprint import *

startTime = datetime.now()

def prod(iterable):
    return reduce(operator.mul, iterable)



def strength_of_hand(hand): # This was the intiial evaluator and we are using to generate table 3. This takes too long to use for many many iterations. Its a shit function so dont dwell on it too much
    position = {"A":0,"K" :1 , "Q" : 2  , "J":3, "T":4}
    position.update({str(i) : 14-i for i in range(2,10)[::-1]})

    counter={} # counts number of time cards will appear
    for card in hand:
        counter[card[0]] = counter.setdefault(card[0],0)+1

    strength=[0]* 9 #This will keep if the hand is present or not but im pretty sure i can make this redundant
    rankings={} #

    #High card
    high_card= sorted(hand, key= lambda x: position[x[0]])[:7] #Takes 5 highest cards, if its a pair it doesnt matter in the end
    high_card=[high_card[i][0] for i in range(5)]
    rankings["High card"]=(high_card,"High card: " + high_card[0] + " High with " + " ".join(high_card[1:])+" Kicker")
    strength[0]=1

    # Pairs and trips
    for k,v in sorted(counter.items(), key= lambda x: position[x[0]]):

        if v==2 and strength[1]==0:  # The strength thing prevents the thing looping over pairs as the list is sorted into descending order
            pair = k
            strength[1]=1
            card_numbers=sorted(counter.keys(), key= lambda x: position[x[0]]) ; card_numbers.remove(pair) #Gets ordered list of unique cards and removes the pair
            rankings["One pair"]=([pair]*2 + card_numbers[:3] , "One pair: "+ pair+ "\'s  with " + " ".join(card_numbers[:3])+ " Kicker") # we are generating the best 5 card hand
            continue # Because i didnt use elif and i cba to thing of how using elif affects everything

        if v==2 and strength[1:3]==[1,0]:
            pair_2 = k
            strength[2]=1
            card_numbers=sorted(counter.keys(), key= lambda x: position[x[0]]) ; card_numbers.remove(pair) ; card_numbers.remove(pair_2)
            rankings["Two pair"] = ([pair]*2 + [pair_2]*2 + [card_numbers[0]] , "Two pair: "+pair+"\'s and "+ pair_2 + "\'s with " + card_numbers[0]+" Kicker")


        if v==3 and strength[3]==0:
            trips= k
            strength[3]=1
            card_numbers=sorted(counter.keys(), key= lambda x: position[x[0]]) ; card_numbers.remove(trips)
            rankings["Three of a kind"] =  ([trips]*3 + card_numbers[:2] , "Three of a kind: "+trips + "\'s with " + " ".join(card_numbers[:2]) +" Kicker")

        if v==4:
            quads=k # will add to the list after full house
            strength[7]=1

    #Straight - organises the cards and see's if the 5 card string is in the ordered list-  best solution - very happy
    order="A23456789TJQKA"[::-1]
    straight="".join(sorted(counter, key= lambda x: position[x]))
    for i in range(len(straight)-4):
        if straight[i:i+5] in order:
            straight=straight[i:i+5]
            strength[4]=1
            rankings["Straight"]=(list(straight) , "Straight: "+straight[0]+" High")#Converts list into separted string and reverse order so highest is first
            break  #The break is now s.t it breaks as soon as it finds a straight and it works in descending order


    #Flush
    suit_count={} #Generates a dict with the suit count
    for card in hand:
        suit_count[card[1]] = suit_count.setdefault(card[1], 0)+1

    hand=sorted(hand, key = lambda x: position[x[0]], reverse= True) #Organises the original seven list into an organised list so we get increasing card numbers
    for suit,count in suit_count.items(): # This loop adds the ones that are in a flushing suit
        if count>=5:
            strength[5]=1
            flush=[]
            for card in hand:
                if card[1]==suit:
                    flush.append(card[0])
            flush=flush[-5:] ; flush.reverse() #Similar to straight so that the highest card in the flush is first

            rankings["Flush"] =(flush ,"Flush: " + flush[0]+" High Flush with " +  " ".join(flush)[1:] + " Kicker")

    #Full house
    if strength[1]+strength[3]==2:
        strength[6]=1
        rankings["Full house" ]= ([trips]*3 + [pair]*2 , "Full house: "+trips+"'s over "+pair+"'s" )


    #Quads
    if strength[7]==1:
        card_numbers=sorted(counter.keys(), key= lambda x: position[x[0]]) ; card_numbers.remove(quads)
        rankings["Four of a kind"]=([quads]*4 + [card_numbers[0]],"Four of a kind: "+ quads + "\'s with " + card_numbers[0] + " Kicker")


    # Straight flush
    if strength[4:6]==[1,1] and "".join(flush) == straight: #Potential bug here where it displays straight flush when not ie with AKQJ s and 10 c but with a spade in the hand
        strength[8]=1
        if flush[0]=="A":
            rankings["Royal flush"] =(flush,"Royal Flush")

        rankings["Straight flush"] =(flush,"Straight Flush to the "+ flush[0])


    for ranking in "Royal flush,Straight flush,Four of a kind,Full house,Flush,Straight,Three of a kind,Two pair,One pair,High card".split(","):
        if ranking in rankings:
            return [ranking] + list(rankings[ranking])


deck= []
for number in "2 3 4 5 6 7 8 9 T J Q K A"[::-1].split():
    for suit in "c d h s".split():
        deck.append(str(number)+str(suit))

print("Generating all 7 card combos")

seven_card_combos=itertools.combinations(deck,7)


table_1= dict(zip(deck[::-1],range(52)))
table_2 = dict(zip(range(13),[2,3,5,7,11,13,17,19,23,29,31,39,41]))

table_3_values={}

print("Importing table 3")

infile=open("table_3.txt","r")
for line in infile:
    l=eval(line) #When incorparating into the engine, we will use classes instead of global variables
    table_3_values[l[1][2]]= l[1][3]
infile.close()




print("Imported table 3")

flush_list={}

table_4={}

iters=0

time_iters = datetime.now()

print("Creating table 4 - please wait takes around 15 minutes. " )

for hand in seven_card_combos:
    iters+=1
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

    if iters%1000000==0:
        print("%s Iterations completed. %.2f%% done.  Time elapsed: %s" %(iters,100*iters/133784560,datetime.now()-time_iters))


    if (prod(value),flush) not in table_4:
        table_4[(prod(value),flush)] = strength_of_hand(hand)+[table_3_values[strength_of_hand(hand)[2]]]




print("Table 4 created")

print("All Hands evaluated - Time elasped: %s" % (datetime.now() - startTime))


table_4=table_4.items()

print("Creating file...")

file=open("table_4.txt","w")
for line in table_4:
    file.write(str(line) + "\n")
file.close()


print("Done - File created")


#Check the case if there is
