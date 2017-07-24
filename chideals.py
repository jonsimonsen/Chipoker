#Other libs
from chipoker import *

class Sim(object):
    """A class for running the simulator."""

    def __init__(self):
        """Run the simulator."""

        self._greet()

        cardomat = Dealer()
        testHand = ChiHand(cardomat)
        testHand.printHand()

    def _greet(self):
        """Display a greeting."""

        print(GREETING)

if __name__ == '__main__':
    sim = Sim()
