
class MotherClass:
    """
    This will be the game's main mother class, where we will define the main attributes
    that most objects in our game have
    """
    def __init__(self, x: int, y: int, sprite: tuple, type: str):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.type = type

    def move_with_background(self):
        """
        Almost every object in the game uses this method.
        Thanks to inheritance we do not need to create a method in each class
        """
        self.x -= 2

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if type(x) != int:
            raise TypeError("INTEGER NEEDED TO WORK IN PYXEL")
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if type(y) != int:
            raise TypeError("INTEGER NEEDED TO WORK IN PYXEL")
        else:
            self.__y = y

    @property
    def sprite(self):
         return self.__sprite

    @sprite.setter
    def sprite(self, sprite):
        self.__sprite = sprite

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        possible_types=["coin","enemy","mario","green_mushroom","koopa_troopa_shell","mushroom","speaker","block","background"]
        if type not in possible_types:
            raise ValueError ("The object of Mother Class can only be of type :" + str(possible_types))
        else:
            self.__type = type

    @property
    def width(self):
        return self.sprite[3]

    @property
    def height(self):
        return self.sprite[4]


