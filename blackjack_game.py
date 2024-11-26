import random

import cards
import player
import strategy


class BlackJack:
    # actions
    HIT = "hit"
    DOUBLE = "double"
    SPLIT = "split"
    STAND = "stand"
    SURRENDER = "surrender"

    def __init__(self, game_config: dict, log, deterministic=False):
        # get the config
        self.game_config = game_config
        self.log = log
        self.log.info(f"Game config: {self.game_config}")

        # set the random seed if required
        if deterministic:
            random.seed(self.seed)

        # game attributes
        self.deck = []
        self.players_dict = {}
        self.current_player_idx = 0

        # default action
        self.default_action = self.HIT

        # reset
        self.reset()

    def reset(self):
        # create the playing card deck and shuffle it
        self.deck = self.create_multiple_card_decks(num_decks=self.num_decks)
        random.shuffle(self.deck)

        # create the players
        for num_player in range(self.num_players):
            self.players_dict[num_player] = player.Player(initial_money=self.default_init_money, log=self.log)

            # give 2 cards to the current player
            card_1 = self.deck.pop(0)
            card_2 = self.deck.pop(0)
            self.players_dict[num_player].set_initial_hand([card_1, card_2], init_bet=self.min_bet)

        # give the dealer its hand
        card_1 = self.deck.pop(0)
        card_2 = self.deck.pop(0)
        self.players_dict["dealer"] = player.Player(initial_money=1e10, log=self.log)
        self.players_dict["dealer"].set_initial_hand([card_1, card_2], init_bet=self.min_bet)

        self.current_player_idx = 0

    def play_one_game(self):
        self.log.info(f"Started game")
        for player_idx in self.players_dict:
            self.log.info(f"Player {player_idx}")
            # loop only through the non-dealer players
            if player_idx == "dealer":
                break

            # get the current player
            self.current_player_idx = player_idx
            hand_idx = 0

            # iterate through all the hands
            while hand_idx < len(self.players_dict[player_idx].hands):
                self.log.info(f"Initial Hand: {self.players_dict[player_idx].hands[hand_idx]}")
                is_hand_open = True

                # select player action
                player_action = self.SPLIT

                while is_hand_open:
                    is_hand_open, hand_max_val = self.step(
                        player_idx=player_idx,
                        hand_idx=hand_idx,
                        current_hand=self.players_dict[player_idx].hands[hand_idx],
                        player_action=player_action)
                    self.log.info(f"Current Hand: {self.players_dict[player_idx].hands[hand_idx]}")

                hand_idx += 1

        # play the dealer - always hits until above 16
        player_idx = "dealer"
        is_hand_open = True
        hand_idx = 0
        hand_max_val = self.players_dict[player_idx].hands[hand_idx].compute_max_value()
        player_action = self.HIT
        self.log.info(f"Initial Dealer Hand: {self.players_dict[player_idx].hands[hand_idx]}")

        while (hand_max_val <= 16.0) and is_hand_open:
            is_hand_open, hand_max_val = self.step(
                player_idx=player_idx,
                hand_idx=0,
                current_hand=self.players_dict[player_idx].hands[hand_idx],
                player_action=player_action)
            self.log.info(f"Dealer Hand: {self.players_dict[player_idx].hands[hand_idx]}")

        # compute payout
        dealer_score = self.players_dict["dealer"].hands[0].max_value

        for player_idx in self.players_dict:
            # loop only through the non-dealer players
            if player_idx == "dealer":
                break

            for hand in self.players_dict[player_idx].hands:
                hand_bet = hand.money_value
                if hand.max_value > dealer_score:
                    # check if the value is given by a blackjack or not
                    if hand.max_value == "22":
                        return_money = (self.blackjack_payout + 1) * hand_bet
                    else:
                        return_money = 2 * hand_bet
                    self.players_dict[player_idx].current_money += return_money

                elif hand.max_value == dealer_score:
                    self.players_dict[player_idx].current_money += hand_bet
                else:
                    # the player gets no money
                    pass

    def step(self, player_idx: [int | str], hand_idx: int, current_hand: player.BlackJackHand,
             player_action: str = None) -> (bool, float):
        """
        :param player_idx:
        :param hand_idx:
        :param current_hand:
        :param player_action:
        :return: (is_hand_open, hand_max_value)
        """
        # check if the hand is closed or can still be played
        if current_hand.is_hand_closed:
            return False, current_hand.max_value

        # if it is not closed, apply the action
        # validate action - check if the action is possible
        is_action_possible = current_hand.is_action_possible(action=player_action)

        if is_action_possible:
            action_to_take = player_action
        else:
            action_to_take = self.default_action

        # compute the arguments needed to perform the action
        if action_to_take in [self.HIT, self.DOUBLE]:
            new_card = self.deck.pop(0)
            action_kwargs = {"new_card": new_card,
                             "bet": self.min_bet}

        elif action_to_take in [self.SPLIT]:
            new_card_1 = self.deck.pop(0)
            new_card_2 = self.deck.pop(0)
            action_kwargs = {"new_card_1": new_card_1,
                             "new_card_2": new_card_2,
                             "bet": self.min_bet}

        elif action_to_take in [self.STAND]:
            action_kwargs = {}
        else:
            action_kwargs = {}

        # apply action
        first_hand, second_hand = current_hand.apply_action(action_to_take, **action_kwargs)

        # in case of split, do smth special
        if (first_hand is not None) and (second_hand is not None):
            self.players_dict[player_idx].hands[hand_idx] = first_hand
            current_hand = self.players_dict[player_idx].hands[hand_idx]
            self.players_dict[player_idx].hands.append(second_hand)

        # check if the hand is closed or can still be played
        if current_hand.is_hand_closed:
            return False, current_hand.max_value
        return True, current_hand.max_value

    def create_multiple_card_decks(self, num_decks: int) -> list:
        """
        Method used to create an un-shuffled card deck, containing the given number of individual card decks.

        :param num_decks: Number of card decks contained within the final deck of cards.
        :type num_decks: int
        :return: A list containing all the cards in the deck. A card is tuple which has 2 elements:
                (card number/symbol, card suit)
        :return type: list
        """
        card_deck = []
        for _ in range(num_decks):
            card_deck.extend(self.create_single_card_deck())

        return card_deck

    @classmethod
    def create_single_card_deck(cls) -> list:
        """
        Method used to create a single un-shuffled card deck, containing 52 cards.

        A card is tuple which has 2 elements: (card number/symbol, card suit)

        :return: A list containing all the cards in the deck.
        :return type: list
        """
        card_deck = []
        card_suits = ["hearts", "diamonds", "spades", "clubs"]

        for num in range(2, 10):
            numbered_suits = [cards.BlackJackCard(face_value=str(num), symbol=suit) for suit in card_suits]
            card_deck.extend(numbered_suits)

        for symbol in ["jack", "queen", "king", "ace"]:
            symbol_suits = [cards.BlackJackCard(face_value=symbol, symbol=suit) for suit in card_suits]
            card_deck.extend(symbol_suits)

        return card_deck

    @property
    def num_players(self):
        """
        Property used to get the number of players playing the current game.
        :return: Number of players playing the current game
        :return type: int
        """
        return self.game_config["num_players"]

    @property
    def num_decks(self):
        """
        Property used to get the number of deck cards used in the current game.
        :return: Number of card decks used in the current game
        :return type: int
        """
        return self.game_config["num_decks"]

    @property
    def min_bet(self):
        """
        Property used to get the minimum bet that a player needs to bet in order to participate in the game.
        :return: Minimum bet to play the game.
        :return type: float
        """
        return self.game_config["min_bet"]

    @property
    def dealer_soft_17(self):
        """
        Property used to get the action required by the dealer in case it gets a hand containing a soft-17.

        A soft-17 is a pair of cards adding up to 17 containing an "Ace" card that counts as 11.

        The options are either "H" or "S".

        "H" means the dealer has to hit when getting the soft-17.
        "S" means the dealer has to stand when getting the soft-17.

        :return: The action required by the dealer in case it gets a hand containing a soft-17
        :return type: str
        """
        return self.game_config["dealer_soft_17"]

    @property
    def blackjack_payout(self):
        """
        Property used to get the payout a player gets when he gets a "blackjack". This means that the pair of 2 cards
        first dealt to him are an "Ace" and a 10-valued card.
        :return: The payout received when getting a blackjack asa a fraction from the bet amount.
        :return type: float
        """
        return self.game_config["blackjack_payout"]

    @property
    def seed(self):
        """
        Property used to get the seed that can be used for setting up the random generators.
        :return: The random seed.
        :return type: int
        """
        return self.game_config["seed"]

    @property
    def default_init_money(self):
        """
        Property used to get the default value for the initial money a player can have at the table.
        :return: Initial sum of money a player has.
        :return type: float
        """
        return self.game_config["default_init_money"]
