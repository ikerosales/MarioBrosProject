
from constants import Constants
from motherclass import MotherClass

class MusicIcon(MotherClass):
        """
        Class for the Speaker on the top left of the screen
        """
        # class attribute with the sprite
        sprite = Constants.SPEAKER_ON_IMAGE

        def __init__(self, x, y, sprite = sprite, type = "speaker"):
            super().__init__(x, y, sprite, type)

