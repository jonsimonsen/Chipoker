#Other libs

from entities import * #Card and dealer
from operator import attrgetter

class ChiHand(object):
    """Class for a chinese poker hand."""

    def __init__(self, dealer):
        """Create a new random hand for chinese poker."""

        self._hand = dealer.dealCards(HAND_SIZE)
        self._suitSort() #Planning to sort by suits(most frequent first), then values descending.
        self._suitCounts = self._countSuits()
        print(str(self._suitCounts))

    def _suitSort(self):
        """Sort the hand by suits(most frequent first), then by values descending."""

        self._hand.sort(key=attrgetter('_suit', '_value'), reverse=True)

    def _hValueSort(self, hand):
        """Sort the hand by values descending. Return the sorted hand."""

        hand.sort(key = attrgetter('_value'), reverse = True)
        return hand

    def _valueSort(self, hand):
        """Sort the hand by values.

        Lists quadruples first. Then triples, doubles and singletons.
        Within each group, values are sorted descending."""

        cards = hand
        cards.sort(key = attrgetter('_value'), reverse = True)
        newHand = list() #For the sorted cards

        counts = [0, 0, 0, 0]   #Quads, trips, pairs, singletons
        occurences = 0
        val = 0
        i = 0

        while i < len(cards):
            target = 0
            val = cards[i]._value
            occurences = sum(curr._value == val for curr in cards)

            if occurences > 4:
                print('Illegal hand.\n')
                return None

            if occurences < 2:
                target += counts[3]

            if occurences < 3:
                target += counts[2] * 2

            if occurences < 4:
                target += counts[1] * 3

            if occurences < 5:
                target += counts[0] * 4

            for occurence in range(occurences):
                newHand.insert((target + occurence), cards[i])
                i += 1

            counts[4 - occurences] += 1

        return [newHand, counts]

    def _setHands(self, cards, sortmethod, counters, base = 9999):

        mask = list()               #Should hold the indices of the cards for the hand to be set
        hand = cards
        sorting = sortmethod
        counts = counters
        newBase = base
        baseHand = list()           #To hold the ranks of the base hand
        index = 0                   #Index of the first singleton that has not been considered yet
        single = 0                  #Value of the first singleton that hasn't been considered
        first = 0                   #Value of the highest card that can be played
        current = 0                 #Value of the highest unprocessed card
        multiCounter = NOSEQ        #Keeps track of progress for the ranks that have multiple suits present. See config file for details.
        okBase = False              #Becomes True when the hand being set is confirmed to be smaller than the base
        Legality = True             #To keep track of the possibility that a legal hand can be set.

        #Base hi-card...
        if newBase <= A_HI:
            #Make sure the hand is sorted correctly
            if sorting != VALUED:
                newSort = self._valueSort(cards)
                hand = newSort[0]
                counts = newSort[1]
                sorting = VALUED

            #Make sure the hand is a real candidate for having hi-card as the best hand
            if counts[0] > 0:
                return None     #It's impossible not to have a pair if the hand contain quads
            if counts[1] > 1:
                return None     #It cannot be best to have a hi-card base when the hand contains two trips
            if counts[1] > 0 and counts[2] > 0:
                return None     #It's better to have pairs in back and middle and the best possible hi-card in front.
            if len(cards) < 13 and counts[1] > 0:
                return None     #It's impossible not to have a pair when having trips remaining after setting the back hand
            if counts[2] > 2:
                return None     #It's better to have a pair in every hand than hi-card in every hand.
            if len(cards) < 13 and counts[2] > 1:
                return None     #Same as above

            #Record the rank of non-singleton values
            multiranks = [0, 0, 0]  #For trips, pair, lower pair
            if counts[1] == 1:
                multiranks[0] = hand[0].getValue()
                index += 3
                multiCounter = MULTISEQ
            else:
                if counts[2] == 2:
                    multiranks[2] == hand[2].getValue()
                    index += 2

                if counts[2] > 0:
                    multiranks[1] == hand[0].getValue()
                    index += 2
                    multiCounter = PAIRSEQ

            #Process first card of the hand setting
            single = hand[index]._getValue()

            if multiranks[0] > single:
                first = multiranks[0]
                multiCounter = MULTICAN
            elif multiranks[1] > single:
                first = multiranks[1]
                multiCounter = PAIRCAN
            else:
                first = single

            #Get the baseHand and make sure that the base value is within its ranges.
            baseHand = self._getBaseHand(newBase)
            if baseHand = None:
                return None

            #Make sure that it's possible to create a hand that is less than the base(step 1)
            if first > baseHand[0]:
                print(ERR_AA)
                return None
            elif first < baseHand[0]:
                okBase = True

            #Record index of the first card in the setting
            if multiCounter == MULTICAN:
                mask.append(0)
                multiCounter = MULTIPRO
            elif multiCounter == PAIRCAN:
                mask.append(0)
                if multiranks[2] > 0:
                    multiCounter = NEXTPAIRSEQ
                else:
                    multiCounter = PAIRPRO
            else:
                mask.append(index)
                index += 1
                single = hand[index].getValue()

            #Process the second card of the hand setting
            while len(mask) < 2:
                #Handle hands that doesn't have enough remaining candidates to be created
                hasTwoPairs = (multiranks[2] > 0)     #assignment based on eval of parenthesised expression
                legality = _enoughRemaining(multiCounter, len(mask), len(hand), index, hasTwoPairs)
                if multiCounter in SINGLES:
                    if (len(hand) < 8 and index >= len(hand) - 1) or (len(hand) >= 8 and index >= len(hand) - 3):
                        print(ERR_A)
                        legality = False
                elif multiCounter == MULTISEQ:
                    if len(hand) < 8:   #This should never happen
                        print(ERR_HI + ERR_B)
                        legality = False
                    elif len(hand) >= 8 and index >= len(hand) - 2:
                        print(ERR_A)
                        legality = False
                elif multiCounter == NEXTPAIRSEQ:
                    if len(hand) < 13: #This should never happen
                        print(ERR_HI + ERR_C)
                        legality = False
                    elif len(hand) == 13 and index >= len(hand) - 2:
                        print(ERR_A)
                        legality = False
                elif multiCounter == PAIRSEQ:
                    if len(hand) < 8: #This should never happen
                        print(ERR_HI + ERR_D)
                        legality = False
                    elif multiranks[2] > 0:
                        if len(hand) < 13:
                            print(ERR_HI + ERR_C)
                            legality = False
                        elif len(hand) == 13 and index >= len(hand) - 1:
                            print(ERR_A)
                            legality = False
                    else:
                        if len(hand) < 8:
                            print(ERR_HI + ERR_D)
                            legality = False
                        elif index >= len(hand) - 2:
                            print(ERR_A)
                            legality = False

    def _enoughRemaining(multiCount, processed, remaining, nextSingle, hasMultiples):
        '''Returns True if enough candidates to fill the hand remains. Otherwise, prints an appropriate error message and returns False.

        multiCount: The available values should be specified in the config file. MULTISEQ should be the smallest and NOSEQ the highest.
        processed: The number of cards for the current hand (back, middle or front) that have been processed. Should be at least 1 before calling this method.
        remaining: The number of cards in the pool of candidates for this hand (back, middle or front). This should include cards that have already been processed (included or excluded from the hand).
        nextSingle: Index of the next singleton value in the card pool (sorted using "VALUED" sorting).
        hasMultiples: Should be True if there are more than a single pair in the card pool, False otherwise.
        '''

        message = ''

        #Verify that the input is within expected range
        if multiCount not in SINGLES:
            if remaining - nextSingle <
        if multiCount not in range(NOSEQ + 1):
            message = 'multiCount not in range.'
        elif processed not in range(1, 5):
            message = 'processed not in range (1-4).'
        elif remaining not in range(3, 14):
            message = 'remaining not in range (3-13).'
        elif remaining < 8 and processed > 2:
            message = 'remaining and processed inconsistency.'
        elif nextSingle not in range(13):
            message = 'nextSingle not in range (0-12).'
        elif nextSingle >= remaining:
            message = 'nextSingle and remaining inconsistency.'

        if message:
            print(message + ERR_ERARG)
            return False

        if remaining < 8:
            handSize = 3
        else:
            handSize = 5

        breakPoint = remaining + processed - handSize

        if multiCount in SINGLES:
            #if (remaining < 8 and nextSingle >= remaining - 1) or (remaining >= 8 and nextSingle >= remaining - 3):
            if nextSingle > breakPoint
                message = ERR_A
        elif multiCount == MULTISEQ:
            if remaining < 8:   #This should never happen
                message = ERR_HI + ERR_B
            elif nextSingle > breakPoint + 1:
                message = ERR_A
        elif multiCount == NEXTPAIRSEQ:
            if remaining < 13: #This should never happen
                message = ERR_HI + ERR_C
            elif remaining == 13 and nextSingle >= remaining - 2:
                message = ERR_A
        elif multiCount == PAIRSEQ:
            if remaining < 8: #This should never happen
                message = ERR_HI + ERR_D
            elif multiranks[2] > 0:
                if remaining < 13:
                    message = ERR_HI + ERR_C
                elif remaining == 13 and nextSingle >= remaining - 1:
                    message = ERR_A
            else:
                if remaining < 8:
                    message = ERR_HI + ERR_D
                elif nextSingle >= remaining - 2:
                    message = ERR_A

        if message:
            print(message)
            return False
        else:
            return True

                if multiCounter == MULTISEQ:
                    if multiranks[0] > single:
                        current = multiranks[0]
                        multiCounter = MULTICAN
                    else:
                        current = single
                elif multiCounter == NEXTPAIRSEQ:
                    if multiranks[2] > single:
                        current = multiranks[2]
                        multiCounter = NEXTPAIRCAN
                    else:
                        current = single
                elif multiCounter == PAIRSEQ:
                    if multiranks[1] > single:
                        current = multiranks[1]
                        multiCounter = PAIRCAN
                    else:
                        current = single
                elif multiCounter not in SINGLES:
                    print('Error in hand setting. Report multiCounter inconsistency.\n')
                    return None
                else:
                    current = single

                #Make sure that it's possible to create a hand that is less than the base
                if (not okBase) and current > baseHand[1]:   #Should do some adjustments, since the base is not necessarily illegal...
                    if current == single:
                        index += 1
                        single = hand[index].getValue()
                    else:
                        if multiCounter == MULTICAN:
                            print(ERR_AB)
                            return None
                        elif multiCounter == PAIRCAN:
                            if multiranks[2] > 0:
                                multiCounter = NEXTPAIRSEQ
                            else:
                                multiCounter = PAIRPRO
                        elif multiCounter == NEXTPAIRCAN:
                            multiCounter = NEXTPAIRPRO
                else:
                    if (not okBase) and current < baseHand[1]:
                        okBase = True

                    if multiCounter == MULTICAN:
                        mask.append(0)
                        multiCounter = MULTIPRO
                    elif multiCounter == PAIRCAN:
                        mask.append(0)
                        if multiranks[2] > 0:
                            multiCounter = NEXTPAIRSEQ
                        else:
                            multiCounter = PAIRPRO
                    elif multiCounter == NEXTPAIRCAN:
                        mask.append(2)
                        multiCounter = NEXTPAIRPRO
                    else:
                        mask.append(index)
                        index += 1
                        single = hand[index].getValue()

        # #old stuff, probably not important...
        # first = hand[0]._getValue()
        # summation = 0
        # counter = 0
        #
        # if first > 9:
        #     summation = 79
        #     counter = 10
        #
        #     while counter < first:
        #         delta = 0
        #         tdelta = 0
        #         for i in range(counter):
        #             delta += DELTAS[i]
        #         summation += delta
        #         counter += 1

    def _getBaseHand(self, base):
        """Returns a list of the base hand."""

        hand = list()   #List for the hand to be returned. Might differ based on the range of the base.
        baseSum = 0     #Lowest possible base based on the elements in hand
        baseDif = 0     #Difference between base and baseSum
        count = 0       #Number of appended elements in hand
        rank = 0        #To keep track of the rank of a card
        elims = 0       #The number of eliminated hands corresponding to the current rank

        if base <= 0:
            print('Illegal function argument to _getBaseHand. Must be greater than 0.\n')
            return None
        elif base <= A_HI:
            while count < 4:
                baseDif = base - baseSum
                rank = 2

                while TOT_HI[count][rank - 2] < baseDif:
                    rank += 1

                hand.append(rank)
                temp = baseSum
                baseSum += TOT_HI[count][rank - 3]
                count += 1

                #If the hand is a three card hand, break out of the loop
                if count == 2 and (temp + TOT_HI[1][rank - 2] - base < rank - 2):
                    baseSum += TOT_HI[2][rank - 3]
                    break

            hand.append(base + 1 - baseSum)
            return hand     #Should move this outside once different hand types are supported
        else:
            print('_getBaseHand error. The given base is not supported yet.\n')     #When done, should say that the base is too high.
            return None

    def _makeHands(self, cards):    #This seems like an old implementation that should probably get deleted.
        """Starts with a hand and returns the chinese poker hands that can be created as a list of rankings."""

        foot = 0
        ace = False
        current = 0
        counter = 5
        candidate = -1

        if len(self._hand) == 13 or len(self._hand) == 8:
            print('Back or middle\n')
            for suitLength in self._suitCounts:
                if suitLength >= 5:
                    current = self._hand[foot].getValue()
                    if current == 14:
                        ace = True

                    while counter <= suitLength:
                        if self._hand[foot + 4].getValue() == current - 4:
                            candidate = 0
                        counter += 1
                else:
                    foot += suitLength
            return
        elif len(self._hand) == 3:
            print('front\n')
            return
        else:
            print('illegal hand size.\n')
            return

    def _countSuits(self):
        """Returns a list containing the count of the various suits in the hand. The hand should be sorted in advance."""

        spades = sum(card._suit == SPADES for card in self._hand)
        hearts = sum(card._suit == HEARTS for card in self._hand)
        diamonds = sum(card._suit == DIAMONDS for card in self._hand)
        clubs = sum(card._suit == CLUBS for card in self._hand)
        #print(str(spades), str(hearts), str(diamonds), str(clubs))
        return [spades, hearts, diamonds, clubs]

    def _testHicards(self):
        """Actually used to test that _getBaseHand produces reasonable results"""

        for i in range(A_HI):
            res = self._getBaseHand(i + 1)
            print(i + 1, ': ', res)

    def printHand(self):
        """Print the cards of the hand."""

        for card in self._hand:
            card.printCard()
