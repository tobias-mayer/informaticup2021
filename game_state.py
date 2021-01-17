from player import Player
from enums.textures import Textures

class GameState:

    def __init__(self, width, height, cells, players, you, running, deadline):
        self._width = width
        self._height = height
        self._cells = cells
        self._players = players
        self._you = you
        self._running = running
        self._deadline = deadline

    def get_width(self):
        """Returns the width of the playing field

        Returns:
            int: The width
        """
        return self._width

    def get_height(self):
        """Returns the height of the playing field

        Returns:
            int: The height
        """
        return self._height

    def get_cells(self):
        """Returns the cells of the playing field as an two dimensional array of Textures

        Returns:
            2d array: The cells of the game with the dimension height * width
        """
        return self._cells

    def get_players(self):
        """Returns a list of all players in the current game

        Returns:
            array: Array of Player objects
        """
        return self._players

    def get_player(self):
        """Returns the player object which the program is controlling

        Returns:
            Player: The player object, None if the player was not found
        """
        for player in self.get_players():
            if player.get_id() == self._you:
                return player
        return None

    def is_running(self):
        """Returns whether the game is still running

        Returns:
            bool: True if the game is running, otherwise False
        """
        return self._running

    def get_you(self):
        """Returns the players id

        Returns:
            int: Player Id
        """
        return self._you

    @staticmethod
    def from_dict(game_state_as_dict):
        """Creates and returns a GameState object from the given dictionary

        Args:
            game_state_as_dict ([dict]): the game state as dictionary

        Returns:
            [GameState]: The created GameState object
        """

        players = []
        players_dict = game_state_as_dict['players']
        for _, (key, value) in enumerate(players_dict.items()):
            players.append(Player.from_dict(value, int(key)))

        deadline = game_state_as_dict['deadline'] if 'deadline' in game_state_as_dict else ''

        return GameState(
            width=game_state_as_dict['width'],
            height=game_state_as_dict['height'],
            cells=[[Textures(x) for x in y] for y in game_state_as_dict['cells']],
            players=players,
            you=game_state_as_dict['you'],
            running=game_state_as_dict['running'],
            deadline=deadline
        )
        