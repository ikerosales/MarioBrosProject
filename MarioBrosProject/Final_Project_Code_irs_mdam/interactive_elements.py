
from motherclass import MotherClass

class InteractiveElements(MotherClass):
    """
    this is the main class for the enemies, and mushrooms
    it will be the mother class with the methods that they will share
    """
    def __init__(self, x: int, y: int, sprite=None, type=None):
        super().__init__(x, y, sprite, type)
        self.direction = "left"
        # sprite is the one we will draw
        # we save the sprite positions for the other two to modify when we change direction
        self.sprite_left = None
        self.sprite_right = None
        self.subtype = None


    def move(self, velocity: float=1):
        """
        This method will move the enemies, and mushrooms
        they will move in the same direction until they have hit another object,
        they start moving left
        @param velocity : Tells the velocity the object takes, its initial value is 1
        """

        if self.direction == "left":
            self.x -= int(2*velocity)
            self.direction = "left"
            self.sprite = self.sprite_left

        else: # direction == right
            self.x += int(2*velocity)
            self.direction = "right"
            self.sprite = self.sprite_right
            # print("Enemy moves to the rigth")


    def gravity(self):
        """
        The interactive objects will fall until anything is under them
        """
        self.y += 4
        if self.direction == "right":
            self.sprite = self.sprite_right
        elif self.direction == "left":
            self.sprite = self.sprite_left

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        possible_direction = ["right","left"]
        if direction not in possible_direction:
            raise ValueError("Need a direction of : "+str(possible_direction))
        else:
            self.__direction = direction

    @property
    def sprite_left(self):
        return self.__sprite_left

    @sprite_left.setter
    def sprite_left(self, sprite_left):
        if sprite_left != None:
            if type(sprite_left) != list and len(sprite_left) != 5:
                raise TypeError("Needed a list of 5 terms indicating (img, u, v, w, h)")
            else:
                self.__sprite_left = sprite_left
        self.__sprite_left = sprite_left

    @property
    def sprite_right(self):
        return self.__sprite_right

    @sprite_right.setter
    def sprite_right(self, sprite_right):
        if sprite_right != None:
            if type(sprite_right) != list and len(sprite_right) != 5:
                raise TypeError("Needed a list of 5 terms indicating (img, u, v, w, h)")
            else:
                self.__sprite_right = sprite_right
        self.__sprite_right = sprite_right

    @property
    def subtype(self):
        return self.__subtype

    @subtype.setter
    def subtype(self, subtype):
        subtypes_possible = ["goomba", "koopa_troopa"]
        if subtype != None:
            if subtype not in subtypes_possible:
                raise ValueError("Need a subtype of : "+str(subtypes_possible))
            else:
                self.__subtype = subtype
        else:
            self.__subtype = subtype




