#Other libs

from entities import * #Card and dealer
from operator import attrgetter

class ChiHand(object):
    """Class for a chinese poker hand."""

    def __init__(self, dealer):
        """Create a new random hand for chinese poker."""

        self._hand = dealer.dealCards(HAND_SIZE)
        self._sortHand() #Planning to sort by suits(most frequent first), then values descending.
        self._suitcounts = self._countSuits()
        print(str(self._suitcounts))

        self._makeHands(self._hand)

    def _sortHand(self):
        """Sort the hand by suits(most frequent first), then by values descending."""

        self._hand.sort(key=attrgetter('_suit', '_value'), reverse=True)

    def _makeHands(self, cards):
        """Starts with a hand and returns the chinese poker hands that can be created as a list of rankings."""

        if len(self._hand) == 13 or len(self._hand) == 8:
            print('Back or middle\n')
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
