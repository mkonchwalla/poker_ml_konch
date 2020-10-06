# Poker Project -Python 3

EDIT: Until further notice, this project is going to be delayed due to the difficulty behind effectively implementing Deep Reinforcement nerual networks. In the mean time, im covering other projects and will return to this after completing more ML projects. The bot is functioning. It works primarily by using standard GTO ranges preflop and uses Bayesian Inference to adjust the presumed hand ranges of its opponents. On the Flop, Turn and River, it computes E.V of each action and takes the most appropriate line. This means the bot is quite exploitable post flop as ranges arent necessarily balanced. I have decided not to post the code for the bot on github as botting is frowned upon in the poker community. 

The poker hand evaluator is the fastest poker hand evaluator in Python on GitHub. 

5 card:
Deuces evaluates 230K hands a second and my evaluator runs just shy of 420K hands a second for 5 card hand analysis. 

7 card: 
Deuces evaluates 15220 hands a second and my evaluator runs at 250K hands a second which is significantly faster than Deuces 

This section below was just for my friends who were supposed to help me with the project initially: 
-----------------------------------------------------------------------------------------------------------------------
In order to run the file:

please run the Engine file Python Poker Project

So welcome to the python poker project this is the initial plan and I hope it works well if you know anyone potentially interested in this let me know.

Firstly you should know the rules of poker and how to play. Here is a link on how to play the game. https://www.pokerstarsschool.com/article/Poker-Basics-04-How-to-Play-No-Limit-Texas-Hold-em

Also, if you don’t understand a word I use here, check the meaning here. It has all of the terminology I will use and a bunch of extra stuff . Use only when needed https://www.pokerstars.uk/poker/terms/ I have tried to italic them when I can

Now I have been looking online and there are very few modules that are relevant to poker. The best is probably the deuces module and even that is probably going to be the best option. However, we could attempt to create our own algorithm in order to do it.

We are focusing on head up texas hold’em no limit which means 1v1 and bet sizes are only restricted to the size of your stack (money you are playing with). Plan ( Work in progress)

The current plan is to create a bot of some sorts that can essentially find an optimal and profitable situation to any situation that it is dealt with. The thing about this game is Expected value of an action. The 3 actions are Call, Bet, Fold. And they all have their formulas for expected values

Fold- When it is your turn to act and you throw your cards away ending the hand. E.V = 0 always as you are no longer losing money at that given stage.

Call- When you are facing a bet and you decide to match the bet and proceed to the next street. The expected value formula is …

Bet – The additional amount you are putting into the pot (If it’s a first raise/2bet/ atleast 2x the amount ). There are a few formulas for Bet depending on the action he takes so I still need to combine them.

So we want to maximize each of the values by figuring out what is profitable each time.

So the primary parameters we have are going to be: percentage of hands to bet, call or fold with and they should all add up to 1. So we can deduce a function of the E.V of any situation

We want to maximize that at any given stage. The problem with that is that we need to work backwards so I’m thinking Monte Carlo method (20,000 iterations) to estimate it. Randomly generate the cards and calculate the river E.V. then the Turn E.V. Until we can get the ML part to catch up and improve. Could we use a one of the polynomial approximations from Computational methods in order to approximate the function and then calculate the gradient to approximate E.V of a call/ bet? Here, we could also apply the ideal value to pick a raise size, and keep it consistent with bluff sizes, im thinking of having 1/3 pot , ½ pot , 2/3 – ¾ pot ., pot , 3/2 pot , 2 pot, All in and each of those being parameters instead of % bet. Would make the function a lot more complicated?

Once we have the ideal percentages, we can calculate the number of hands in order to make the play with using the evaluator to work out the best hands. We can do it such that we have hands that 1) have the best equity and 2) deny the best equity. I think its best to combine both of those which its why I think its important to separate the bets into 2 forms. Bet bluff and bet value which combined together can have it such that %bluff + %value = % bet. The sizing in any given spot will try to be the best size s.t we can keep our range fully hidden and disguised. It should hopefully be consistent to protect our range which is why I think depending on the board texture we can manually programme different sizes.

There are alot of issues with the method above in terms of the calculations which is why I would like to go over this in person

Engine

This is just a standard poker engine that runs the game.

Some classes/Functions that need to be created are • Deck • Ranges • Card? • Player • Bet • Call • Fold And the function that calculates the winner aka the evaluator. Evaluator

This is the part of the project where we evaluate hand strength and use that to see who wins. Essential in calculating equities.

The current ideas I have in mind for the evaluator are:

Using vector – generate a 52 digit long binary number or 52 dimensional vector that represents a 5 combo hand and do it s.t we evaluate each number to be …

Look up table – have a sorted table so we can do a binary search log(n), possibly combine binary with it. 52 C 7 = 133,784,560 , 52 C 5 = 2,598,960 but 7C5 is 21 so, 21 combination ( Seems like the best option)

Prime numbers – 13 or 52 prime numbers, using the property that each number has a unique prime factorization so each hand corresponds to a unique product of primes which can only be made by multiplying 5 primes together, and using a table or a series of functions to set it up to a score.

Modulo method- Combine the 13 prime numbers method above with modulo so we can track the flushes .

Standard check – this is the standard method of approach but takes way too long to do. It checks to see if each thing is a pair. Already programmed from before. I am going to have to check the complexity of each of these methods but it shouldn’t take too long.

Using matrices – might be a method involving the trace or other shit.

The modulo method looks the most promising and it is what im going to do.

Whilst the sections are highly related: we can have another team working on the main player algorithm aka the calculations on the best strategy to play.

Main player algorithm

So I’m thinking of giving the bot a few general options.

The first is if it thinks its winning or its behind. If its ahead, it will either bet/ check for value. If its behind, then it will either bet/ fold for value. Let’s add some notation into this.

f – is the percentage of folds c – is the percentage of calls b – is the percentage of bets bvalue or bv– is the percentage of value bets bbluff or bb – is the percentage of bluffs

f + c + b = 1 bvalue + bbluff = b

Total E.V = F(c,b) = c* E.V of a call + b * E.V of a bet + 0 * (1 - b - c) [This is a fold so its zero]

Here are some research papers: (haven’t read them myself, will do eventually)

• http://www.cs.virginia.edu/~evans/poker/wp-content/uploads/2011/02/opponent_modeling_in_poker_billings.pdf • https://www.cs.auckland.ac.nz/~ian/papers/AIJournal.pdf
