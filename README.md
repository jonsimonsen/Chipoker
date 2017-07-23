# Chipoker
Simulator for chinese poker

# Description
The simulator is based on the following rules:

-Hands are compared pairwise. <br>
-For each hand, the winner gets one point from the loser. <br>
-The overall winner (having gained the most points) gets an additional point from the loser. <br>
-Bonus points are as follows: 1 for a full house in the middle, 2 for trips in the back, 3 for quads in the front, 4 for a straight flush in the front. <br>
-Scoring for quads/straight flushes in the middle are not yet determined. <br>
-No additional bonus points are rewarded (6 pairs, triple straights/ triple flushes or other). <br>

# v0.1
Deals a single hand, and prints the cards. Contains a config file that might need some cleanup.
