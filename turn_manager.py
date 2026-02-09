import random                   # For random dice rolls

class TurnManager:
    def __init__(self):
        pass

    # Dice rolling function
    def roll_dice(self):
        roll1 = random.randint(1,6)
        roll2 = random.randint(1,6)
        total = roll1 + roll2
        print(f"Rolled Dice: {roll1} + {roll2} = {total}")
        return total

    def run_turn(self, player, board_manager, card_manager):
        # Player turn function:
        # 1. Roll dice for movement points
        # 2. Allow movement until points run out or player enters room
        # 3. If player enters room, get suggestion or accusation

        # 1. Roll Dice
        moves_remaining = self.roll_dice()      # Calls roll_dice function and sets total to 'moves_remaining'
        print(f"\n--- {player.name} has {moves_remaining} movements. Position: {player.position}")

        # 2. Movement loop
        while moves_remaining > 0:              # WHILE player has movement, accept a direction as input
            print(f"Moves left: {moves_remaining}")
            move = input("Enter move (up/down/left/right): ").strip().lower()   # .strip removes whitespace, .lower used for case sensitivity

            if move in ["up", "down", "left", "right"]:                 # IF player input is a valid direction...
                success = board_manager.move_player(player, move)       # Check movement validation function in board_manager...
                if success:                                             # IF movement is successful, reduce moves_remaining by 1
                    moves_remaining -= 1
                    print(f"{player.name} moved {move}. New position: {player.position}")

                    # Check for room entrance
                    room = board_manager.get_room_at_player(player)     # Checks if player.position is a room entrance listed in board_manager
                    if room:
                        print(f"{player.name} entered the {room}!")
                        self.room_entered(player, room)                 # IF player.position = a room entrance, run room_entered function
                        # End turn after entering room
                        moves_remaining = 0
                else:
                    print("Move invalid. Try a different direction.")   # Player failed movement validation...

            else:
                print("Invalid input. Type 'up/down/left/right'.")      # Player did not enter a valid direction...

        print(f"{player.name}'s turn is over.")                         # Turn over when moves_remaining == 0

    # Function runs upon entering a room
    def room_entered(self, player, room_name):
        print(f"\n{player.name}, you can now make a suggestion or accusation.")
        choice = ""
        while choice not in ["s", "a"]:         # Loops until receiving valid input for a suggestion or accusation
            choice = input("Enter 's' to make a suggestion. Enter 'a' to make your accusation: ").strip().lower()
            print("Invalid input...")

        suspect = input("Select suspect: ").strip()     # Player inputs suspect name for suggestion/accusation
        weapon = input("Select weapon: ").strip()       # Player inputs weapon name for suggestion/accusation
        room = room_name                                # Room guess for suggestion/accusation always equals the room the player entered

        if choice == "a":
            correct = self.game_manager.check_accusation(player, suspect, weapon, room)     # IF player made an accusation, check solution in game_manager (unfinished)
            if not correct:
                print(f"{player.name} is eliminated for making an incorrect accusation!")
        else:
            print(f"{player.name} suggests: {suspect} with the {weapon} in the {room}.")    # ELSE check player suggestion (unfinished)
            print("Suggestion checking not implemented yet...")
