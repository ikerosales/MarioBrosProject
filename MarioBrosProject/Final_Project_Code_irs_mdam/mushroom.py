
from constants import Constants
from interactive_elements import InteractiveElements

class Mushroom(InteractiveElements):
    """
    Class for the red mushroom that transforms mario into super mario
    """
    def __init__(self, x, y, sprite = Constants.MUSHROOM_IMAGE, type = "mushroom"):
        super().__init__(x, y, sprite, type)

        self.sprite_right = Constants.MUSHROOM_IMAGE
        self.sprite_left = Constants.MUSHROOM_IMAGE

        self.direction = "right"
