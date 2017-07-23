#Other libs
from chipoker import *

class Sim(object):
    """A class for running the simulator."""

    def __init__(self):
        """Run the simulator."""

        cardomat = Dealer()
        testHand = ChiHand(cardomat)
        testHand.printHand()

if __name__ == '__main__':
    sim = Sim()
