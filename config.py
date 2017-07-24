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
