import random

import cards
import player


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

        # reset
        self.reset()

    def reset(self):
        # create the playing card deck and shuffle it
        self.deck = self.create_multiple_card_decks(num_decks=self.num_decks)
        random.shuffle(self.deck)

        # create the players
        for num_player in range(self.num_players):
            self.players_dict[num_player] = player.Player(initial_money=self.default_init_money)
        self.current_player_idx = 0

    def step(self, player_action: str = None):
        current_player = self.players_dict[self.current_player_idx]
        current_hand = current_player.hands[current_player.current_hand_idx]

        # validate action - check if the action is possible
        is_action_possible = current_hand.is_action_possible()


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
