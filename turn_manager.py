import random                   # For random dice rolls

# TurnManager runs the actions a player can take on their turn
class TurnManager:
    # Initializer function
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.moves_remaining = 0
        self.current_player = None

    # Dice rolling function
    def roll_dice(self) -> int:
        roll1 = random.randint(1,6)
        roll2 = random.randint(1,6)
        total = roll1 + roll2
        return total

    # Sets player allowed movement using the dice roll function
    def start_turn(self, player):
        
        self.moves_remaining = self.roll_dice()
        return self.moves_remaining

    # Returns remaining moves for player's turn
    def get_moves_remaining(self):
        return self.moves_remaining

    # Player movement check - runs move_player from board_manager and returns true if movement successful
    def move_player(self, player, direction, board_manager) -> bool:
        return board_manager.move_player(player, direction)

    # Checks suggestions/accusations upon entering a room
    def room_entered(self, player, action, suspect, weapon, room):
        
        # debug lines...
        #print("Player param:", player, player.name)
        #print("TurnManager current_player:", self.current_player, getattr(self.current_player, 'name', None))

        # Possible results to be returned to game manager, ex: IF result = "game_over" return False
        result = {
            "game_over": False,
            "eliminated": False,
            "card_shown": None,
            "correct_accusation": None
            }

        # IF player chooses accusation upon entering a room...
        if action == "accusation":
                # Verify accusation using game manager, use value of 'correct' to set 'result'
                correct = self.game_manager.check_accusation(player, suspect, weapon, room)
                result["game_over"] = self.game_manager.game_over
                result["eliminated"] = not correct
                result["correct_accusation"] = correct

        # ELSE IF player chooses suggestion upon entering a room...
        elif action == "suggestion":
            # Check player hands for a card that matches the suggestion using game manager, return result
            shown_card = self.game_manager.check_suggestion(player, suspect, weapon, room)
            result["card_shown"] = shown_card

        return result

    
