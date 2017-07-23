#Other libs
from random import randint
from config import *

class Card(object):
    """A playing card. Has a suit and a value with ranges that should be defined in config.py"""

    #At a later stage, it might be convenient to be able to display symbols for suits
    #and shorter description for ranks.

    def __init__(self, suit, value):
        """Create a card with the given suit and rank. Raises a ValueError if any of the arguments are invalid."""

        #Make sure that the given parameters are valid
        if(suit in SUITS):
            self._suit = suit
        else:
            raise ValueError("suit must correspond to a member of SUITS in config.py")
        if value >= MIN_RANK and value <= MAX_RANK:
            self._value = value
        else:
            raise ValueError("value must be between MIN_RANK and MAX_RANK in config.py")

    def getSuit(self):
        """Getter for _suit"""
        return self._suit

    def getValue(self):
        """Getter for _value"""
        return self._value

    def strSuit(self):
        """Return a string corresponding to the suit of the card."""

        if self._suit == CLUBS:
            return "clubs"
        elif self._suit == DIAMONDS:
            return "diamonds"
        elif self._suit == HEARTS:
            return "hearts"
        elif self._suit == SPADES:
            return "spades"
        else:
            return "illegal suit"

    def strValue(self, context = 0):
        """Return a string corresponding to the rank of the card."""

        if(self._value == 2):
            return "deuce"
        elif(self._value == 3):
            return "trey"
        elif(self._value == 4):
            return "four"
        elif(self._value == 5):
            return "five"
        elif(self._value == 6):
            if context == 0:
                return "six"
            else:
                return "sixe" #hack to get the correct plural
        elif(self._value == 7):
            return "seven"
        elif(self._value == 8):
            return "eight"
        elif(self._value == 9):
            return "nine"
        elif(self._value == 10):
            return "ten"
        elif(self._value == 11):
            return "jack"
        elif(self._value == 12):
            return "queen"
        elif(self._value == 13):
            return "king"
        elif(self._value == 14):
            return "ace"
        else:
            return "illegal rank"

    def printCard(self):
        """Print info about the card (rank and suit)."""

        print("\t" + self.strValue() + " of " + self.strSuit())

