from enums.directions import Directions

class Player:

    def __init__(self, player_id, x, y, direction, speed, active):
        self._player_id = player_id
        self._x = x
        self._y = y
        self._direction = direction
        self._speed = speed
        self._active = active

    def get_id(self):
        """Returns the players id

        Returns:
            int: The players id
        """
        return self._player_id

    def get_x(self):
        """Returns the players X position

        Returns:
            int: The players X position
        """
        return self._x

    def get_y(self):
        """Returns the players Y position

        Returns:
            int: The players Y position
        """
        return self._y

    def get_pos(self):
        """Returns the players position

        Returns:
            [int, int]: The players position as an array
        """
        return [self._x, self._y]

    def get_direction(self):
        """Returns the players current direction

        Returns:
            Directions: Players current direction
        """
        return self._direction

    def get_speed(self):
        """Returns the players speed

        Returns:
            int: Players speed
        """
        return self._speed

    def is_active(self):
        """Returns whether the player is still alive

        Returns:
            bool: True if the player is alive, otherwise False
        """
        return self._active

    @staticmethod
    def from_dict(player_as_dict, player_id):
        """Creates and returns a player object from the given dictionary

        Args:
            player_as_dict ([dict]): the player as dictionary
            player_id ([int]): Id of the player

        Returns:
            [Player]: The created Player object
        """
        return Player(
            player_id=player_id,
            x=player_as_dict['x'],
            y=player_as_dict['y'],
            direction=Directions.from_str(player_as_dict['direction']),
            speed=player_as_dict['speed'],
            active=player_as_dict['active']
        )
