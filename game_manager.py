from card_manager import CardManager
from turn_manager import TurnManager
from board_manager import BoardManager
from player import Player

class GameManager:
    def __init__(self, player_names):
        # Create Players
        self.players = [Player("Professor Pear"), Player("Colonel Ketchup"), Player("Mrs. Peanut"), Player("Miss Violet")]

        # Initialize Game Over Flag
        self.game_over = False

        # Initialize other managers
        self.card_manager = CardManager(self.players)
        self.turn_manager = TurnManager()
        self.board_manager = BoardManager(self.players)

        # Request card setup from CardManager
        self.card_manager.setup_cards()

    def check_accusation(self, player, suspect, weapon, room):
        solution = self.card_manager.solution
        if (suspect == solution['suspect'] and weapon == solution['weapon'] and room == solution['room']):
            print(f"{player.name} wins! The solution was correct.")
            self.game_over = True
            return True
        else:
            print(f"{player.name} made an incorrect accusation and is eliminated.")
            player.is_eliminated = True
            return False

    def run_game_loop(self):
        while not self.game_over:
            for player in self.players:
                if player.is_eliminated:
                    continue                # Skip eliminated players

                # Section incomplete
                print(f"\n{player.name}'s turn:")
                self.turn_manager.run_turn(player, self.board_manager, self.card_manager)
                # ^ Section incomplete

                # Check for last player standing, creates list of players that are NOT marked eliminated
                active_players = [p for p in self.players if not p.is_eliminated]
                if len(active_players) == 1:
                    print(f"{active_players[0].name} is the last player standing and wins!")
                    self.game_over = True
                    break
