# Import modules
from card_manager import CardManager
from turn_manager import TurnManager
from board_manager import BoardManager
from player import Player

class GameManager:
    def __init__(self, player_names):   # Initialization function
        # Create Players
        self.players = [Player("Red"), Player("Blue"), Player("Yellow"), Player("Green")]

        # Initialize Game Over Flag
        self.game_over = False

        # Initialize other managers
        self.card_manager = CardManager(self.players)
        self.turn_manager = TurnManager()
        self.board_manager = BoardManager(self.players)

        # Request card setup from CardManager
        self.card_manager.setup_cards()

    # Verify accusation function
    def check_accusation(self, player, suspect, weapon, room):
        solution = self.card_manager.solution           # Retrieves game solution from card_manager
        if (suspect == solution['suspect'] and weapon == solution['weapon'] and room == solution['room']):
            print(f"{player.name} wins! The solution was correct.")
            self.game_over = True
            return True                         # IF all entries match the solution, game_over == True
        else:
            print(f"{player.name} made an incorrect accusation and is eliminated.")
            player.is_eliminated = True
            return False                        # ELSE all entries did not match solution and the player is eliminated

    # Game loop function
    def run_game_loop(self):
        while not self.game_over:           # Run game loop until game_over == True
            for player in self.players:
                if player.is_eliminated:
                    continue                # Skip eliminated players

                print(f"\n{player.name}'s turn:")
                self.turn_manager.run_turn(player, self.board_manager, self.card_manager)       # Run next turn using turn_manager

                # Check for last player standing, creates list of players that are NOT marked eliminated
                active_players = [p for p in self.players if not p.is_eliminated]
                if len(active_players) == 1:
                    print(f"{active_players[0].name} is the last player standing and wins!")
                    self.game_over = True
                    break
                       
     
