
from background_elements.blocks import Blocks
from constants import Constants

class Block_Floor(Blocks):
    """
    Class of Blocks that contains the blocks that form the floor
    """
    def __init__(self, x: int, y: int, sprite = Constants.FLOOR_BLOCK):
        super().__init__(x, y, sprite)
        self.subtype = "block_floor"

