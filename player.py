# Player Class Definition
class Player:
    def __init__(self, name):           # Initialization Function
        self.name = name                # Player name
        self.position = 0               # Position on board
        self.hand = []                  # List of cards in hand
        self.is_eliminated = False      # Elimination status
