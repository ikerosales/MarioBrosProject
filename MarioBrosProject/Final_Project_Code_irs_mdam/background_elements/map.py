import pyxel

from background_elements.block_floor import Block_Floor
from background_elements.pipe import Pipe
from background_elements.stairs import StairBlock
from background_elements.breakable_brick import BreakableBrick
from background_elements.brick_with_coins import  BrickWithCoins
from background_elements.question_block import QuestionBlock
from background_elements.invisible_block import InvisibleBlock
from background_elements.castle import Castle
from constants import Constants


class Map:
    """
    This class we will create all of the elements that will belong to the map:
    pipes, blocks, stairs...
    It will also have the methods move and draw that will be in charge of what appears on the screen regarding these elements
    """
    def __init__(self):
        self.width = Constants.LENGTH_OF_MAP

        # list that will contain all the lists of the different objects
        self.map_lists_objects = []

        # we will create lists with the different objects of each type that form the map

        hole_floor_positions = [64, 65, 66, 67, 97, 98, 128, 129, 130]
        self.blocks_floor = []
        for block_number in range(Constants.LENGTH_OF_MAP // 16):
            if block_number not in hole_floor_positions:
                block_floor1 = Block_Floor(block_number * 16, Constants.HEIGHT_OF_MAP - 16)
                self.blocks_floor.append(block_floor1)
                block_floor2 = Block_Floor(block_number * 16, Constants.HEIGHT_OF_MAP - 16 * 2)
                self.blocks_floor.append(block_floor2)

        self.map_lists_objects.append(self.blocks_floor)

        # we will create lists with the different objects of each type that form the map
        self.pipes = []
        pipes_x_position = [12, 32, 40, 48, 110]
        for i in range(len(pipes_x_position)):
            pipes_x_position[i] *= 16
        pipes_y_position = Constants.HEIGHT_OF_MAP - 16 * 4  # two blocks of the floor, 32 height
        for j in pipes_x_position:
            pipe = Pipe(j, pipes_y_position)
            self.pipes.append(pipe)

        self.map_lists_objects.append(self.pipes)

        self.stair_up1 = StairBlock.create_stair("up", 59 * 16)
        self.stair_up2 = StairBlock.create_stair("up", 75 * 16, 4)
        self.stair_down1 = StairBlock.create_stair("down", 83 * 16, 4)
        self.stair_up3 = StairBlock.create_stair("up", 123 * 16)
        self.stair_down2 = StairBlock.create_stair("down", 131 * 16)
        self.stair_up4 = StairBlock.create_stair("up", 141 * 16)

        self.stairs = [self.stair_up1, self.stair_up2, self.stair_down1, self.stair_up3, self.stair_up4, self.stair_down2]
        for stair in self.stairs:
            self.map_lists_objects.append(stair)

        # there are two heights of blocks in the air
        height_2 = 16*6
        height_1 = 16*10

        # breakable bricks
        self.breackable_bricks = []

        # brick with coins
        self.bricks_with_coins = []

        # question blocks
        self.question_blocks = []

        # we fill in the second height first

        breakable_brick_x_positions_height2 = [22, 23, 24, 25, 26, 68, 69, 70]

        for x in breakable_brick_x_positions_height2:
            breakable_brick = BreakableBrick(x*16, height_2)
            self.breackable_bricks.append(breakable_brick)

        brick_with_coins_x_position_height2 = [27]

        for x in brick_with_coins_x_position_height2:
            brick_coins = BrickWithCoins(x*16, height_2)
            self.bricks_with_coins.append(brick_coins)

        question_block_x_position_height2 = [8, 105]

        for x in question_block_x_position_height2:
            question_block = QuestionBlock(x*16, height_2)
            self.question_blocks.append(question_block)

        # now we fill the first height

        breakable_brick_x_positions_height1 = [6, 8, 18, 25, 27, 45, 52, 54, 94, 116, 118, 138]

        for x in breakable_brick_x_positions_height1:
            breakable_brick = BreakableBrick(x*16, height_1)
            self.breackable_bricks.append(breakable_brick)

        self.map_lists_objects.append(self.breackable_bricks)

        brick_with_coins_x_position_height1 = [4, 20, 44, 92, 93]

        for x in brick_with_coins_x_position_height1:
            brick_coins = BrickWithCoins(x*16, height_1)
            self.bricks_with_coins.append(brick_coins)

        self.map_lists_objects.append(self.bricks_with_coins)

        question_block_x_position_height1 = [7, 9, 19, 26, 53, 103, 107, 117, 139]

        for x in question_block_x_position_height1:
            question_block = QuestionBlock(x*16, height_1)
            self.question_blocks.append(question_block)

        self.map_lists_objects.append(self.question_blocks)

        self.invisible_blocks = []
        invisible_block = InvisibleBlock(36*16, height_1)
        self.invisible_blocks.append(invisible_block)

        self.map_lists_objects.append(self.invisible_blocks)


        self.castle = [Castle(Constants.NUMBER_OF_SCREENS * Constants.WIDTH_SCREEN - Constants.CASTLE_IMAGE_TLMP_WIDTH, 120)]
        self.map_lists_objects.append(self.castle)


    def move_map(self):
        """
        Method that will move all the elements of the map, when Mario is in the middle of the screen
        """

        for list in self.map_lists_objects:
            for object in list:
                object.move_with_background()



    def draw(self):
        """
        Method we will call from the game to draw all the map
        """
        for list in self.map_lists_objects:
            for object in list:
                if type(object) == InvisibleBlock:
                    pyxel.blt(object.x, object.y, *object.sprite)
                elif type(object) == Castle:
                    pyxel.bltm(object.x, object.y, *object.sprite, colkey=6)
                else:
                    pyxel.blt(object.x, object.y, *object.sprite, )

