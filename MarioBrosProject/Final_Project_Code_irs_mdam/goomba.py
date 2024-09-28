
from interactive_elements import InteractiveElements
from constants import Constants


class Goomba(InteractiveElements):
    """
    This is an interactive class for Goomba
    """
    def __init__(self, x: int, y: int, sprite = Constants.GOOMBA_IMAGE, type="enemy"):
        super().__init__(x, y, sprite, type)

        self.sprite_left = Constants.GOOMBA_IMAGE
        self.sprite_right = Constants.GOOMBA_IMAGE
        self.subtype = "goomba"
