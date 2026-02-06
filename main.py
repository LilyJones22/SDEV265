#Import modules
from game_manager import GameManager

def main():
    game = GameManager(player_names = None)

    print("Solution cards (for testing): ", game.card_manager.solution)

    game.run_game_loop()

    print("\nGame Over!")

if __name__ == "__main__":
    main()
    
