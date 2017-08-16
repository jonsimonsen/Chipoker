#Other libs

from entities import * #Card and dealer
from operator import attrgetter

class ChiHand(object):
    """Class for a chinese poker hand."""

    def __init__(self, dealer):
        """Create a new random hand for chinese poker."""

        self._hand = dealer.dealCards(HAND_SIZE)
        self._sortHand() #Planning to sort by suits(most frequent first), then values descending.
        self._suitCounts = self._countSuits()
        print(str(self._suitCounts))

        #self._makeHands(self._hand)

    def _sortHand(self):
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

        mask = list()
        hand = cards
        sorting = sortmethod
        counts = counters
        newBase = base
        index = 0
        single = 0
        first = 0

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

            multiranks = [0, 0, 0]  #For trips, pair, lower pair
            if counts[1] == 1:
                multiranks[0] = hand[0].getValue()
                index += 3
            else:
                if counts[2] == 2:
                    multiranks[2] == hand[2].getValue()
                    index += 2
                if counts[2] > 0:
                    multiranks[1] == hand[0].getValue()
                    index += 2

            single = hand[index]._getValue()

            if multiranks[0] > single:
                first = multiranks[0]
            elif multiranks[1] > single:
                first = multiranks[1]
            else:
                first = single

            #Make sure that there's an index corresponding to the rank at and directly below the hand.
            if 16 - first > len(ALL_HI):
                print('Impossible base for the hand setting procedure.\n')
                return None

            #Make sure that it's possible to create a hand that is less than the base(step 1)
            if ALL_HI[15 - first] > newBase:
                print('Illegal base for the hand setting procedure.\n')
                return None

            mask.append(first)
            curind = 1
            current = cards[curind].getValue()

            while(len(mask) < 5 and curind < 8):
                if mask[-1] == current:
                    curind += 1
                else:

                    pass

                current = hand[curind].getValue()



        first = hand[0]._getValue()
        summation = 0
        counter = 0

        if first > 9:
            summation = 79
            counter = 10

            while counter < first:
                delta = 0
                tdelta = 0
                for i in range(counter):
                    delta += DELTAS[i]
                summation += delta
                counter += 1


        #If base is hicard...
        if base <= MAX_HI:
            pass


    def _makeHands(self, cards):
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

    def printHand(self):
        """Print the cards of the hand."""

        for card in self._hand:
            card.printCard()
