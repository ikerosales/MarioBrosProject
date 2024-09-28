
from constants import Constants
from mario import Mario
from background_elements.blocks import Blocks
from interactive_elements import InteractiveElements
from mushroom import Mushroom
from koopa_troopa_shell import KoopaTroopaShell
from background_elements.castle import Castle

class Collisions():
    """
    this is where we will create methods that we will call on during our program
    which will check the interactions (or collisions) between the different objects of the game
    """

    def nothing_right(self, annimated_object, map_list_objects: list) -> bool:
        """
        checks if there is an object to the annimated object's right to see if
        he can move in that direction
        @param annimated_object : could be Mario, an enemy or any other interactive element
        @param map_list_objects : It is a list used in most of the collision functions that contain a nested list of all the background objects
        @return: a boolean
        """
        nothing_right = True
        for object in map_list_objects:
            for object_2 in range(len(object)):
                if type(object[object_2]) != Castle:
                    if annimated_object.x + annimated_object.width == object[object_2].x and \
                            annimated_object.y + annimated_object.height > object[object_2].y and \
                            annimated_object.y < object[object_2].y + object[object_2].height  and type(annimated_object)!= KoopaTroopaShell:
                        nothing_right = False
                    # Koopa troopa moves at a different velocity
                    elif type(annimated_object) == KoopaTroopaShell  and abs(annimated_object.x + annimated_object.width - object[object_2].x) <= 2 and \
                              annimated_object.y + annimated_object.height > object[object_2].y and \
                              annimated_object.y < object[object_2].y + object[object_2].height and type(object[object_2]) != Castle:
                        nothing_right = False

        return nothing_right


    def nothing_left(self, annimated_object, map_list_objects:list) -> bool:
        """
        checks if there is an object to the annimated object's left to see if
        he can move in that direction.
        @param annimated_object: could be Mario, an enemy or any other interactive element
        @param map_list_objects: It is a list used in most of the collision functions that contain a nested list of all the background objects
        @return: a boolean
        """
        nothing_left = True
        for object in map_list_objects:
            for object_2 in range(len(object)):
                if type(object[object_2]) != Castle:
                    if annimated_object.x == object[object_2].x + object[object_2].width and \
                            annimated_object.y + annimated_object.height > object[object_2].y and \
                            annimated_object.y < object[object_2].y + object[object_2].height and type(object[object_2]) != Castle and type(annimated_object)!= KoopaTroopaShell:
                        nothing_left = False
                    #Koopa troopa moves at a different velocity
                    elif  type(annimated_object) == KoopaTroopaShell and abs(annimated_object.x - object[object_2].x - object[object_2].width) <= 2 and \
                            annimated_object.y + annimated_object.height > object[object_2].y and \
                            annimated_object.y < object[object_2].y + object[object_2].height and type(object[object_2]) != Castle :
                        nothing_left = False

        return nothing_left


    def nothing_down(self, annimated_object, map_lists_objects: list)->bool:
        """
        checks if there is an object underneath the annimated object to see if
        he can move in that direction
        @param annimated_object : could be Mario, an enemy or any other interactive element
        @param map_list_objects : It is a list used in most of the collision functions that contain a nested list of all the background objects
        @return: a boolean
        """
        nothing_down = True
        for list_objects in map_lists_objects:
             for object in range(len(list_objects)):
                 if (annimated_object.x + annimated_object.width > list_objects[object].x and annimated_object.x < list_objects[
                     object].x + list_objects[object].width) \
                        and (annimated_object.y + annimated_object.height == list_objects[object].y) and type(annimated_object) != InteractiveElements:
                     nothing_down = False
                 elif isinstance(annimated_object, InteractiveElements) and (annimated_object.x + annimated_object.width >= list_objects[object].x and annimated_object.x <= list_objects[
                     object].x + list_objects[object].width) \
                        and (annimated_object.y + annimated_object.height == list_objects[object].y):
                     nothing_down = False
        return nothing_down

    def collision_above_object_to_create(self, mario: Mario, list_of_objects:list)->tuple:
        """
        This function will execute when the variable "nothing_up" is False.
        It will get the position of Mario and it will see with which block he is colliding at that moment

        @param mario: Mario
        @param list_of_objects:  It is a list used in most of the collision functions that contain a nested list of all the background objects
        @return: tuple, with the object that needs to be created and it's coordinates
        """

        middle_of_mario_x = mario.x + mario.width//2
        middle_of_blocks_x = []

        for list_object in list_of_objects:
            for object in list_object:
                middle_of_blocks_x.append(object.x + object.sprite[3]//2)

        blocks_y_bottom = []
        for list_object in list_of_objects:
            for object in list_object:
                blocks_y_bottom.append(object.y + object.sprite[4])

        min = abs(middle_of_mario_x - middle_of_blocks_x[0])
        min_index = 0
        for i in range(len(middle_of_blocks_x)):
            if abs(middle_of_mario_x - middle_of_blocks_x[i]) < min and mario.y == blocks_y_bottom[i]:
                min = abs(middle_of_mario_x - middle_of_blocks_x[i])
                min_index = i

        list_objectss=[]
        for list_object in list_of_objects:
            for object in list_object:
                list_objectss.append(object)

        touched_block = list_objectss[min_index]

        object_to_create, object_to_create_x, object_to_create_y = self.block_touched(touched_block, mario)

        return object_to_create, object_to_create_x, object_to_create_y

    def block_touched(self, touched_block: Blocks, mario: Mario) -> tuple:
        """
        Method that will change the necessary atributes of the block touched and
        specify the needed object to create and its coordinates
        @param touched_block: a block
        @param mario : Mario object
        @return: a tuple
        """
        object_to_create = "none"
        object_to_create_x = -16
        object_to_create_y = -16

        if touched_block.subtype == "question_block":

            if touched_block.mushroom == True:
                object_to_create = "mushroom"
                touched_block.mushroom = False
                touched_block.sprite = Constants.CLEAR_BLOCK_IMAGE

            elif touched_block.coins > 0:
                object_to_create = "coin"
                touched_block.coins -= 1

                if touched_block.coins == 0:
                    touched_block.sprite = Constants.CLEAR_BLOCK_IMAGE

        elif touched_block.subtype == "invisible_block":
            if touched_block.mushroom == True:
                object_to_create = "green_mushroom"
                touched_block.mushroom = False
                touched_block.sprite = Constants.CLEAR_BLOCK_IMAGE

        if touched_block.subtype == "brick_with_coins" and mario.subtype == "super":
            # When a block is touched a coin is generated, when there is no coins left the block changes its aspect.
            if touched_block.coins > 0:
                object_to_create = "coin"
                touched_block.coins -= 1
            if touched_block.coins == 0:
                touched_block.sprite = Constants.CLEAR_BLOCK_IMAGE

        if mario.subtype == "super":
            if touched_block.subtype == "breakable_brick":
                # Block is marked to be destroyed in game
                touched_block.keepalive = False

        if object_to_create != "none":
            object_to_create_x = touched_block.x
            object_to_create_y = touched_block.y - 16 # so it appears on top

        return object_to_create, object_to_create_x, object_to_create_y

    def nothing_up(self, annimated_object, map_lists_objects: list) -> bool:
        """
        checks if there is an object above the annimated object to see if
        he can move in that direction
        @param annimated_object : could be Mario, an enemy or any other interactive element
        @param map_list_objects : It is a list used in most of the collision functions that contain a nested list of all the background objects
        @return: a boolean
        """

        nothing_up = True

        for object in map_lists_objects:
            for object_2 in range(len(object)):
                if annimated_object.x + annimated_object.sprite[3] > object[object_2].x and \
                annimated_object.x < object[object_2].x + object[object_2].sprite[3] and \
                annimated_object.y == object[object_2].y + object[object_2].sprite[4]:
                    nothing_up = False

        return nothing_up

    def mario_jump_on_enemy(self, mario: Mario, enemy: InteractiveElements) -> tuple:
        """
        Checks if Mario has jumped on top of an enemy
        @param annimated_object : could be Mario, an enemy or any other interactive element
        @param enemy : an interactive object
        @return: a tuple
        """
        mario_on_enemy = False
        collision_x = None
        collision_y = None

        if (mario.x + mario.width >= enemy.x and mario.x <= enemy.x + enemy.width) \
                and abs(mario.y + mario.height - enemy.y) <= 2:
            mario_on_enemy = True
            collision_x = enemy.x
            collision_y = enemy.y + 25

        return mario_on_enemy, collision_x, collision_y

    def collision_with_object(self, annimated_object:InteractiveElements, second_object:InteractiveElements)->bool:
        """
        Checks whether mario, or a koopa troopa shell in movement, and an enemy have come into contact
        @param annimated_object An annimated_object
        @param second_object An other annimated_object
        @return: a bool
        """
        collision = False

        if (abs(annimated_object.x - second_object.x) <= 18) and (
                annimated_object.y + annimated_object.height > second_object.y) and \
                abs(annimated_object.y - second_object.y + second_object.height) <= annimated_object.height:
            collision = True

        # I keep the subtype="super" I will be used to save a live and continue
        if type(annimated_object)==Mario:
            if collision == True and annimated_object.subtype == "super":
                if annimated_object.direction == "right":
                    annimated_object.sprite = Constants.MARIO_RIGTH
                else:  # mario.direction == "left":
                    annimated_object.sprite = Constants.MARIO_LEFT

        return collision


    def collision_mario_mushroom(self,mario: Mario, mushroon: Mushroom)->bool:
        """
        checks whether mario and the mushroom have come into contact,
        and if it is a red mushroom turns Mario into SuperMario
        @param mario : Mario
        @param mushroon : a green or red Mushroom
        @return: a boolean
        """
        collision = False
        # we check collision
        if ((abs(mario.x - mushroon.x) < mario.width) and (abs(mario.y - mushroon.y) < mario.height)):
               collision = True

        # if it was a red mushroom we change Mario's attributes to transform him into SuperMario
        if collision == True and mushroon.type == "mushroom":
            mario.y -= 16
            # we change the sprites
            if mario.direction == "right":
                if mario.x == 208:
                    mario.sprite = Constants.SUPER_MARIO_RIGTH
                else:
                    mario.sprite = Constants.SUPER_MARIO_RIGTH_JUMP

            else: # mario.direction == "left":
                if mario.x == 208:
                    mario.sprite = Constants.SUPER_MARIO_LEFT
                else:
                    mario.sprite = Constants.SUPER_MARIO_LEFT_JUMP

            mario.type = "mario"
            mario.subtype = "super"

        return collision

    def collision_mario_shell_static(self, mario: Mario, shell: KoopaTroopaShell)->str:
        """
        Checks collisions between Mario and koopa_troopa shell when it is in static form
        @param mario Mario
        @param shell a KoopaTroopaShell
        @return: a string
        """
        if abs(mario.x + 16 - shell.x) <= 3 and abs(mario.y - shell.y) <= mario.height or (mario.y + mario.height == shell.y
                                                                          and mario.x + 16 > shell.x and mario.x < shell.x + 16):
            return "right"
        elif mario.x == shell.x + 16 and abs(mario.y - shell.y) <= mario.height:
            return "left"
        else:
            return "static"