class PokerPerson(object):
    """An adt class for persons sitting at a poker table (players and dealer)."""

    def __init(self):
        """Default initialization of the ADT."""

        print("Please don't try to initialize an object of this ADT.")

    def processHand(self, hand):
        """Default method for reading, sorting and classifying a poker hand."""

        print("Please make sure to implement a processHand method for the descendant of this ADT.")

    def sortHand(self, hand, drawing = False, testMode = False):
        """Sorts the hand. Prints what hand it is. Then returns the sorted hand."""

        cards = list(hand)          #cards to be sorted/classified
        foot = 0                    #Index of the first unprocessed card
        head = len(cards) - 1       #Index of the last unprocessed card
        counter = 0                 #To count the number of cards having the same rank as the card at foot
        pattern = HICARD            #Look in config.py for an overview of the possible patterns

        #Sort, with aces first and deuces last
        cards.sort(key = lambda card: card._value, reverse = True)

        #Check for hands containing more than one card of equal rank (pairs, trips, two pair etc.)
        #The cards will be sorted so paired cards appear before unpaired and trips before pairs (in a full house)
        while(foot <= head):
            counter = sum(c.getValue() == cards[foot].getValue() for c in cards)
            if counter == 1:
                #Move the card to the back. Move head forward, so the card will not be considered again.
                #Since all unpaired are treated this way, their order is preserved.
                cards.append(cards.pop(foot))
                head -= 1
            else:
                if counter == 4:
                    pattern = QUADS
                    foot = head + 1     #With quads at the foot, the hand is already sorted, so no need to loop again
                elif counter == 3:
                    if pattern == PAIR:
                        #A pair has already been processed. Since the trips are more interesting, the pair is moved to the end of the list
                        pattern = FULL_HOUSE
                        cards.append(cards.pop(0))
                        cards.append(cards.pop(0))
                        foot = head + 1     #With a full house, all cards have been sorted, so no need to loop again
                    else:
                        pattern = TRIPS
                        foot += counter     #The trips are in the right place. Move the foot to the first card that doesn't match their rank
                elif counter == 2:
                    if pattern == TRIPS:
                        #The trips have been processed, and the pair is therefore correctly placed
                        pattern = FULL_HOUSE
                        foot = head + 1     #With a full house, all cards have been sorted, so no need to loop again
                    elif pattern == PAIR:
                        #Since none of the pairs are moved, their order is preserved
                        pattern = TWO_PAIR
                        foot = head + 1     #With two pairs, the fifth card will always be in the correct place by now
                    else:
                        #The pair is likely to be correctly placed, so move the foot to the first card that doesn't match the rank
                        pattern = PAIR
                        foot += counter
                else:
                    #It is assumed that there are four suits and no jokers, so the count should never be outside the interval [1,4]
                    pattern = NO_HAND
                    foot = head + 1
                    print("Illegal hand")

        #If no cards were of equal rank, the hand is either a straigh flush, a flush, a straight or a hi-card hand.
        if(pattern == HICARD):
            #Order a wheel (5-high straight) correctly
            if cards[0].getValue() == 14 and cards[1].getValue() == 5:
                cards.append(cards.pop(0))
                
            #Check for straights and flushes
            pattern = self.findSequence(cards, drawing)
        elif(pattern == PAIR) and drawing:
            #Check for straight- and flush-draws
            pattern = self.findSequence(cards, drawing)

        hiDraw = None

        #If the hand contained a draw, sort it so the first card in the hand is not part of the draw
        if drawing:
            if pattern == UNPSF:
                temp = cards.pop(1)
                cards.insert(0, temp)
                pattern = PSTRFLDRAW
            elif pattern == UNPFL:
                temp = cards.pop(1)
                cards.insert(0, temp)
                pattern = PFLDRAW
            elif pattern == UNSTRFL:
                if cards[0].getValue() == 14 and cards[2].getValue() <= 5: #To rearrange wheel flush draws
                    temp = cards.pop(0)
                    cards.append(temp)
                else:
                    temp = cards.pop(-1)
                    cards.insert(0, temp)

                pattern = STRFLDRAW
            elif pattern == UNFL:
                suit = cards[0].getSuit()
                for i in range(1, len(cards)):
                    if cards[i].getSuit() != suit:
                        temp = cards.pop(i)
                        cards.insert(0, temp)
                        pattern = FLDRAW
                        break
            elif pattern == UNSTR:
                temp = cards.pop(-1)
                cards.insert(0, temp)
                pattern = STRDRAW

        #If there's a wheel flush draw, put the ace in the last position (if it's not paired)
        if pattern == PSTRFLDRAW:
            if cards[2].getValue() == 14 and cards[0].getValue() <= 5:
                temp = cards.pop(2)
                cards.append(temp)

        #If there's a broadway draw, put the small card in the first position
        if pattern == BWDRAW:
            temp = cards.pop(-1)
            cards.insert(0, temp)

        if pattern > HICARD and pattern < PAIR:
            if pattern >= PBWDRAW:
                hiDraw = cards[2]
            else:
                hiDraw = cards[1]

        #Print each card in the hand if in test mode.
        if testMode:
            for card in cards:
                card.printCard()

        self.printHandInfo(pattern, cards[0], hiDraw)
        return (cards, pattern)

    def findSequence(self, hand, drawing = False):
        """Returns the pattern found (straight, flush, straightflush or hicard). Unless drawing is False, it also looks at drawing patterns. Make sure to follow the rules given below.

        hand: The hand to be examined. It must be sorted and follow the rules given below. Look for a sortHand() method to sort the hand correctly.
        drawing: If true, look for drawing patterns. Otherwise, only consider the current value/category of the hand.

        If drawing = False, the hand must not contain any duplicate ranks (pairs, trips, quads).
        If drawing = True, the hand may contain one pair but no other duplicate ranks.
        The method does not test that the provided hand follows these rules, but the return value can not be trusted if the rules are not followed.
        
        """

        suitCount = sum(card.getSuit() == hand[0].getSuit() for card in hand) #Number of cards having the same suit as the first card
        firstRank = hand[0].getValue()
        swap = False    #Determine if a pair needs to be swapped

        #Test for straights/flushes
        if(firstRank == 5) or (firstRank - hand[4].getValue() == 4):
            if suitCount == 5:
                return STRFL
            elif firstRank != hand[1].getValue(): #To verify that the hand does not in fact contain a pair (invalidating the possibility of a straight)
                return STRAIGHT
        elif suitCount == 5:
            return FLUSH

        #Test for draws
        if drawing:
            #Test for flush draws
            if suitCount == 4:
                flushing = True
                swap = True
            elif sum(card.getSuit() == hand[1].getSuit() for card in hand) == 4:
                flushing = True
            else:
                flushing = False
            
            #If paired, test the last four cards for straight/flush draws (else test all five cards)
            if firstRank == hand[1].getValue():
                thirdRank = hand[2].getValue()
                fifthRank = hand[4].getValue()
                #Broadway?
                if fifthRank >= 10 and (firstRank == 14 or (thirdRank == 14 and firstRank >= 10)):
                    if flushing:
                        if swap:
                            return UNPSF
                        else:
                            return PSTRFLDRAW
                    else:
                        return PBWDRAW
                #Open ended?
                if(firstRank != 14 and thirdRank != 14): #Cannot be openended if it contains an ace
                    if((thirdRank - fifthRank == 2 and (firstRank == thirdRank + 1 or firstRank == fifthRank - 1))
                       or thirdRank - fifthRank == 3 and firstRank < thirdRank and firstRank > fifthRank):
                        if flushing:
                            if swap:
                                return UNPSF
                            else:
                                return PSTRFLDRAW
                        else:
                            return PSTRDRAW
                #Flush draw with or without gutshot?
                if flushing:
                    if((thirdRank == fifthRank + 2 and (firstRank == thirdRank + 2 or firstRank == fifthRank - 2)) or
                       (thirdRank == fifthRank + 3 and (firstRank == thirdRank + 1 or firstRank == fifthRank - 1)) or
                       (thirdRank == fifthRank + 4 and (firstRank < thirdRank and firstRank > fifthRank)) or
                       (thirdRank == 14 and firstRank <= 5 and hand[3].getValue() <= 5) or
                       (firstRank == 14 and thirdRank <= 5)):
                        if swap:
                            return UNPSF
                        else:
                            return PSTRFLDRAW
                    else:
                        if swap:
                            return UNPFL
                        else:
                            return PFLDRAW
                #Otherwise, the hand is assumed to be a pair (since the caller should not call this method if the hand contains quads, trips or more than one pair)
                return PAIR
            else:
                #Unpaired hand...
                fourthRank = hand[3].getValue()
                
                #Open ended?
                if hand[1].getValue() - hand[4].getValue() == 3:
                    if flushing:
                        if hand[0].getSuit() != hand[1].getSuit() and hand[0].getSuit() != hand[4].getSuit():
                            return STRFLDRAW
                        elif ((hand[4].getSuit() != hand[0].getSuit() and firstRank - hand[1].getValue() == 2) or
                              (firstRank == 14 and hand[1].getValue() == 6 and hand[1].getSuit() != hand[0].getSuit())):
                            return UNSTRFL
                        else:
                            return UNFL
                    else:
                        return STRDRAW
                if firstRank - fourthRank == 3 and firstRank < 14:
                    if flushing:
                        if hand[4].getSuit() != hand[0].getSuit() and hand[4].getSuit() != hand[3].getSuit():
                            return UNSTRFL
                        elif hand[0].getSuit() != hand[4].getSuit():
                            if fourthRank - hand[4].getValue() == 2:
                                return STRFLDRAW
                            else:
                                return FLDRAW
                        else:
                            return UNFL
                    else:
                        return UNSTR
                #Broadway? (must check open-ended first, since a hand can both be open ended and have a broadway draw)
                if firstRank == 14 and (fourthRank >= 10):
                    if flushing:
                        if hand[4].getSuit() != hand[0].getSuit() and hand[4].getSuit() != hand[3].getSuit():
                            return UNSTRFL
                        elif hand[0].getSuit() != hand[4].getSuit():
                            return FLDRAW
                        else:
                            return UNFL
                    else:
                        return BWDRAW
                #Flush draw with or without gutshot?
                if flushing:
                    if ((firstRank - fourthRank == 4 and hand[4].getSuit() != hand[0].getSuit() and hand[4].getSuit() != hand[3].getSuit()) or
                        (firstRank == 14 and hand[2].getValue() <= 5 and hand[0].getSuit() == hand[4].getSuit() and hand[1].getSuit() != hand[0].getSuit())):
                        return UNSTRFL
                    if hand[1].getValue() - hand[4].getValue() == 4 and hand[0].getSuit() != hand[1].getSuit() and hand[0].getSuit() != hand[4].getSuit():
                        return STRFLDRAW
                    #If there was no straight draw containing the same cards as the flush draw, classify this as a flush draw
                    if hand[0].getSuit() != hand[1].getSuit() and hand[0].getSuit() != hand[4].getSuit():
                        return FLDRAW
                    else:
                        return UNFL
                
        return HICARD

    def printHandInfo(self, category, firstCard, firstDraw):
        """Prints info about the hand based on its pattern/category and the most significant card."""

        msg = ""    #Message to be printed about the hand

        if category < 0:
            #Illegal value
            msg = "Illegal value for the hand category."
        elif category == HICARD:
            msg = "high card " + firstCard.strValue() + "."
        elif category == BWDRAW:
            msg = "broadway straight draw."
        elif category == STRDRAW:
            msg = firstDraw.strValue() + " high open-ender."
        elif category == FLDRAW:
            msg = firstDraw.strValue() + " high flush draw."
        elif category == STRFLDRAW:
            msg = firstDraw.strValue() + " high straight flush draw."
        elif category <= PAIR:
            msg = "a pair of " + firstCard.strValue(-1) + "s"
            if category < PAIR and firstCard.getValue() > firstDraw.getValue() and (firstCard.getValue() < 14 or firstDraw.getValue() > 5):
                hiPair = True #The expression in the parantheses are to avoid that wheel draws are considered ace-high.
            else:
                hiPair = False
                
            if category == PBWDRAW:
                msg += " with a broadway straight draw."
            elif category == PSTRDRAW:
                msg += " with a(n) "
                if hiPair:
                    msg += firstCard.strValue()
                else:
                    msg += firstDraw.strValue()
                msg += " high open-ender."
            elif category == PFLDRAW:
                msg += " with a(n) "
                if hiPair:
                    msg += firstCard.strValue()
                else:
                    msg += firstDraw.strValue()
                msg += " high flush draw."
            elif category == PSTRFLDRAW:
                msg += " with a(n) "
                if hiPair:
                    msg += firstCard.strValue()
                else:
                    msg += firstDraw.strValue()
                msg += " high straight flush draw."
            elif category == PAIR:
                msg += "."
        elif category == TWO_PAIR:
            msg = firstCard.strValue(-1) + "s up."
        elif category == TRIPS:
            msg = "trip " + firstCard.strValue(-1) + "s."
        elif category == STRAIGHT:
            msg = firstCard.strValue() + "-high straight."
        elif category == FLUSH:
            msg = firstCard.strValue() + "-high flush."
        elif category == FULL_HOUSE:
            msg = firstCard.strValue(-1) + "s full."
        elif category == QUADS:
            msg = "quad " + firstCard.strValue(-1) + "s."
        elif category == STRFL:
            msg = firstCard.strValue() + "-high straight flush."
        else:
            msg = "Unknown hand type."

        print(msg)

