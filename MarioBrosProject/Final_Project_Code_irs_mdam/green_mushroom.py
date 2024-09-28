
from constants import Constants
from interactive_elements import InteractiveElements

class GreenMushroom(InteractiveElements):
    """
    This is a subclass of interactive enemies that will create the green mushroom
    """
    def __init__(self, x: int, y: int , sprite = Constants.MUSHROOM_GREEN_IMAGE, type = "green_mushroom"):
        super().__init__(x, y, sprite, type)
        self.sprite_right = Constants.MUSHROOM_GREEN_IMAGE
        self.sprite_left = Constants.MUSHROOM_GREEN_IMAGE
        self.direction = "right"

