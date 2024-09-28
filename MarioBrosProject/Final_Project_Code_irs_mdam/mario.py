
from constants import Constants
from motherclass import MotherClass

class Mario(MotherClass):

    """
    This is the class for Mario where we will create it's specific methods
    """
    def __init__(self, x: int, y: int, sprite=Constants.MARIO_RIGTH, type = "mario"):
        super().__init__(x, y, sprite, type)

        self.direction = "right"
        self.subtype = "normal"
        self.counter = 0 # for the jump


    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self,direction):
        possible_direction = ["right", "left"]
        if direction not in possible_direction:
            raise ValueError("Need a direction of : " + str(possible_direction))
        else:
            self.__direction = direction

    @property
    def counter(self):
        return self.__counter

    @counter.setter
    def counter(self, counter):
        if counter < 0:
            raise ValueError("MARIO COUNTER CAN NOT BE SMALLER THAN 0")
        else:
            self.__counter = counter


    def move(self, direction: str):
        """
        Method that moves Mario
        According to the direction it will also change the animation and the sprite
        :param direction: right or left
        :param size: size of the screen board
        """

        if direction == "right":
            self.x += 2
            self.direction = "right"
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_RIGTH
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_RIGTH

        elif direction == "left" and self.x > 5:
            self.x -= 2
            self.direction = "left"
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_LEFT
            else: # super mario
                self.sprite = (0, 16, 112, 16, 32)
                self.sprite = Constants.SUPER_MARIO_LEFT



    def jump(self):
        """
        It will move mario upwards counting how high he has jumped, changing self.counter
        to later fall
        It also changes the sprite to add animation
        """
        self.y -= 8
        self.counter += 1

        # it also changes the sprite accordingly
        if self.direction == "right":
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_RIGTH_JUMP
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_RIGTH_JUMP
        else:
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_LEFT_JUMP
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_LEFT_JUMP


    def rebound(self):
        """
        Method that makes mario do a small jump when he has jumped on top of an enemy
        """
        self.y -= 8
        self.counter += 1



    def gravity(self):
        """
        After jumping Mario will start falling again, calling this method
        """
        self.y += 4

        # we also update the sprite
        if self.direction == "right":
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_RIGTH_JUMP
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_RIGTH_JUMP
        else:
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_LEFT_JUMP
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_LEFT_JUMP

    def orientation(self):
        """
        changes Mario's sprite according to the direction
        """
        if self.direction == "right":
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_RIGTH
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_RIGTH
        else:
            if self.subtype == "normal":
                self.sprite = Constants.MARIO_LEFT
            else: # super mario
                self.sprite = Constants.SUPER_MARIO_LEFT


