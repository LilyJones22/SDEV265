import random                       # For random dice rolls

class CardManager:                  # CardManager class definition
    def __init__(self, players):    # Initialization function
        self.players = players      # List of player objects
        self.suspects = ["Red", "Blue", "Yellow", "Green"]
        self.weapons = ["Candlestick", "Knife", "Rope"]
        self.rooms = ["Kitchen", "Living Room", "Bedroom", "Bathroom"]
        self.solution = {}          # 1 suspect, 1 weapon, 1 room

    def setup_cards(self):
        # Pick solution cards
        self.solution['suspect'] = random.choice(self.suspects)
        self.solution['weapon'] = random.choice(self.weapons)
        self.solution['room'] = random.choice(self.rooms)

        # Put remaining cards in one list
        remaining_cards = []

        # If card is not in solution, append to 'remaining_cards' list (card = loop control variable)
        for card in self.suspects:
            if card != self.solution['suspect']:
                remaining_cards.append(card)

        for card in self.weapons:
            if card != self.solution['weapon']:
                remaining_cards.append(card)

        for card in self.rooms:
            if card != self.solution['room']:
                remaining_cards.append(card)

        # Shuffle remaining cards (shuffle is a built in function of random)
        random.shuffle(remaining_cards)

        # Deal remaining cards to players evenly
        player_index = 0
        for card in remaining_cards:
            self.players[player_index].hand.append(card)            # Add one card from remaining_cards list to the player hand
            player_index = (player_index + 1) % len(self.players)   # move to next player

    

