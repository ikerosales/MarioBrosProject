
from background_elements.blocks import Blocks
from constants import Constants

import random

class QuestionBlock(Blocks):
    """
    Class belonging to blocks for Question blocks, that will contain coins or a red mushroom
    """
    def __init__(self, x: int, y: int, sprite = Constants.QUESTION_BLOCK_IMAGE):
        super().__init__(x, y, sprite)
        self.subtype = "question_block"

        if x == 9*16:
            # the block in that position will contain a mushroom
            self.mushroom = True
            self.coins = 0
        else:
            # the rest will contain coins
            self.mushroom = False
            self.coins = random.randint(1, 6)

    @property
    def mushroom(self):
        return self.__mushroom

    @mushroom.setter
    def mushroom(self, mushroom):
        if type(mushroom) != bool:
            raise TypeError("Only admmitted bool results .(T/F)")
        else:
            self.__mushroom = mushroom

    @property
    def coin(self):
        return self.__coin

    @coin.setter
    def coin(self, coin):
        if type(coin) != int and coin < 0:
            raise TypeError("Only admmitted integers, as coin cannot have decimals")
        else:
            self.__coin = coin