class Dealer(PokerPerson):
    """A poker dealer.

    _cards: A full deck of cards that should be immutable.
    _deck: An actual deck of cards that can be used(mutated).

    It seems unnecessary to actually shuffle the cards at the start of a new round, so the dealer should just
    pick (pop) a random card from the deck for each dealt card.
    Since the deck will no longer contain the cards that was drawn during the latest round, a
    resetDeck() method can be called to reassemble the deck.
    """

    def __init__(self):
        """Create a dealer with a dummy version of a deck (that can't be altered), and an actual deck."""

        #Set up a full deck that can be copied into an actual deck when starting a new hand
        #This seemed easier than collecting cards from the muck before a new deal.
        self._cards = list()
        self._initCards()

        #Initialize the actual deck
        self._deck = list()
        self.resetDeck()

    def _initCards(self):
        """Create the cards of a deck. Only planned use is for the constructor."""

        for s in SUITS:
            for v in range(MIN_RANK, MAX_RANK + 1):
                newCard = Card(s, v)
                self._cards.append(newCard)

    def resetDeck(self):
        """Reassemble the deck by making _deck a copy of _cards."""

        #Copy the dummy deck     
        self._deck = list(self._cards)

    def dealHand(self):
        """Deal a hand from the deck.

        returns a list containg the cards of the dealt hand.
"""

        return self.processHand(self.dealCards())

    def dealCards(self, n = HAND_SIZE):
        """Deal a given number of cards from the deck.

        n: Number of cards to deal.

        returns a list containing the dealt cards.
"""

        hand = list()

        for i in range(n):
            hand.append(self._deck.pop(randint(0, len(self._deck) - 1)))

        return hand

    def processHand(self, hand):
        """Sorts the hand. Prints what hand it is. Then returns the sorted hand."""

        cards = self.sortHand(hand)
        return cards[0]

    def showDown(self, players, potsize):
        """Awards the pot to the player with the best hand."""

        bestHand = self._createHand(NUTLOW)
        cmpVal = 0
        winners = list()

        for player in players:
            hand = self.processHand(player.getHand())
            cmpVal = self.cmpHands(hand, bestHand)

            if cmpVal > 0:
                winners = list()    #Remove beaten players from the list
                winners.append(player)
                bestHand = hand
            elif cmpVal == 0:
                winners.append(player)

        #print("winners: " + str(len(winners)) + "\n")
        
        winnings = potsize // len(winners)
        rest = potsize % len(winners)

        while rest != 0:
            winners[randint(0, len(winners) - 1)].chipUp(1)
            rest -= 1

        for winner in winners:
            winner.chipUp(winnings)

    def cmpHands(self, firstHand, lastHand):
        """Return 1 if the first hand is best, 0 if they're equal and -1 otherwise."""

        first = self.rateHand(firstHand)
        last = self.rateHand(lastHand)

        if first > last:
            return 1
        elif first < last:
            return -1
        else:
            for i in range(len(firstHand)):
                if firstHand[i].getValue() > lastHand[i].getValue():
                    return 1
                elif firstHand[i].getValue() < lastHand[i].getValue():
                    return -1

            return 0

    def rateHand(self, hand):
        """Returns a number telling what category the hand belongs in"""

        counter = sum(card.getValue() == hand[0].getValue() for card in hand)

        if counter == 4:
            return QUADS
        elif counter == 3:
            if hand[3].getValue() == hand[4].getValue():
                return FULL_HOUSE
            else:
                return TRIPS
        elif counter == 2:
            if hand[2].getValue() == hand[3].getValue():
                return TWO_PAIR
            else:
                return PAIR
        elif counter != 1:
            return NO_HAND
        else:
            return self.findSequence(hand)
         
    def _printCards(self):
        """Print the cards of the entire deck (for testing)"""

        for card in self._cards:
            card.printCard()

    def printDeck(self):
        """Print the cards left in the actual deck"""

        for card in self._deck:
            card.printCard()

    def _createHand(self, template):
        """Method that creates specific hands. Details omitted to avoid unauthorized use."""

        #Deal a hand.
        #The template argument should contain a list of indices corresponding to the position of the cards in a newly reset deck.
        #It is easiest to sort the list descending, since popping messes with the indices of the following elements.
        #The method provides the possibility of a backdoor/cheat, so should probably be removed if used in a game.

        cards = list()

        #Reset the deck to make sure that the intended cards are drawn
        self.resetDeck()
            
        for ind in template:
            cards.append(self._deck.pop(ind))

        #Sort the hand and display what kind of hand it is. Then return it.
        return self.processHand(cards)

