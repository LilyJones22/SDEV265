#Import modules
from game_manager import GameManager

def main():
    game = GameManager(player_names = None)

    # Print randomly chosen solution for testing purposes
    print("Solution cards (for testing): ", game.card_manager.solution)

    # Runs game loop function from game_manager
    game.run_game_loop()

    # Prints Game Over when game loop ends
    print("\nGame Over!")

if __name__ == "__main__":      # Only runs main() function if this file is executed directly
    main()
    
