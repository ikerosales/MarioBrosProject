
from interactive_elements import InteractiveElements
from constants import Constants


class KoopaTroopa(InteractiveElements):
    """
    This is an enemies class for the Koopa Troopas
    """
    def __init__(self, x: int, y: int, sprite = Constants.KOOPA_TROOPA_LEFT_IMAGE,type="enemy"):
        super().__init__(x, y, sprite, type)
        self.sprite_left = Constants.KOOPA_TROOPA_LEFT_IMAGE
        self.sprite_right = Constants.KOOPA_TROOPA_RIGHT_IMAGE

        self.subtype = "koopa_troopa"
