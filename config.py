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

###sorting

SUITED = 0
VALUED = 1

#MULTI contains trips. PAIR contains at least one pair.
#NEXTPAIR contains two pair, with the first already processed.
#NO contains no pairs.
#SEQ means that it exists, but is not yet a candidate.
#CAN means it's a an unprocessed candidate.
#PRO means that it has been processed.
MULTISEQ = 0
MULTICAN = 1
MULTIPRO = 2
PAIRSEQ = 3
PAIRCAN = 4
PAIRPRO = 5
NEXTPAIRSEQ = 6
NEXTPAIRCAN = 7
NEXTPAIRPRO = 8
NOSEQ = 9
SINGLES = [MULTIPRO, PAIRPRO, NEXTPAIRPRO, NOSEQ]

##ratings

###5 cards

A_HI = 1573
K_HI = 1012
Q_HI = 627
J_HI = 372
T_HI = 210
N_HI = 112
E_HI = 56
S_HI = 26
X_HI = 11
V_HI = 4
F_HI = 1
R_HI = 0
W_HI = 0
DELALL_HI = [A_HI, K_HI, Q_HI, J_HI, T_HI, N_HI, E_HI]
ALL_HI = [W_HI, R_HI, F_HI, V_HI, X_HI, S_HI, E_HI, N_HI, T_HI, J_HI, Q_HI, K_HI, A_HI]

###4 cards

FK_HI = 561
FQ_HI = 385
FJ_HI = 255
FT_HI = 162
FN_HI = 98
FE_HI = 56
FS_HI = 30
FX_HI = 15
FV_HI = 7
FF_HI = 3
FR_HI = 1
FW_HI = 0
FALL_HI = [FW_HI, FR_HI, FF_HI, FV_HI, FX_HI, FS_HI, FE_HI, FN_HI, FT_HI, FJ_HI, FQ_HI, FK_HI]

###3 cards

RQ_HI = 165
RJ_HI = 120
RT_HI = 84
RN_HI = 56
RE_HI = 35
RS_HI = 20
RX_HI = 10
RV_HI = 4
RF_HI = 1
RR_HI = 0
RW_HI = 0
RALL_HI = [RW_HI, RR_HI, RF_HI, RV_HI, RX_HI, RS_HI, RE_HI, RN_HI, RT_HI, RJ_HI, RQ_HI]

###2 cards

WJ_HI = 45
WT_HI = 36
WN_HI = 28
WE_HI = 21
WS_HI = 15
WX_HI = 10
WV_HI = 6
WF_HI = 3
WR_HI = 1
WW_HI = 0
WALL_HI = [WW_HI, WR_HI, WF_HI, WV_HI, WX_HI, WS_HI, WE_HI, WN_HI, WT_HI, WJ_HI]

TOT_HI = [ALL_HI, FALL_HI, RALL_HI, WALL_HI]

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
FJV = 0

DN = [1, 4, 10, 20, 35, 56, 84, 120, 165]
DELTAS = [0, 0, 0, 0, 1, 3, 6, 10, 15, 21, 28, 36, 45]
TDELTAS = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

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

##Error messages

ERR_ERARG = ' Report _enoughRemaining error.\n'
ERR_AA = 'Illegal base for the hand setting procedure. 1st hicard rank too high.\n'
ERR_AB = 'Illegal base for the hand setting procedure. 2nd hicard rank (trips) is too high.\n'
ERR_A = 'Illegal base for the hand setting procedure. 2nd hicard rank is too high for all possible hands.\n'
ERR_HI = 'Illegal base (hicard) for the hand setting procedure. '   #Should always be concatenated by one of B-D (or equivalent)
ERR_B = 'Trips should be eliminated from hand with less than 13 cards.\n'
ERR_C = 'Two pairs should be eliminated from hand with less than 13 cards.\n'
ERR_D = 'Pairs should be eliminated from hand with less than 8 cards.\n'
