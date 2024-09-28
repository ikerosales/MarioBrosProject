
from background_elements.blocks import Blocks
from constants import Constants

class Castle(Blocks):
    """
    Class with the sprite that contains Mario's castle
    """
    def __init__(self, x: int, y: int, sprite = Constants.CASTLE_IMAGE_TLMP):
        super().__init__(x, y, sprite)
        self.subtype = "castle"
