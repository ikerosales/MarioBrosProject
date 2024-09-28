
from motherclass import MotherClass

class Blocks(MotherClass):
    """
    This is the mother class we will use for all type of blocks.
    Although it does not have any methods, we used it as a structure class that controls every subtype of block

    """
    def __init__(self, x: int, y: int,sprite = None,type = "block"):
        super().__init__(x, y, sprite, type)
        self.subtype = None

    @property
    def subtype(self):
        return self.__subtype

    @subtype.setter
    def subtype(self, subtype):
        possible_subtypes=("block_floor","brick_with_coins","breakable_brick","castle","invisible_block","pipe","question_block","stairs")
        if subtype != None:
            if subtype not in possible_subtypes:
                raise ValueError("The subtype of a block must always be :"+str(possible_subtypes))
            else:
                self.__subtype = subtype
        self.__subtype = subtype




