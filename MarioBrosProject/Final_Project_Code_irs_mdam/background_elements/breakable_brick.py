
from background_elements.blocks import Blocks
from constants import Constants

class BreakableBrick(Blocks):
    """
    Class belonging to blocks for the breakable blocks
    """
    def __init__(self, x: int, y: int, sprite = Constants.BREAKABLE_BRICK_IMAGE):
        super().__init__(x, y, sprite)
        self.subtype = "breakable_brick"
        # attribute to know if it was hit by super mario and needs to be destroyed
        self.keepalive = True

    @property
    def keepalive(self):
        return self.__keepalive

    @keepalive.setter
    def keepalive(self, keepalive):
        if type(keepalive) != bool:
            raise TypeError("Only admits bool results .(T/F)")
        else:
            self.__keepalive = keepalive