class Player(PokerPerson):
    """A poker player"""

    def __init__(self, balance = MIN_STAKE * BUY_IN):
        """Setting up variables for the player."""

        self._chips = balance       #Default should be one buy-in at the smallest stakes unless something else is given
        self._cash = 0              #Cash that is not converted to chips (if moving up, the remainder of cash that cannot be used to buy new chips end up here)
        self._wager = 0             #Chips that is on the table, but is not yet in the pot
        self._type = -1             #0 = loose, 1 = regular, 2 = tight (maybe best to just include this into the strat-list)
        self._strat = list()        #To hold a list that determines the strategy of the player
        self._hand = list()
        self._sorted = False        #Should only be true if processHand() has been called since last time the player was dealt something.
        self._pattern = -1          #Category of hand held (see config.py for the range)
        self._rating = 0            #The player's rating of the hand
        self._played = 0            #Number of hands played
        self._status = MOVE_UP      #For determining if the player is seated/moving up/moving down or busto
        self._ups = 0               #Number of times the player has moved up in stakes
        self._downs = 0             #Number of times the player has moved down in stakes

    def getChips(self):
        """Return the number of chips the player has."""

        return self._chips

    def chipUp(self, amount):
        """Increases the player's chips by the given amount. A negative value will decrease the player's chips."""

        self._chips += amount   #Currently, it is assumed that the caller specifies a correct/reasonable amount.

    def takeChips(self):
        """Sets _chips to 0. Intended for use by cashiers."""

        self._chips = 0

    def getCash(self):
        """Getter for _cash"""
        return self._cash

    def setCash(self, value):
        """Setter for _cash"""
        self._cash = value

    def addCash(self, value):
        """Alternative setter for _cash. Increments it by the given value."""
        self._cash += value

    def getWager(self):
        """Getter for _wager"""
        return self._wager

    def setWager(self, value):
        """Setter for _wager"""
        self._wager = value

    def getType(self):
        """Return a string saying what type of player this is."""

        if(self._type == 0):
            return " loose "
        elif(self._type == 1):
            return "regular"
        elif(self._type == 2):
            return " tight "
        else:
            return "unknown"

    def setStrat(self, cat, strat):
        """Initilize player type and strat according to the given parameters"""

        self._type = cat
        self._strat = strat

    def getHand(self):
        """Return the player's hand"""

        return self._hand

    def setHand(self, hand):
        """Give a hand to the player. The player will then process the hand."""

        self._sorted = False
        cards = self.processHand(hand)
        if cards is not None:
            self._hand = cards
        self._played += 1   #If using this when drawing cards, this line must be made conditional

    def getRating(self):
        """Return the player's rating of the hand."""
        return self._rating

    def setRating(self, value):
        """Setter for _rating"""
        self._rating = value

    def countHand(self):
        """Setter for _played. Increments it by 1."""
        self._played += 1

    def getStatus(self):
        """Return the current status of the player."""

        return self._status

    def setStatus(self, status):
        """Set the status of the player."""

        self._status = status

    def moveUp(self):
        """Increments _ups by 1"""
        self._ups += 1

    def getUps(self):
        """Getter for _ups"""
        return self._ups

    def moveDown(self):
        """Increments _downs by 1"""
        self._downs += 1

    def getDowns(self):
        """Getter for _downs"""
        return self._downs

    def moveIn(self):
        """Bet the maximum amount on a hand. Used for testing. The finished simulator should be based on a limit structure."""

        self.chipUp(MIN_STAKE * -6)     #2 big bets predraw, 4 postdraw

    def processHand(self, hand):
        """Sorts the hand. Prints what hand it is. Updates _pattern and _sorted accordingly."""

        if self._sorted:
            return None #The hand is already sorted

        cards = self.sortHand(hand, True)

        self._pattern = cards[1]
        self._sorted = True
        return cards[0]

    def rateHand(self):
        """Give a rating to the hand based on global constants. If the categories in the config file is changed, this function needs to be changed too."""

        firstRank = self._hand[0].getValue()

        if self._pattern > FULL_HOUSE:
            self._rating = K_FULL
        elif self._pattern == FULL_HOUSE:
            if firstRank >= 13:
                self._rating = K_FULL
            elif firstRank >= 10:
                self._rating = T_FULL
            elif firstRank >= 6:
                self._rating = F_FULL
            else:
                self._rating = A_FLUSH
        elif self._pattern == FLUSH:
            if firstRank >= 14:
                self._rating = A_FLUSH
            elif firstRank >= 11:
                self._rating = J_FLUSH
            else:
                self._rating = A_STRAIGHT
        elif self._pattern == STRAIGHT:
            if firstRank >= 14:
                self._rating = A_STRAIGHT
            elif firstRank >= 10:
                self._rating = T_STRAIGHT
            else:
                self._rating = E_STRAIGHT
        elif self._pattern == TRIPS:
            if firstRank >= 14:
                self._rating == TRIP_A
            elif firstRank >= 12:
                self._rating == TRIP_Q
            elif firstRank >= 9:
                self._rating == TRIP_I
            else:
                self._rating == TRIP_B
        elif self._pattern == TWO_PAIR:
            if firstRank >= 14:
                self._rating = A_UP
            elif firstRank >= 12:
                self._rating = Q_UP
            else:
                self._rating = C_UP
        elif self._pattern == PAIR:
            if firstRank >= 14:
                self._rating = P_A
            else:
                self._rating = P_A + P_DELTA * (14 - firstRank)
        elif self._pattern >= PBWDRAW:
            pair = P_A + P_DELTA * (14 - firstRank)
            if self._pattern == PSTRFLDRAW:
                self._rating = min(pair, SFDRAW)
            elif self._pattern == PFLDRAW or self._pattern == PSTRDRAW:
                self._rating = min(pair, SEQDRAW)
            elif self._rating == PBWDRAW:
                self._rating = pair #The pair will always be worth more than the broadway draw
            else:
                self._rating = TRASH #This should never happen, since there should not be any other categories within this elseif
        elif self._pattern > HICARD:
            if self._pattern == STRFLDRAW:
                self._rating = SFDRAW
            elif self._pattern == FLDRAW or self._pattern == STRDRAW:
                self._rating = SEQDRAW
            elif self._pattern == BWDRAW:
                self._rating = BRDRAW
            else:
                self._rating = TRASH #This should never happen, since there should not be any other categories within this elseif
        elif firstRank == 14:
            secondRank = self._hand[1].getValue()
            
            if secondRank == 13:
                self._rating = AK_HI
            elif secondRank == 12:
                self._rating = AQ_HI
            elif secondRank == 11:
                self._rating = AJ_HI
            elif secondRank == 10:
                self._rating = AT_HI
            else:
                self._rating = TRASH
        elif firstRank == 13 and self._hand[1].getValue() == 12:
            self._rating = AT_HI
        else:
            self._rating = TRASH

    def actPre(self, wagers):
        """Decide on waging before the draw. Dependent on exact ordering of the player's strat list."""

        waged = self.getWager()
        rating = self.getRating()

        if(wagers == 2): #No raise yet
            if rating > self._strat[0]:     #Since limping has not been implemented, this is the least aggressive strat parameter
                if waged < 2:               #Unless in big blind, fold and concede chips to the pot
                    self.chipUp(-waged)
            else:
                self.setWager(4)
        elif(wagers == 4): #The pot has been raised
            if rating > self._strat[3]:
                self.chipUp(-waged)
            elif rating > self._strat[1]:
                self.setWager(4)
            else:
                self.setWager(6)
        elif(wagers == 6): #The pot has been reraised
            if rating > self._strat[4]:
                if((rating <= self._strat[3]) and (waged == 4)):    #Only needs to call a single raise
                    self.setWager(6)
                else:   #Fold
                    self.chipUp(-waged)
            elif rating > self._strat[2]:
                self.setWager(6)
            else:
                self.setWager(8)
        elif(wagers != 8): #An incorrect argument has been given
            return wagers #Assumes that error handling detects this case in the caller
        else: #The betting has been capped
            if rating > self._strat[5]:
                if((rating <= self._strat[3]) and (waged == 6)):    #Only needs to call a single raise
                    self.setWager(8)
                else:   #Fold
                    self.chipUp(-waged)
            else:
                self.setWager(8)

        return self.getWager()

