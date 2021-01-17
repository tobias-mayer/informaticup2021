from enum import Enum

class Commands(Enum):
    TURN_LEFT = 0
    TURN_RIGHT = 1
    SLOW_DOWN = 2
    SPEED_UP = 3
    CHANGE_NOTHING = 4

    def __str__(self):
        if self == Commands.TURN_LEFT:
            return 'turn_left'
        elif self == Commands.TURN_RIGHT:
            return 'turn_right'
        elif self == Commands.SLOW_DOWN:
            return 'slow_down'
        elif self == Commands.SPEED_UP:
            return 'speed_up'
        elif self == Commands.CHANGE_NOTHING:
            return 'change_nothing'
        else:
            raise NotImplementedError

