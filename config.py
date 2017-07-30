"""Configuration file for Chipoker"""

#Global constants

##General
HANDS = 1000            #Number of playable hands that the simulator will aim for.
HANDBUF = HANDS / 2     #Number of backup hands to account for folds.
HAND_SIZE = 13
HEADING = 'Welcome to Chipoker, the simulator for chinese poker.\n\n'
TAILING = 'It will simulate ' + str(HANDS) + ' chinese poker hands.\n'
GREETING = HEADING + TAILING

###Required defines for compatibility with entities.py
MIN_STAKE = 1
MAX_STAKE = 1
BUY_IN = 1
MAX_TABLES = 1

##Dealing

###hands/cards

CLUBS       = 0
DIAMONDS    = 1
HEARTS      = 2
SPADES      = 3
SUITS       = (CLUBS, DIAMONDS, HEARTS, SPADES)
MIN_RANK    = 2     #deuces
MAX_RANK    = 14    #aces

###ratings

#AKQJTNESXVURW
NO_HAND = 0
MAX_HI = 1535
#Three card hands from 432 to 976 starts at 1
NE = 51
FNE = 70
TV = 79
FTV = 80
TX = 83
FTX = 87
TS = 91
FTS = 101
TE = 106
FTE = 126
TN = 132
FTN = 166
JV = 176
FJV =

DN = [1, 4, 10, 20, 35, 56, 84, 120, 165]
DELTAS = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]

STRFL = 1
QUADS = 11
FULL_HOUSE = 24
FLUSH = 37
STRAIGHT = 1324
TRIPS = 1334
TWO_PAIR = 1347
PAIR = 2205
HICARD = 5065
TTRIPS = 1
TPAIR = 14
THICARD = 872
