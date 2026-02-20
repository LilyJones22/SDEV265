# Import modules
import random
from card_manager import CardManager
from turn_manager import TurnManager
from board_manager import BoardManager
from player import Player

# GameManager acts as the middle man for logic - UI asks GameManager for a result, GameManager retrieves result from other modules
class GameManager:
    def __init__(self, player_names):   # Initialization function
        # Create Players
        self.players = [Player("Red"), Player("Blue"), Player("Yellow"), Player("Green")]

        # Initialize Game Over Flag
        self.game_over = False

        # Initialize turn order index
        self.current_player_index = 0

        # Initialize other modules
        self.card_manager = CardManager(self.players)
        self.turn_manager = TurnManager(self)
        self.board_manager = BoardManager(self.players)

        # Request card setup from CardManager
        self.card_manager.setup_cards()

    # Tracks the current player 
    def current_player(self):
        return self.players[self.current_player_index]

    # Advances to the next player turn using an index and list of players
    def advance_turn(self):
        if self.game_over:
            return

        for _ in range(len(self.players)):
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if not self.current_player().is_eliminated:
                break

    # Turn action functions
    # Retrieves dice roll from turnManager
    def dice_roll(self) -> int:
        if self.game_over or self.current_player().is_eliminated:
            return 0
        return self.turn_manager.start_turn(self.current_player())

    # Retrieves moves remaining from turnManager
    def get_moves_remaining(self):
        return self.turn_manager.get_moves_remaining()

    # Retrieves movement validation from turnManager
    def get_movement(self, direction: str) -> bool:
        if self.game_over or self.current_player().is_eliminated:
            return False
        return self.turn_manager.move_player(self.current_player(), direction, self.board_manager)

    # Retrieves results of suggestions/accusations from turnManager, handles eliminations/game over
    def handle_room_action(self, action: str, suspect: str, weapon: str, room: str):
        
        # Debug line...
        #print(f"{self.current_player().name}")
        
        if self.game_over or self.current_player().is_eliminated:
            return None
        
        result = self.turn_manager.room_entered(self.current_player(), action, suspect, weapon, room)

        if result.get("eliminated"):
            # Debug line...
            #print(f"{self.current_player().name}")
            return result
        elif result.get("game_over"):
            self.game_over = True
        return result

    # Verifies accusations using the solution stored in cardManager
    def check_accusation(self, player, suspect, weapon, room):
        solution = self.card_manager.solution
        correct = (suspect == solution['suspect'] and weapon == solution['weapon'] and room == solution['room'])
        if correct:
            self.game_over = True
        else:
            player.is_eliminated = True
        return correct

    # Verifies suggestions using cards stored in each player's hand within player class
    def check_suggestion(self, player, suspect, weapon, room):
        for p in self.players:
            if p == player:
                continue
            for card in p.hand:
                if card in (suspect, weapon, room):
                    return card
        return None

    # Get UI update data
    def get_active_players(self):
        return [p for p in self.players if not p.is_eliminated]

    def get_player_position(self, player):
        return self.board_manager.get_player_position(player)
       
