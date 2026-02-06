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
        # Player turn:
        # 1. Roll dice for movement points
        # 2. Allow movement until points run out or player enters room
        # 3. If player enters room, get suggestion or accusation

        # 1. Roll Dice
        moves_remaining = self.roll_dice()      # Calls roll_dice function and sets total to 'moves_remaining'
        print(f"\n--- {player.name} has {moves_remaining} movements.")

        # 2. Movement loop
        while moves_remaining > 0:
            print(f"Moves left: {moves_remaining}")
            move = input("Enter move (up/down/left/right): ").strip().lower()

            if move in ["up", "down", "left", "right"]:
                success = board_manager.move_player(player, move)
                if success:
                    moves_remaining -= 1
                    print(f"{player.name} moved {move}. New position: {player.position}")

                    # Check for room entrance
                    room = board_manager.get_room_at_player(player)
                    if room:
                        print(f"{player.name} entered the {room}!")
                        self.make_suggestion(player, card_manager, room)
                        # End turn after entering room
                        moves_remaining = 0
                else:
                    print("Move invalid. Try a different direction.")

            else:
                print("Invalid input. Type 'up/down/left/right.")

        print(f"{player.name}'s turn is over.")

    def make_suggestion(self, player, card_manager, room):
        # Incomplete, this will be for suggestions or accusations
        print(f"{player.name} can make a suggestion in the {room}. (Incomplete...)")
        # ^ Remove and replace with suggest/accusation function