class Table(object):
    """A poker table.

        _player: A list of the players that are seated here
        _pot: The amount of chips that have been collected for the winner(s) of the current round.
        _button: The index of the player that has the dealer button at the table.
        _rounds: The number of rounds/hands that have been played at the table.
        
    """

    def __init__(self):
        """Create a new poker table."""

        self._players = list()
        self._pot = 0       #Amount of chips in the middle
        self._button = 0    #The position of the button based on the index of the corresponding player
        self._rounds = 0

    def getPot(self):
        """Getter for _pot"""
        return self._pot

    def addToPot(self, amount):
        """Add chips to _pot.

            amount: The number of chips to add
        
        """
        self._pot += amount

    def resetPot(self):
        """Set _pot to 0. Should only be called after the pot has been given to the winner(s)."""
        self._pot = 0

    def getButton(self):
        """Getter for _button."""
        return self._button

    def passButton(self):
        """Setter for _button. Passes the button one position clockwise, and increments rounds by 1."""

        self._button = (self._button + 1) % SEATS
        self._rounds += 1

    def getRounds(self):
        """Getter for _rounds"""
        return self._rounds

    def seat(self, player, position = -1):
        """Seat a player at the table.

        player: The player that is to be seated.
        position: The index where the player should be inserted in the list of players.

        If a negative position is given, the player is seated in the position where the big blind will be posted.
        The status of the player will be set to SEATED.
        There is currently no error checking for trying to seat a player at an invalid position or a full table.
        
        """

        if position < 0:
            pos = (self.getButton() + 2) % 5
        else:
            pos = position

        player.setStatus(SEATED) #seated
        self._players.insert(pos, player)

    def playHand(self, stake, dealer = None):
        """Play one hand at the table.

        stake: The amount of cash that corresponds to a big blind.
        dealer: A dealer must be supplied to give players their hands. Otherwise, they'll just bet the max amount and flip for the pot.

        returns: The player that is about to post the big blind if that player doesn't meet the requirements for playing at the table.
        Otherwise, it returns None.
        
        Cash isn't really used at the table, but the method needs to know if the table is at the lowest stakes available.
"""

        wagers = 0  #The amount that the players must match to stay in the hand

        #If there's no dealer, players just move in and draws for who wins the pot
        if(dealer == None):
            for player in self._players:
                player.moveIn()
                player.countHand()
                self.addToPot(6 * MIN_STAKE)

            #Award the pot to a random player
            self._players[randint(0, SEATS - 1)].chipUp(self.getPot())
            self.resetPot()
        else:
            #Post SB
            target = (self.getButton() + 1) % SEATS
            self._players[target].setWager(1)

            #Post BB
            target = (target + 1) % SEATS
            self._players[target].setWager(2)

            #Deal hands
            target = (target + 1) % SEATS
            
            for i in range(SEATS):
                self._players[(target + i) % SEATS].setHand(dealer.dealHand())
                self._players[(target + i) % SEATS].rateHand()
                print("Player #" + str(i) + " has:")
                #self._players[(target + i) % SEATS].printHandInfo()

            #Round of betting
            wagers = 2  #Matching the big blind
            ind = 0     #Signifies the player to act relative to the UTG-player(using modulo)
            newWage = 0 #Amount waged by the latest player to act

            #Loop until action comes to a player that has already wagered an amount equal to wagers or the big blind has checked (both means that action is closed)
            while((ind < SEATS) or (self._players[(target + ind) % SEATS].getWager() < wagers)):
                if((ind >= SEATS) and (self._players[(target + ind) % SEATS].getWager() == 0)):
                    ind += 1    #Player is out, check next seat
                else:
                    #Ask player for an action (return value determines if it's a raise, call/check or fold)
                    newWage = self._players[(target + ind) % SEATS].actPre(wagers)

                    if(newWage == wagers + 2):
                        wagers = newWage    #The player raised
                    elif(newWage != wagers):
                        #The player didn't contribute the correct amount to stay in the pot (folded)
                        self.addToPot(newWage)
                        self._players[(target + ind) % SEATS].setWager(0)
                        
                    ind += 1

            #Award the pot to the player with the best hand
            contestants = list()
            for player in self._players:
                if(player.getWager() == wagers):
                    self.addToPot(player.getWager())
                    player.chipUp(-player.getWager())
                    player.setWager(0)
                    contestants.append(player)

            dealer.showDown(contestants, self.getPot())
            self.resetPot()

        #Return the player from the big blind if that player can no longer play at these stakes
        mover = self.finishHand(dealer, stake)
        return mover

    def finishHand(self, dealer, stake):
        """Do cleanup after the hand has finished"""

        #Move button
        self.passButton()

        #If there's a dealer, reset the deck
        if dealer is not None:
            dealer.resetDeck()

        #Move the new big blind player up or down if required
        bb = (self.getButton() + 2) % 5
        if(self._players[bb].getChips() >= MIN_STAKE * MAX_STACK):
            self._players[bb].setStatus(MOVE_UP)
            return self._players.pop(bb)
        elif((stake > MIN_STAKE) and (self._players[bb].getChips() <= MIN_STAKE * MIN_STACK)):
            self._players[bb].setStatus(MOVEDOWN)
            return self._players.pop(bb)
        elif((stake <= MIN_STAKE) and (self._players[bb].getChips() < MIN_STAKE * MIN_UNITS)):
            self._players[bb].setStatus(BUSTO)
            return self._players.pop(bb)
        else:
            return None

    def reportStacks(self):
        """Report the stack sizes for the players"""
        for i in range(len(self._players)):
            output = "\tSeat #" + str(i) + "(" + self._players[i].getType() + "): " + str(self._players[i].getChips()) + " chips"
            print(output)

        print("")

