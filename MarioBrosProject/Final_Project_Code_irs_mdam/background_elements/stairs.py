
from background_elements.blocks import Blocks
from constants import Constants

class StairBlock(Blocks):
    """
    Class that will contain the blocks that form the stairs, with a specific method to create the stairs
    """
    def __init__(self, x: int, y: int, sprite = Constants.STAIR_BLOCK_IMAGE):
        super().__init__(x, y, sprite)
        self.subtype = "stairs"


    def create_stair(direction: str, x: int, n: int=5, y: int=224):  # direction up or down, x,y bottom left
        """
        Method that we will use to create the stairs as a list of the StairBlocks in the according positions
        """
        stair = []
        base = n  # number of blocks on lower base
        n_base = n
        x_stair = x
        y_stair = y - 16  # height of floor - size block

        for i in range(base):
            for j in range(n_base):
                step = StairBlock(x_stair, y_stair)
                stair.append(step)
                x_stair += 16
            n_base -= 1  # new step height next height one less
            y_stair -= 16
            if direction == "up":
                x_stair = x + (i+1)*16
            else:  # direction == down
                x_stair = x

        return stair

