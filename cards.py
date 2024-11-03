
class BlackJackCard:

    def __init__(self, face_value: str, symbol: str):
        self.face_value = face_value
        self.symbol = symbol
        self.values = self.get_card_values()

    def get_card_values(self):
        face_values_dict = {
            "2": [2],
            "3": [3],
            "4": [4],
            "5": [5],
            "6": [6],
            "7": [7],
            "8": [8],
            "9": [9],
            "10": [10],
            "jack": [10],
            "queen": [10],
            "king": [10],
            "ace": [1, 11]
        }
        try:
            return face_values_dict[self.face_value]
        except KeyError:
            raise KeyError(f"The face value of the card is unknown: {self.face_value}")

    def __eq__(self, other):
        if self.face_value == other.face_value:
            return True
        return False

