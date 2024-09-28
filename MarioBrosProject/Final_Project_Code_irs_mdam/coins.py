
import time

from constants import Constants
from motherclass import MotherClass

class Coin(MotherClass):
    """
    Class for coins creation
    """
    # class attribute with the sprite
    sprite = Constants.COINS_IMAGE

    def __init__(self, x: int, y: int, sprite = sprite, type = "coin"):
        super().__init__(x, y, sprite, type)
        self.time_created = time.time()


