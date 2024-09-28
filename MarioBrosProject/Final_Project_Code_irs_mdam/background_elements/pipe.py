
from background_elements.blocks import Blocks
from constants import Constants

class Pipe(Blocks):
    """
    Class of type of block for pipes
    """
    def __init__(self, x: int, y: int, sprite = Constants.PIPE_IMAGE):
        super().__init__(x, y, sprite)
        self.subtype = "pipe"


