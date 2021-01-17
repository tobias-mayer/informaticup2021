import unittest

from game_state import GameState
from player import Player
from enums.directions import Directions

class GameStateTest(unittest.TestCase):

    def test_from_dict(self):
        game_state_dict = {
            "width": 5,
            "height": 3,
            "cells": [
                [0,0,0,0,3],[0,0,1,0,0],[2,0,0,0,0]
            ],
            "players": {
                "1": {
                    "x": 17,
                    "y": 0,
                    "direction": "right",
                    "speed": 1,
                    "active": True
                },
                "2": {
                    "x": 41,
                    "y": 15,
                    "direction": "up",
                    "speed": 1,
                    "active": True
                },
                "3": {
                    "x": 0,
                    "y": 9,
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

        self.assertTrue(gs.get_width() == 5)
        self.assertTrue(gs.get_height() == 3)
        self.assertTrue(gs.get_player().get_id() == 1)
        self.assertTrue(gs.is_running() == True)
        self.assertTrue(len(gs.get_players()) == 3)

    def test_getters(self):
        gs = GameState(4, 4, [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [Player(1, 2, 1, Directions.RIGHT, 1, True)], 1, True, '')

        self.assertTrue(gs.get_width() == 4)
        self.assertTrue(gs.get_height() == 4)
        self.assertTrue(gs.get_player().get_id() == 1)
        self.assertTrue(gs.is_running() == True)
        self.assertTrue(len(gs.get_players()) == 1)
               