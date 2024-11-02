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

    @staticmethod
    def create_hand(dealt_cards: [], init_bet: float):
        playing_hand = BlackJackHand(initial_cards=dealt_cards,
                                     initial_bet=init_bet)
        return playing_hand

    def set_initial_hand(self, dealt_cards: [], init_bet: float):
        # create hand
        hand = self.create_hand(dealt_cards=dealt_cards, init_bet=init_bet)
        self.hands = [hand]

        # remove bet from the currently owned money
        self.current_money -= init_bet

    def hit(self, new_card: cards.BlackJackCard, hand_idx):
        # get the current hand
        current_hand = self.hands[hand_idx]

        # add the new card to the hand
        current_hand.add_card_to_hand(new_card=new_card, additional_bet=0)

        # reset the hands list
        self.hands[hand_idx] = current_hand

    def double(self, new_card: cards.BlackJackCard, bet, hand_idx):
        # get the current hand
        current_hand = self.hands[hand_idx]

        # add the new card to the hand
        current_hand.add_card_to_hand(new_card=new_card, additional_bet=bet)

        # remove bet from the current amount of money
        self.current_money -= bet

        # reset the hands list
        self.hands[hand_idx] = current_hand

    def split(self):
        pass


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

        values = list(set(values))
        values.sort()

        return values

    def add_card_value(self, new_card: cards.BlackJackCard):
        new_values = []
        for card_val in new_card.values:
            for val in self.card_values:
                new_sum = val + card_val
                new_values.append(new_sum)

        new_values = list(set(new_values))
        new_values.sort()
        self.card_values = copy.deepcopy(new_values)

    def add_card_to_hand(self, new_card: cards.BlackJackCard, additional_bet: float = 0):
        self.cards.append(new_card)
        self.bet += additional_bet
        self.add_card_value(new_card=new_card)


