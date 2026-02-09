class BoardManager:
    def __init__(self, players):                    # Initialization function
        self.players = players
        self.grid_size = 12                         # Used for movement validation
        self.room_entrances = {                     # List of room entrance positions paired to the room they represent
            39: "Kitchen",
            46: "Living Room",
            99: "Bedroom",
            106: "Bathroom"
            }

        # List of room boundaries on board. Player should be unable to enter these positions as they represent a wall
        self.room_walls = [25, 26, 27, 37, 38, 49, 50, 51, 34, 35, 36, 47, 48, 58, 59, 60, 85, 86, 87, 97, 98, 109, 110, 111, 94, 95, 96, 107, 108, 118, 119, 120]

        self.start_positions = [1, 12, 133, 144]    # Player starting positions

        for i, player in enumerate(players):        # Loop places each player in their starting position
            player.position = self.start_positions[i]

    # Player movement function
    def move_player(self, player, direction):
        new_position = player.position

        # Movement validations 
        if direction == "up":
            if player.position > self.grid_size:    # IF player is NOT in top row...
                new_position -= self.grid_size      # allow player to move up 1 square
            else:                                   # ELSE movement is invalid
                return False
        elif direction == "down":
            if player.position <= self.grid_size * (self.grid_size - 1):    # IF player is NOT in bottom row...
                new_position += self.grid_size                              # allow player to move down 1 square
            else:                                                           # ELSE movement is invalid
                return False
        elif direction == "left":
            if (player.position - 1) % self.grid_size != 0:                 # IF player is NOT in left column...
                new_position -= 1                                           # allow player to move left 1 square
            else:                                                           # ELSE movement is invalid
                return False
        elif direction == "right":
            if player.position % self.grid_size != 0:                       # IF player is NOT in right column...
                new_position += 1                                           # allow player to move right 1 square
            else:                                                           # ELSE movement is invalid
                return False
        else:
            return False                            # Player did not enter a valid direction... movement is invalid

        if new_position in self.room_walls:         # IF player moves into a position located in 'room_walls' list, movement is invalid
            return False

        player.position = new_position              # Movement is valid, update player.position
        return True

    # Function retrieves the name of the room at player.position
    def get_room_at_player(self, player):
        return self.room_entrances.get(player.position, None)
