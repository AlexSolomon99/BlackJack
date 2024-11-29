import abc
import player
import random

# actions
WAIT = "wait"
HIT = "hit"
DOUBLE = "double"
SPLIT = "split"
STAND = "stand"


class AbstractStrategy(abc.ABC):

    def select_action(self,
                      bj_hand: player.BlackJackHand,
                      possible_actions: list,
                      *args, **kwargs):
        pass


class DealerStrategy(AbstractStrategy):

    def __init__(self, dealer_max: int = 16):
        self.dealer_max = dealer_max

    def select_action(self,
                      bj_hand: player.BlackJackHand,
                      possible_actions: list,
                      *args, **kwargs):
        # play until the hand is at least equal to the max possible value
        hand_max_value = bj_hand.compute_max_value()
        if hand_max_value >= self.dealer_max:
            return STAND
        return HIT


class RandomStrategy(AbstractStrategy):

    def __init__(self):
        pass

    def select_action(self,
                      bj_hand: player.BlackJackHand,
                      possible_actions: list,
                      *args, **kwargs):
        return random.choice(possible_actions)