class Manager(object):
    """A stake manager (responsible for all tables having a certain stake)"""

    def __init__(self, stake = MIN_STAKE, tables = MAX_TABLES, cashier = None, recruiter = None, dealer = None):
        """Setting up variables for the manager"""

        self._stake = stake
        self._numtables = tables
        self._cashier = cashier
        self._recruiter = recruiter
        self._dealer = dealer
        self._tables = list()
        self._freeTables = list()   #Tables that are not filled
        self._waitList = list()     #Players waiting to be seated at the manager's stakes
        self._rounds = 0            #Rounds played globally since the manager was hired (even if no tables at these stakes played a hand in the round)
        self._boss = None           #When higher stakes exist, this should be the Manager at the next stakes
        self._upList = list()       #People that were playing here, and should now be transferred to a waiting list at higher stakes
        self._downList = list()     #People that were playing here, and should now be transferred to a waiting list at lower stakes

    def getStake(self):
        """Getter for _stake"""
        return self._stake

    def getNumtables(self):
        """Getter for _numtables"""
        return self._numtables

    def getRounds(self):
        """Getter for _rounds"""
        return self._rounds

    def countRound(self):
        """Setter for _rounds. Increments by 1."""
        self._rounds += 1

    def getBoss(self):
        """Getter for _boss"""
        return self._boss

    def resetUps(self):
        """Make sure that _upList is empty."""
        self._upList = list()

    def resetDowns(self):
        """Make sure that _downList is empty."""
        self._downList = list()        

    def fetchPlayers(self, n = 1):
        """Fills the waitlist with n players"""
        
        self._waitList.extend(self._recruiter.findPlayers(n))

    def startTables(self):
        """Start new tables, populating them with players from the waitList. This process repeats until there are not enough player left in the waitList for another full table."""

        while((len(self._tables) < self.getNumtables()) and (len(self._waitList) >= SEATS)):
            newTab = Table()

            for i in range(SEATS):
                newTab.seat(self._waitList.pop(0), i)

            self._tables.append(newTab)

    def startHand(self):
        """Starts a new hand at all tables"""

        #Get a list of players moving down to the manager's stakes from his boss
        if self.getBoss() is not None:
            for mover in self.getBoss()._downList:
                self._cashier.handleMover(mover, self.getBoss().getStake(), self.getStake())
                self._waitList.append(mover)

            self.getBoss().resetDowns()

        #If there are too many empty tables, ask the recruiter to find a new player
        if(self._recruiter is not None):
            if((len(self._tables) + len(self._freeTables) < self.getNumtables()) or (len(self._freeTables) > len(self._waitList))):
                self.fetchPlayers(GROWRATE)

        #Fill tables from the waitList
        for i in range(len(self._waitList)):
            if(len(self._freeTables) > 0):
                self._tables.append(self._freeTables.pop(0))
                self._tables[-1].seat(self._waitList.pop(0))
            else:
                break

        #Make new tables for the remaining players in the waitlist
        self.startTables()

        #Play a hand at each table. Handle moving players between stakes
        for table in self._tables:
            mover = table.playHand(self.getStake(), self._dealer)

            if mover is not None:
                self._tables.remove(table)
                self._freeTables.append(table)
                status = mover.getStatus()

                if status == BUSTO:
                    self._cashier.handleBust(mover)
                elif status == MOVE_DOWN:
                    mover.moveDown()
                    self._downList.append(mover)
                elif status == MOVE_UP:
                    mover.moveUp()
                    self._upList.append(mover)
                else:
                    print("Error: Illegal status on a player.")

        #Handle players that are about to move up in stakes
        if(self.getStake() == MAX_STAKE):
            for winner in self._upList:
                self._cashier.handleBreak(winner)
        elif(len(self._upList) > 0):
            if(self.getBoss() is None):
                self.hireBoss()     #Not a natural way of hiring. Since the simulator doesn't care about human relationships, it seems ok

            for mover in self._upList:
                self._cashier.handleMover(mover, self.getStake(), self.getBoss().getStake())
                self.getBoss()._waitList.append(mover)

        self.resetUps()     #All move ups have been handled, so reset the list
        self.countRound()   #Keep track of how many rounds have been played since the manager was hired

        #Start a new hand at the next level of stakes
        if self.getBoss() is not None:
            self.getBoss().startHand()

    def hireBoss(self):
        """When there is noone responsible for the next level of stakes, a boss is hired for the manager"""

        #TODO: Look into scaling down the number of tables at higher stakes
        newMan = Manager(self._stake * 2, cashier = self._cashier, dealer = self._dealer)
        self._boss = newMan

    def makeReport(self):
        """Report the stack sizes at the tables"""

        mainhead = "Report for " + str(self.getStake()) + " unit stakes after " + str(self.getRounds()) + " hands played.\n"
        print(mainhead)
        
        for i in range(len(self._tables)):
            header = "Table #" + str(i) + " after " + str(self._tables[i].getRounds()) + " hands.\n"
            print(header)
            self._tables[i].reportStacks()

        for j in range(len(self._freeTables)):
            header = "Table #" + str(len(self._tables) + j) + " after " + str(self._freeTables[j].getRounds()) + " hands.\n"
            print(header)
            self._freeTables[j].reportStacks()


        if(self.getBoss() is not None):
            self.getBoss().makeReport()

