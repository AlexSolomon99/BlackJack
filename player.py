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

        # set the possible actions
        self.possible_actions = [self.HIT, self.DOUBLE, self.STAND, self.SURRENDER]

        # check if split is a possible action
        if hand.cards[0] == hand.cards[1]:
            self.possible_actions.append(self.SPLIT)

    def hit(self, new_card: cards.BlackJackCard, hand_idx):
        # get the current hand
        current_hand = self.hands[hand_idx]

        # add the new card to the hand
        current_hand.add_card_to_hand(new_card=new_card, additional_bet=0)

        # reset the hands list
        self.hands[hand_idx] = current_hand

        # set the possible actions
        self.possible_actions = [self.HIT, self.DOUBLE, self.STAND, self.SURRENDER]

    def double(self, new_card: cards.BlackJackCard, bet, hand_idx):
        # get the current hand
        current_hand = self.hands[hand_idx]

        # add the new card to the hand
        current_hand.add_card_to_hand(new_card=new_card, additional_bet=bet)

        # remove bet from the current amount of money
        self.current_money -= bet

        # reset the hands list
        self.hands[hand_idx] = current_hand

        # set the possible actions
        self.possible_actions = [self.STAND, self.SURRENDER]

    def split(self, new_card_1, new_card_2):
        # get info about the current hand
        current_hand = self.hands[0]
        initial_cards = current_hand.cards
        initial_bet = current_hand.bet

        self.hands = []

        # create the first new hand
        first_hand = self.create_hand(dealt_cards=[initial_cards[0], new_card_1], init_bet=initial_bet)

        # create the second new hand
        second_hand = self.create_hand(dealt_cards=[initial_cards[1], new_card_2], init_bet=initial_bet)

        # save the hands
        self.hands = [first_hand, second_hand]

        # bet again for the second hand
        self.current_money -= initial_bet


class BlackJackHand:

    # actions
    WAIT = "wait"
    HIT = "hit"
    DOUBLE = "double"
    SPLIT = "split"
    STAND = "stand"
    SURRENDER = "surrender"

    def __init__(self, initial_cards: List[cards.BlackJackCard], money_value: float):
        self.cards = initial_cards
        self.card_values = self.compute_hand_values()
        self.money_value = money_value

        # set the hand's status
        self.possible_actions = [self.WAIT]

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
        self.money_value += additional_bet
        self.add_card_value(new_card=new_card)

    def hit(self, new_card: cards.BlackJackCard):
        # add the new card to the hand
        self.add_card_to_hand(new_card=new_card, additional_bet=0)

        # set the possible actions
        self.possible_actions = [self.HIT, self.DOUBLE, self.STAND, self.SURRENDER]

    def double(self, new_card: cards.BlackJackCard, bet):
        # add the new card to the hand
        self.add_card_to_hand(new_card=new_card, additional_bet=bet)

        # set the possible actions
        self.possible_actions = [self.STAND, self.SURRENDER]

    def split(self, new_card_1, new_card_2):
        # check if the split is possible
        initial_cards = self.cards

        if len(initial_cards) != 2:
            print(f"The split cannot be done. The number of cards is different from 2: {len(initial_cards)}")
            return None, None

        if initial_cards[0] != initial_cards[1]:
            print(f"The split cannot be done. Cards are different")
            return None, None

        initial_bet = self.money_value

        # create the first new hand
        first_hand = BlackJackHand(initial_cards=[initial_cards[0], new_card_1], money_value=initial_bet)

        # create the second new hand
        second_hand = BlackJackHand(initial_cards=[initial_cards[1], new_card_2], money_value=initial_bet)

        return first_hand, second_hand



