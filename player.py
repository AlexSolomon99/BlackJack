from typing import List
import copy

import cards

class Player:

    def __init__(self, initial_money: float):
        # the amount of money the player has and its playing hands
        self.initial_money = initial_money
        self.current_money = initial_money
        self.hands = []

        # initialise historical data
        self.historical_money = []
        self.historical_actions = []

    def create_hand(self, dealt_cards: [], init_bet: float):
        playing_hand = {
            "cards": dealt_cards,
            "min_card_value": None,
            "max_card_value": None,
            "bet": init_bet
        }
        return playing_hand


class BlackJackHand:

    def __init__(self, initial_cards: List[cards.BlackJackCard], initial_bet: float):
        self.cards = initial_cards
        self.card_values = self.compute_hand_values()
        self.bet = initial_bet

    def compute_hand_values(self):
        values = [0]
        for card in self.cards:
            new_values = []
            current_card_values = card.values
            for card_val in current_card_values:
                for val in values:
                    new_sum = val + card_val
                    new_values.append(new_sum)

            new_values.sort()
            values = copy.deepcopy(new_values)

        return values

    def add_card_value(self, new_card: cards.BlackJackCard):
        new_values = []
        for card_val in new_card.values:
            for val in self.card_values:
                new_sum = val + card_val
                new_values.append(new_sum)

        new_values.sort()
        self.card_values = copy.deepcopy(new_values)

    def add_card_to_hand(self, new_card: cards.BlackJackCard, additional_bet: float = 0):
        self.cards.append(new_card)
        self.bet += additional_bet
        self.add_card_value(new_card=new_card)


