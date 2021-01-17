import unittest

from player import Player
from enums.directions import Directions

class PlayerTest(unittest.TestCase):

    def test_from_dict(self):
        player_dict = {
            "x": 17,
            "y": 0,
            "direction": "right",
            "speed": 1,
            "active": True
        }

        p = Player.from_dict(player_dict, 1)

        self.assertTrue(p.get_id() == 1)
        self.assertTrue(p.get_x() == 17)
        self.assertTrue(p.get_y() == 0)
        self.assertTrue(p.get_direction() == Directions.RIGHT)
        self.assertTrue(p.get_speed() == 1)

        pos = p.get_pos()
        self.assertTrue(pos[0] == 17 and pos[1] == 0)



    def test_getters(self):
        p = Player(1, 20, 30, Directions(1), 2, True)

        self.assertTrue(p.get_id() == 1)
        self.assertTrue(p.get_x() == 20)
        self.assertTrue(p.get_y() == 30)
        self.assertTrue(p.get_direction() == Directions.RIGHT)
        self.assertTrue(p.get_speed() == 2)

        pos = p.get_pos()
        self.assertTrue(pos[0] == 20 and pos[1] == 30)

        self.assertTrue(p.is_active() == True)
        