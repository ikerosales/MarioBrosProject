
from background_elements.blocks import Blocks
from constants import Constants

class InvisibleBlock(Blocks):
    """
    Class belonging to blocks for the invisible block that contains the green mushroom
    """
    def __init__(self, x: int, y: int, sprite = Constants.INVISIBLE_BLOCK_IMAGE):
        super().__init__(x, y,sprite)
        self.subtype = "invisible_block"
        self.mushroom = True

    @property
    def mushroom(self):
        return self.__mushroom

    @mushroom.setter
    def mushroom(self, mushroom):
        if type(mushroom)!=bool:
            raise TypeError("Only admmitted bool results .(T/F)")
        else:
            self.__mushroom = mushroom


