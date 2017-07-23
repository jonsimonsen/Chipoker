#Other libs

from entities import * #Card and dealer

class ChiHand(object):
    """Class for a chinese poker hand."""

    def __init__(self, dealer):
        """Create a new random hand for chinese poker."""

        self.hand = dealer.dealCards(13)
        #self._sortHand() #Planning to sort by suits(most frequent first), then values descending.

    def printHand(self):
        """Print the cards of the hand."""

        for card in self.hand:
            card.printCard()
