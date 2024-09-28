
from constants import Constants
from motherclass import MotherClass

class KoopaTroopaShell(MotherClass):
    """
    class for koopa troopas state after being killed by mario
    turns into a shell
    """
    def __init__(self, x: int, y: int,direction: str, sprite = Constants.KOOPA_TROOPA_SHELL_IMAGE, type = "koopa_troopa_shell"):
        self.direction = direction
        super().__init__(x, y, sprite, type)

    def move(self,velocity=3):
        """
        Mehtod that moves the shell at a default speed of 3
        """
        if self.direction == "right":
            self.x += 2*velocity
        elif self.direction == "left":
            self.x -= 2*velocity

    def gravity(self):
        """
        Gracity method for the shell so it falls
        """
        self.y += 4