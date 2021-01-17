import unittest

from game_state import GameState
from game import Game
from enums.directions import Directions
from enums.commands import Commands

class GameTest(unittest.TestCase):

    def test_is_in_game_bounds(self):
        game_state_dict = {
            "width": 5,
            "height": 3,
            "cells": [
                [0,0,0,0,3],
                [0,0,1,0,0],
                [2,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 0,
                    "y": 2,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                },
                "3": {
                    "x": 0,
                    "y": 4,
                    "direction": "left",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        gs = GameState.from_dict(game_state_dict)
        game = Game(game_state=gs)

        self.assertFalse(game._is_in_game_bounds([0, 4]))
        self.assertFalse(game._is_in_game_bounds([6, 2]))
        self.assertTrue(game._is_in_game_bounds([2, 2]))
        self.assertTrue(game._is_in_game_bounds([2, 1]))

    def test_check_occupied_by_snake(self):
        game_state_dict = {
            "width": 5,
            "height": 3,
            "cells": [
                [0,0,0,0,3],
                [0,0,1,0,0],
                [2,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 0,
                    "y": 2,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                },
                "3": {
                    "x": 0,
                    "y": 4,
                    "direction": "left",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        gs = GameState.from_dict(game_state_dict)
        game = Game(game_state=gs)

        self.assertTrue(game._check_occupied_by_snake([2, 1]))
        self.assertFalse(game._check_occupied_by_snake([0, 0]))

    def test_is_move_six(self):
        game = Game()
        
        game._move_counter = 7
        self.assertFalse(game._is_move_six())

        game._move_counter = 24
        self.assertTrue(game._is_move_six())

    def test_generate_possible_fields(self):
        game = Game()

        square_tl, square_tr, square_sd, square_su, square_cn = game._generate_possible_fields([2, 2], Directions.UP, 1)

        self.assertTrue(square_tl[0] == 1 and square_tl[1] == 2)
        self.assertTrue(square_tr[0] == 3 and square_tr[1] == 2)
        self.assertTrue(square_sd[0] == 2 and square_sd[1] == 2)
        self.assertTrue(square_su[0] == 2 and square_su[1] == 0)
        self.assertTrue(square_cn[0] == 2 and square_cn[1] == 1)

    def test_calculate_path(self):
        game_state_dict = {
            "width": 5,
            "height": 3,
            "cells": [
                [0,0,0,0,3],
                [0,0,1,0,0],
                [2,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 0,
                    "y": 2,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                },
                "3": {
                    "x": 0,
                    "y": 4,
                    "direction": "left",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        gs = GameState.from_dict(game_state_dict)
        game = Game(game_state=gs)

        path = game._calculate_path([0, 4], [0, 0])
        self.assertTrue(len(path) == 1)

        path = game._calculate_path([0, 0], [0, 0])
        self.assertTrue(len(path) == 1)

        game._move_counter = 3
        path = game._calculate_path([0, 0], [0, 2])
        self.assertTrue(len(path) == 3)

        game._move_counter = 6
        path = game._calculate_path([0, 0], [0, 2])
        self.assertTrue(len(path) == 3)

        path = game._calculate_path([0, 1], [2, 3])
        self.assertTrue(len(path) == 1)

        game._move_counter = 3
        path = game._calculate_path([0, 0], [2, 0])
        self.assertTrue(len(path) == 3)

        game._move_counter = 6
        path = game._calculate_path([0, 0], [2, 0])
        self.assertTrue(len(path) == 3)

    def test_calculate_collision_cmds(self):
        game_state_dict = {
            "width": 5,
            "height": 4,
            "cells": [
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,0,2,0],
                [0,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 3,
                    "y": 2,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        game_state = GameState.from_dict(game_state_dict)
        game = Game(game_state=game_state)

        result = game._calculate_collision_cmds([0, 0], Directions.RIGHT, 1, [1, 1], Directions.UP, 1)

        expected_result = [Commands.TURN_LEFT, Commands.TURN_RIGHT, Commands.SPEED_UP, Commands.CHANGE_NOTHING]

        self.assertTrue(set(result) == set(expected_result))

    def test_check_if_reachable(self):
        game_state_dict = {
            "width": 5,
            "height": 4,
            "cells": [
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,0,2,0],
                [0,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 3,
                    "y": 2,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        game_state = GameState.from_dict(game_state_dict)
        game = Game(game_state=game_state)

        result = game._check_if_reachable([2, 1], [4, 1])
        self.assertTrue(result)

        result = game._check_if_reachable([2, 1], [3, 4])
        self.assertFalse(result)

        result = game._check_if_reachable([2, 1], [2, 1])
        self.assertFalse(result)

        result = game._check_if_reachable([2, 1], [2, 3])
        self.assertTrue(result)

    def test_predict_move(self):
        game_state_dict = {
            "width": 5,
            "height": 4,
            "cells": [
                [0,0,0,0,0],
                [1,1,1,2,0],
                [0,0,2,2,0],
                [0,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 3,
                    "y": 1,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        game_state = GameState.from_dict(game_state_dict)
        game = Game()

        predicted_move = game.predict_move(game_state)

        self.assertTrue(predicted_move == Commands.TURN_LEFT)

        game_state_dict = {
            "width": 5,
            "height": 4,
            "cells": [
                [3,3,3,0,0],
                [1,1,1,0,0],
                [0,2,2,2,0],
                [0,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 2,
                    "y": 1,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 1,
                    "y": 2,
                    "direction": "left",
                    "speed": 1,
                    "active": True
                },
                "3": {
                    "x": 2,
                    "y": 0,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                }
            },
            "you": 1,
            "running": True,
            "deadline": "2021-01-04T10: 45: 31Z"
        }

        game_state = GameState.from_dict(game_state_dict)
        game = Game()

        predicted_move = game.predict_move(game_state)

        self.assertTrue(predicted_move == Commands.CHANGE_NOTHING)
