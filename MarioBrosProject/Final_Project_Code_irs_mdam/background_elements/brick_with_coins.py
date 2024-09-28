
from background_elements.blocks import Blocks
from constants import Constants

import random

class BrickWithCoins(Blocks):
    """
    Class belonging to blocks for the bricks with coins blocks
    """
    def __init__(self, x: int, y: int, sprite = Constants.BRICK_WITH_COINS_IMAGE):
        super().__init__(x, y, sprite)
        self.subtype = "brick_with_coins"
        # number of coins it will contain
        self.coins = random.randint(1, 4)

    @property
    def coin(self):
        return self.__coin

    @coin.setter
    def coin(self, coin):
        if type(coin) != int and coin < 0:
            raise TypeError("Only admmitted integers, as coin cannot have decimals")
        else:
            self.__coin = coin