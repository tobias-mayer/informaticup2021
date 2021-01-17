from enum import Enum

class Directions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def from_str(label):
        if label == 'up':
            return Directions.UP
        elif label == 'right':
            return Directions.RIGHT
        if label == 'down':
            return Directions.DOWN
        elif label == 'left':
            return Directions.LEFT
        else:
            raise NotImplementedError