class Cashier(object):
    """A cashier that gives players back cash based on their amount of chips"""

    def __init__(self):
        """Setting up variables for the cashier"""

        self._bustos = list()       #Keeps track of the players that leaves and the amount of cash they take with them
        self._highRollers = list()  #Keeps track of the players that are waiting for higher stakes, and their amount of cash they have

    def handleBust(self, busto, stake = MIN_STAKE):
        """Handles a player that has too few chips to keep playing"""

        busto.addCash(busto.getChips() * stake // MIN_STAKE)
        busto.takeChips()

        #Keep track of the player
        self._bustos.append(busto)

    def handleBreak(self, winner, stake = MAX_STAKE):
        """Handle a player that has too many chips to keep playing at the simulated tables"""

        winner.addCash(winner.getChips() * stake // MIN_STAKE)
        winner.takeChips()

        #Keep track of the player
        self._highRollers.append(winner)

    def handleMover(self, mover, oldstake, newstake):
        """Handle a player that is about to move up or down"""

        #print("Before:")
        #print(str(mover._chips))
        mover.addCash(mover.getChips() * oldstake // MIN_STAKE)
        mover.takeChips()
        mover.addChips = mover.getCash() // (newstake // MIN_STAKE)
        mover.setCash(mover.getCash() % (newstake // MIN_STAKE))
        #print("After:")
        #print(str(mover._chips))
        #print(str(mover._cash))

    def makeReport(self):
        """Report on the players that have left the casino"""

        print("Cash of highrollers:")
        for winner in self._highRollers:
            print("\t" + str(winner.getCash()) + "(" + winner.getType() + ")")

        print("\nCash of bustos:")
        for busto in self._bustos:
            print("\t" + str(busto.getCash()) + "(" + busto.getType() + ")")

        print("")

class Recruiter(object):
    """A recruiter that finds new players for the casino"""

    def __init__(self, playertypes):
        """Setting up variables for the recruiter"""

        self._playerTypes = playertypes

    def findPlayers(self, n):
        """Finding several players in one go"""

        recruits = list()

        for i in range(n):
            newFace = Player()
            newType = randint(0, len(self._playerTypes) - 1)
            newFace.setStrat(newType, self._playerTypes[newType])
            recruits.append(newFace)

        return recruits

    def findPlayer(self):
        """Find a single player"""

        return self.findPlayers(1)
