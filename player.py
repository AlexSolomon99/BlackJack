from typing import List
import copy

import cards
import strategies


class Player:

    def __init__(self, initial_money: float, strategy: strategies.AbstractStrategy, log):
        # set the log
        self.log = log

        # the amount of money the player has and its playing hands
        self.initial_money = initial_money
        self.current_money = initial_money
        self.hands = []
        self.current_hand_idx = 0

        # set the strategy
        self.strategy = strategy

    def create_hand(self, dealt_cards: [], init_bet: float):
        playing_hand = BlackJackHand(initial_cards=dealt_cards,
                                     money_value=init_bet,
                                     log=self.log)
        return playing_hand

    def set_initial_hand(self, dealt_cards: [], init_bet: float):
        # create hand
        hand = self.create_hand(dealt_cards=dealt_cards, init_bet=init_bet)
        self.hands = [hand]

        self.current_money -= init_bet

    @property
    def current_hand(self):
        if self.current_hand_idx >= len(self.hands):
            log_msg = f"Hand with index {self.current_hand_idx} does not exist"
            self.log.error(log_msg)
            raise IndexError(log_msg)
        return self.hands[self.current_hand_idx]

    def __str__(self):
        return f"Money: {self.current_money} | Init Money: {self.initial_money} | Hands: {self.hands}"

    def __repr__(self):
        return f"Money: {self.current_money} | Init Money: {self.initial_money} | Hands: {self.hands}"


class BlackJackHand:

    # actions
    WAIT = "wait"
    HIT = "hit"
    DOUBLE = "double"
    SPLIT = "split"
    STAND = "stand"

    def __init__(self, initial_cards: List[cards.BlackJackCard], money_value: float, log):
        # set the log
        self.log = log

        # win status
        self.blackjack_status = False
        self.win_status = False
        self.money_value = money_value
        self.max_value = -1

        # set the hand's status
        self.possible_actions = [self.WAIT]

        # set the cards
        self.cards = None
        self.card_values = None
        self.set_initial_cards(initial_cards=initial_cards)

    @property
    def is_winner(self):
        return self.win_status

    @property
    def is_blackjack(self):
        return self.blackjack_status

    @property
    def is_hand_closed(self):
        if self.possible_actions == [self.STAND]:
            return True
        return False

    def apply_action(self, action, **input_kwargs):
        action_dict = {
            self.STAND: self.stand,
            self.HIT: self.hit,
            self.DOUBLE: self.double,
            self.SPLIT: self.split
        }
        return action_dict[action](**input_kwargs)

    @staticmethod
    def action_wrap(action_function):
        def wrapper(*args, **kwargs):
            result = action_function(*args, **kwargs)
            if result is None:
                return None, None
            return result

        return wrapper

    def is_action_possible(self, action):
        if action in self.possible_actions:
            return True
        return False

    def set_initial_cards(self, initial_cards):
        self.cards = initial_cards
        self.card_values = self.compute_hand_values()
        self.max_value = self.compute_max_value()

        # check the card values
        if 21 in self.card_values:
            self.win_status = True
            self.blackjack_status = True
            self.possible_actions = [self.STAND]
        else:
            self.possible_actions = [self.HIT, self.DOUBLE, self.STAND]
            if self.cards[0] == self.cards[1]:
                self.possible_actions.append(self.SPLIT)

    def compute_max_value(self):
        # set blackjack value
        if self.blackjack_status:
            return 22

        # compute max value of the hand
        max_value = -1
        for value in self.card_values:
            if value <= 21:
                max_value = value
            else:
                break
        return max_value

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
        self.max_value = self.compute_max_value()

    def add_card_to_hand(self, new_card: cards.BlackJackCard, additional_bet: float = 0):
        self.cards.append(new_card)
        self.money_value += additional_bet
        self.add_card_value(new_card=new_card)

    @action_wrap
    def hit(self, new_card: cards.BlackJackCard, *args, **kwargs):
        # add the new card to the hand
        self.add_card_to_hand(new_card=new_card, additional_bet=0)

        # check the card values
        if 21 in self.card_values:
            self.win_status = True
            self.possible_actions = [self.STAND]
            self.stand()
        elif min(self.card_values) > 21:
            self.possible_actions = [self.STAND]
            self.stand()
        else:
            # set the possible actions
            self.possible_actions = [self.HIT, self.DOUBLE, self.STAND]

        return None, None

    @action_wrap
    def double(self, new_card: cards.BlackJackCard, bet, *args, **kwargs):
        # add the new card to the hand
        self.add_card_to_hand(new_card=new_card, additional_bet=bet)

        # check the card values
        if 21 in self.card_values:
            self.win_status = True
            self.possible_actions = [self.STAND]
            self.stand()
        else:
            # set the possible actions
            self.possible_actions = [self.STAND]
            self.stand()

    @action_wrap
    def split(self, new_card_1, new_card_2, bet, *args, **kwargs):
        # check if the split is possible
        initial_cards = self.cards

        # create the first new hand
        first_hand = BlackJackHand(initial_cards=[initial_cards[0], new_card_1], money_value=bet, log=self.log)

        # create the second new hand
        second_hand = BlackJackHand(initial_cards=[initial_cards[1], new_card_2], money_value=bet, log=self.log)

        return first_hand, second_hand

    @action_wrap
    def stand(self, *args, **kwargs):
        self.max_value = self.compute_max_value()

    def __str__(self):
        cards_str_output = ""
        for card in self.cards:
            cards_str_output += f"{card} "

        output_str = f"Max Value: {self.max_value} | Hand: {cards_str_output} | Possible Actions: {self.possible_actions}"

        return output_str

    def __repr__(self):
        cards_str_output = ""
        for card in self.cards:
            cards_str_output += f"{card} "

        output_str = f"Max Value: {self.max_value} | Hand: {cards_str_output} | Possible Actions: {self.possible_actions}"

        return output_str



