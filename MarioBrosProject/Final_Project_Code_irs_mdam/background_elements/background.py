
from constants import Constants
from motherclass import MotherClass

class Background(MotherClass):
    """
    Mother class for the background tilemap, that will contain the bushes mountain and clouds of the background
    """
    def __init__(self, x: int, y: int, sprite=Constants.BUSHES_CLOUDS_MOUNTAINS_TILEMAP, type="background"):
        super().__init__(x, y, sprite, type)


