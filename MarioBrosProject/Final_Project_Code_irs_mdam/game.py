
import time
import pyxel
import random

from mario import Mario
from background_elements.background import Background
from numbers import Number
from coins import Coin
from background_elements.map import Map
from collisions import Collisions
from goomba import Goomba
from koopa_troopa import KoopaTroopa
from constants import Constants
from mushroom import Mushroom
from green_mushroom import GreenMushroom
from music_icon import MusicIcon
from koopa_troopa_shell import KoopaTroopaShell


class Game:
    """
    Main class that will initialize the game and control all the objects from the different classes
    It will have the pyxel update and draw, necessary to keep the game in a loop
    """
    def __init__(self, width: int = 256, height: int = 256, caption:str = "MarioBros"):

        # we initialize the values we need for the size of the game for pyxel
        self.width = width
        self.height = height
        self.caption = caption

        # we position Mario at the starting point
        self.mario = Mario(20, 208)
        # For SuperMario
        self.touched_one_time = False

        # number of lives
        self.lives = 3

        # we create the map which will have all the elements of the map
        self.map = Map()

        # We initialize the values for the timer, coins and score that appear at the top of the screen
        self.user_interface()

        # initial score
        self.score = 0

        # we set the words that appear for time score and lives
        self.time_image = Constants.TIME_IMAGE
        self.score_image = Constants.SCORE_IMAGE
        self.lives_image = Constants.LIVES_IMAGE
        self.testing_game_image = Constants.TESTING_GAME_IMAGE

        # the elements of the backgournd, bushes mountains and the clouds
        self.bushesmountains = Background(0, 0)

        # we initialize the parameters we will need in our game
        self.initiate_jump = False
        self.middle = False
        self.frame_counter = 0

        # we create the list where we will store the enemies
        self.enemies = []
        self.enemy_produced = False
        # enemy killed, True or False, coordinate x and coordinate y, where they where killed
        self.enemy_killed = [False, None, None]
        # koopa troopa shells
        self.shells = []

        # we initialize the object collisions that will check the rest of the objects interactions
        self.collisions = Collisions()

        # other objects are mushrooms coins
        self.other_objects = []

        # attributes that control the game
        self.restart = False
        self.game_over = False
        self.win = False
        self.start_game = False

        self.play_music = True

        # Now we initialize the game
        pyxel.init(self.width, self.height, caption=self.caption, scale=2)
        pyxel.load("resources.pyxres")

        # This part has to go after the pyxel.init and pyxel.load
        # it will start the music
        self.speaker_symbol = Constants.SPEAKER_ON_IMAGE
        if self.play_music:
            self.music_icon = MusicIcon(1, 1)
            pyxel.playm(Constants.BACKGROUND_MUSIC, loop=False)

        # If the following variable is true the enemies do not affect mario
        # set variables for testing, you can change it by pressing the key T
        self.testing_the_game = False

        # Now we run the game
        pyxel.run(self.update, self.draw)



    def update(self):
        '''
        This function is executed every frame.
        It ckecks if the usser's interaction with the keyboard to update the game
        '''

        if self.start_game == False:
            Game.game_screens(self, types="starting")
            if pyxel.btn(pyxel.KEY_ENTER):
                self.start_game = True
        else:
            # A new frame has been executed
            self.frame_counter += 1

            # we check if the player wants to finish the game
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

            # we change the values of the time numbers when another second has passed
            if (time.time() - self.time) >= 1:
                Number.change_value_time(self.unit_time, self.tenths_time, self.hundredths_time)
                self.time = time.time()  # we reset the time so as to check if a second has passed

            # we check if Mario is in the middle of the screen
            middle_of_the_screen = Constants.MIDDLE_OF_SCREEN - self.mario.width
            if self.mario.x >= middle_of_the_screen:
                middle = True
            else:
                middle = False

            # we check if Mario has reached the end of the game, so he can advance and reach the castle
            if (self.map.castle[0].x <= (Constants.WIDTH_SCREEN - Constants.CASTLE_IMAGE_TLMP_WIDTH)):
                middle = False

            # we remove objects that are out of the screen
            self.clean_up()

            # M-KEY controls the music start-stop music
            if pyxel.btnr(pyxel.KEY_M):
                self.stop_start_music()

            # R-KEY Restart the Game
            if pyxel.btn(pyxel.KEY_R):
                self.restart = True

            # T-KEY set up testing mode of the Game
            if pyxel.btn(pyxel.KEY_T):
                self.testing_the_game = True


            # movement
            if pyxel.btn(pyxel.KEY_RIGHT):

                # we look at whether there is something in the way and whether he has reached the middle of the screen
                nothing_right = self.collisions.nothing_right(self.mario, self.map.map_lists_objects)

                if nothing_right and middle == False:
                    # Mario can move to the right
                    self.mario.move("right")

                elif nothing_right and middle == True:
                    # everything but Mario moves to the left
                    self.bushesmountains.move_with_background()
                    self.map.move_map()

                    for enemy in self.enemies:
                        enemy.move_with_background()
                    for other_object in self.other_objects:
                        other_object.move_with_background()
                    for shell in self.shells:
                        shell.move_with_background()

                # else there is something blocking his way so nothing moves
                else:
                    self.collision_music(Constants.MARIO_COLLISION_MUSIC)


            if pyxel.btn(pyxel.KEY_LEFT):
                nothing_left = self.collisions.nothing_left(self.mario, self.map.map_lists_objects)
                if nothing_left:
                    self.mario.move("left")

                # else there is something blocking his way so Mario can't move left
                else:
                    self.collision_music(Constants.MARIO_COLLISION_MUSIC)

            # we check that Mario is on the ground or on an object
            nothing_down = self.collisions.nothing_down(self.mario, self.map.map_lists_objects)

            # gravity for mario
            if nothing_down and self.initiate_jump == False:
                self.mario.gravity()

            # orientation of mario on the floor
            if not nothing_down:
                self.mario.orientation()

            # jump
            i_am_standing_on_something = False
            if not nothing_down:
                i_am_standing_on_something = True

            if pyxel.btn(pyxel.KEY_UP) and i_am_standing_on_something:
                self.initiate_jump = True

            # if there is a collision above with a block, a new object needs to be created
            object_to_create = "none"
            object_to_create_x = -16
            object_to_create_y = -16

            if self.initiate_jump:
                # we check that Mario can move up
                nothing_up = self.collisions.nothing_up(self.mario, self.map.map_lists_objects)

                if nothing_up:
                    self.mario.jump()
                    self.collision_music(Constants.MARIO_JUMP_MUSIC)

                elif not nothing_up:
                    # depending on the block Mario has hit a new object may need to be created
                    object_to_create, object_to_create_x, object_to_create_y \
                        = self.collisions.collision_above_object_to_create(self.mario, self.map.map_lists_objects)
                    if object_to_create == "none":
                        # if it was just a normal collision the collision music plays and no object is created
                        self.collision_music(Constants.MARIO_COLLISION_MUSIC)

                # If the key is pressed, Mario can only do 8 consecutive increments
                if self.mario.counter % 9 == 0 or nothing_up == False:
                     self.initiate_jump = False
                     self.mario.counter = 0

                if pyxel.btnr(pyxel.KEY_UP):
                    self.initiate_jump = False
                    self.mario.counter = 0

            # now depending on the previous collisions we create the new objects
            # and play their music

            if object_to_create == "mushroom":
               mushroom = Mushroom(object_to_create_x, object_to_create_y)
               self.collision_music(Constants.MUSHROOM_MUSIC)
               self.other_objects.append(mushroom)

            elif object_to_create == "green_mushroom":
                green_mushroom = GreenMushroom(object_to_create_x, object_to_create_y)
                self.collision_music(Constants.MUSHROOM_MUSIC)
                self.other_objects.append(green_mushroom)

            elif object_to_create == "coin":
                coin = Coin(object_to_create_x, object_to_create_y)
                self.other_objects.append(coin)
                self.collision_music(Constants.COINS_MUSIC)
                # in the case for the coins we update the score and the value on the screen
                self.score += Constants.COIN_SCORE
                Number.change_value_coin_counter(self.unit_coins,self.tenths_coins)

            for object in self.other_objects:
                if object.type == "coin":
                    time_now = time.time()
                    if abs(time_now - object.time_created) > 1:
                        # we destroy the coins once they have been on the screen for 1 second
                        self.other_objects.remove(object)

            # Mushroom
            for mushroom in self.other_objects:
                if mushroom.type == "mushroom" or mushroom.type == "green_mushroom":
                    # since the mushrooms also move we have to take into account their movement and collisions

                    if mushroom.direction == "left":
                        nothing_left_mushroom = self.collisions.nothing_left(mushroom, self.map.map_lists_objects)
                        if nothing_left_mushroom == False:
                            mushroom.direction = "right"

                    else:  # mushroom.direction == "right"
                        nothing_right_mushroom = self.collisions.nothing_right(mushroom, self.map.map_lists_objects)
                        if nothing_right_mushroom == False:
                            mushroom.direction = "left"

                    # if they are not on top of something or the floor they will fall
                    nothing_down_mushroom = self.collisions.nothing_down(mushroom, self.map.map_lists_objects)
                    if nothing_down_mushroom:
                        mushroom.gravity()

                    # moving mushroom
                    mushroom.move(velocity=1/2)

                # now we check their interactions with Mario
                collision_mario_mushroom = self.collisions.collision_mario_mushroom(self.mario, mushroom)
                if collision_mario_mushroom:
                    if mushroom.type == "green_mushroom":
                        # we add a life and update the score
                        self.lives += 1
                        self.score += Constants.GREEN_MUSSROOM_SCORE
                    else:
                        # otherwise we just update the score since the method collision_mario_mushroom
                        # will change Mario's form to SuperMario
                        self.score += Constants.RED_MUSSROOM_SCORE

                    # we play the music when Mario has taken the mushroom
                    self.collision_music(Constants.MUSHROOM_MUSIC)
                    # and we remove it
                    self.other_objects.remove(mushroom)


            # rebound if an enemy is touched from above
            nothing_up = self.collisions.nothing_up(self.mario, self.map.map_lists_objects)
            if self.enemy_killed[0] and nothing_up:
                self.mario.rebound()
            if self.enemy_killed[0] and self.mario.counter % 3 == 0:
                self.enemy_killed = [False, None, None]
                self.mario.counter = 0

            #### Enemies

            # creating new enemies

            # When the castle appears no more enemies will be created.
            if self.map.castle[0].x > 200:
                # according to the random
                if self.frame_counter % random.randint(140, 160) == 0 and len(self.enemies) < 4 and self.enemy_produced == False:
                    # we choose the type randomly
                    n = random.randint(1, 4)

                    # they will appear on the right side of the screen and in the air, where they will fall on an object
                    if n == 1:
                        enemy = KoopaTroopa(280, 80)
                    else:
                        enemy = Goomba(280, 80)

                    self.enemies.append(enemy)

            if pyxel.frame_count % 100 == 0 and self.enemy_produced:
                self.enemy_produced = False

            # checking movement for enemies and their collisions
            for enemy in self.enemies:

                if enemy.direction == "left":
                    nothing_left_enemy = self.collisions.nothing_left(enemy, self.map.map_lists_objects)

                    if nothing_left_enemy == False:
                        enemy.direction = "right"

                else:  # enemy.direction == "right"
                    nothing_right_enemy = self.collisions.nothing_right(enemy, self.map.map_lists_objects)

                    if nothing_right_enemy == False:
                        enemy.direction = "left"

                # Enemies falling if they aren't on top of something
                nothing_down_enemy = self.collisions.nothing_down(enemy, self.map.map_lists_objects)

                if nothing_down_enemy:
                    enemy.gravity()

                # now we move the enemy accordingly
                enemy.move()

                ## Collisions between Mario and enemies

                # if mario jumps on an enemy he defeats them

                # if it is a koopa troopa we substitute it with a shell
                mario_on_enemy, collision_x, collision_y = self.collisions.mario_jump_on_enemy(self.mario, enemy)
                if mario_on_enemy:
                    if enemy.subtype == "koopa_troopa":
                        koopa_troopa_shell = KoopaTroopaShell(enemy.x, enemy.y, direction="static")
                        self.shells.append(koopa_troopa_shell)

                    # we remove it
                    self.enemies.remove(enemy)

                    # we update the score and play the sound
                    self.collision_music(Constants.KILL_ENEMY_MUSIC)
                    self.score += Constants.MARIO_KILL_ENEMY_SCORE
                    self.enemy_killed = [True, collision_x, collision_y]


                # if an enemy touches Mario but wasn't jumped on Mario loses a life or changes form
                collision_mario_enemy = self.collisions.collision_with_object(self.mario, enemy)
                if collision_mario_enemy and self.restart == False and self.touched_one_time == False or self.mario.y > 256:
                    # if mario is in normal form
                    if self.mario.subtype == "normal" or self.mario.y > 256:
                        if self.lives > 1:
                            # we take a life and restart the game
                            self.lives -= 1
                            if self.testing_the_game == False:
                                self.restart = True
                        else:
                            # if there are no more lives left and we are not on testing mode the game is finished
                            self.lives = 0
                            if self.testing_the_game == False:
                                self.game_over = True
                    else:
                        # Change the type to normal and continue the game
                        self.mario.subtype = "normal"
                        self.score += Constants.SUPER_MARIO_KILLED_SCORE
                        self.touched_one_time = True

            # koopa troopa shells
            for shell in self.shells:
                if shell.direction == "static" and not self.enemy_killed[0]:
                    shell.direction = self.collisions.collision_mario_shell_static(self.mario, shell)
                    if shell.direction != "static":
                        # in order to not be killed when touching it
                        for i in range(2):
                            self.mario.rebound()

                # if it is moving we check the collisions
                if shell.direction == "right":
                    nothing_right_shell=self.collisions.nothing_right(shell, self.map.map_lists_objects)
                    if nothing_right_shell == False:
                        shell.direction = "left"

                elif shell.direction == "left":
                    nothing_left_shell = self.collisions.nothing_left(shell, self.map.map_lists_objects)
                    if nothing_left_shell == False:
                        shell.direction = "right"

                # we call on gravity when needed
                nothing_down_shell = self.collisions.nothing_down(shell, self.map.map_lists_objects)
                if nothing_down_shell:
                    shell.gravity()

                # we check if the shell has killed any enemy
                for enemy in self.enemies:
                    collision_shell_enemy = self.collisions.collision_with_object(shell, enemy)
                    if collision_shell_enemy:
                        self.enemies.remove(enemy)

                # we check if the shell has killed Mario
                collision_mario_shell = self.collisions.collision_with_object(self.mario, shell)
                if collision_mario_shell and self.restart == False and self.touched_one_time == False:
                    # if mario is in normal form
                    if self.mario.subtype == "normal":
                        if self.lives > 1:
                            self.lives -= 1
                            if self.testing_the_game == False:
                                self.restart = True
                        else:
                            self.lives = 0
                            if self.testing_the_game == False:
                                self.game_over = True
                    else:
                        # Change the type to normal and continue the game
                        self.mario.subtype = "normal"
                        self.score += Constants.SUPER_MARIO_KILLED_SCORE
                        self.touched_one_time = True

                # now we move the shell
                shell.move()

            # to allow again Mario to be killed after being hit one time
            if pyxel.frame_count % 50 == 0:
                self.touched_one_time = False

            # restart if the time is up
            if abs(time.time() - self.time_start) > self.game_time:
                self.restart = True
                self.lives -= 1

            if self.restart:
                Game.game_screens(self, types="restart")
                # we wait with 100  frames to start the new game
                if pyxel.frame_count % 100 == 0:
                    self.restart = False

            if self.game_over:
                # we wait with 100  frames to end the game
                if pyxel.frame_count % 100 == 0:
                    pyxel.quit()

            # Mario win's if he reaches the castle
            if self.map.castle[0].x + 36 == self.mario.x:
                if self.play_music:
                    pyxel.playm(Constants.BACKGROUND_MUSIC, loop=False)
                Game.game_screens(self, types="win")

        # we update the score and the lives
        Number.score_counter_update(self.score, self.score_numbers)
        self.lives_number.figure = self.lives
        self.lives_number.change_sprite()

        # if mario has falling through a whole we restart the game
        if self.testing_the_game == True and self.mario.y > 256:
            self.restart = True

    def draw(self):
        """
        This is the function needed for pyxel that will draw all of the elements we will see on the board
        """

        # the special screens
        if self.restart:
            pyxel.cls(0)
            pyxel.text(self.width // 2,self.height // 2,"RESTART",7)
            pyxel.text(self.width // 2,self.height // 2 + 16 ,"Lives :"+str(self.lives),7)
            pyxel.blt(self.width // 2 - 18 ,self.height // 2 + 13 ,*(0, 0, 48, 16, 16),colkey=6)
        elif self.game_over:
            pyxel.cls(0)
            pyxel.text(self.width // 2, self.height // 2, "GAME OVER", 7)
        elif self.win:
            pyxel.cls(pyxel.frame_count % 16)
            pyxel.text(self.width // 2, self.height // 2, "YOU PASSED LEVEL 1-1", 7)
        elif not self.start_game:
            pyxel.cls(0)
            pyxel.text(self.width // 2 -100, self.height // 2 - 32 , "SUPER MARIO BROS", 7 + pyxel.frame_count % 2)
            pyxel.blt(120, 80, *Constants.SUPER_MARIO_RIGTH, colkey=6)
            pyxel.text(self.width // 2 -100, self.height // 2, "PRESS ENTER-KEY TO START THE GAME", 7)
            pyxel.text(self.width // 2 - 100 , self.height // 2 + 32, "MADE BY IKER ROSALES & MONICA ALVARO DE MENA", 7)

        else:
            # sky
            pyxel.cls(6)

            # we draw the bushes, mountains and clouds of the background
            pyxel.bltm(self.bushesmountains.x, self.bushesmountains.y, *self.bushesmountains.sprite)
            pyxel.bltm(2400, 120, 0, 198, 42, 80, 92)

            # we draw each of the elements above, time, coins, score

            # time
            time_numbers = [self.unit_time.sprite, self.tenths_time.sprite, self.hundredths_time.sprite]
            for n in time_numbers:
                pyxel.blt(*n, colkey=0)

            # number of coins we have
            coin_numbers = [self.unit_coins.sprite, self.tenths_coins.sprite]
            for c in coin_numbers:
                pyxel.blt(*c, colkey=0)
            # icon of the coin
            pyxel.blt(16, 16 * 3, *self.coin_symbol, colkey=6)

            # score
            for n_score in self.score_numbers:
                pyxel.blt(*n_score.sprite, colkey=0)

            pyxel.blt(30, 4, *self.score_image, colkey=0)
            pyxel.blt(190, 4, *self.time_image, colkey=0)
            pyxel.blt(190, 16 * 3, *Constants.MARIO_RIGTH, colkey=6)
            pyxel.blt(206, 16 * 3, *Constants.CROSS_IMAGE, colkey=0)

            pyxel.blt(*self.lives_number.sprite, colkey=0)

            if self.testing_the_game == True:
                pyxel.blt(16, 16 * 4 + 8, *self.testing_game_image, colkey=0)

            # icon of the speaker
            pyxel.blt(self.music_icon.x, self.music_icon.y, *self.speaker_symbol, colkey=0)

            # now we draw all of the objects of the map
            self.map.draw()

            # we draw all the enemies
            for enemy in self.enemies:
                pyxel.blt(enemy.x, enemy.y, *enemy.sprite, colkey=6)
            for shell in self.shells:
                pyxel.blt(shell.x, shell.y, *shell.sprite, colkey=6)

            # other objects
            for other_object in self.other_objects:
                pyxel.blt(other_object.x, other_object.y, *other_object.sprite, colkey=6)

            # when an enemy is killed the score appears on the screen
            if self.enemy_killed[0]:
                pyxel.text(self.enemy_killed[1], self.enemy_killed[2], str(Constants.MARIO_KILL_ENEMY_SCORE), 7)

            # finally we draw mario
            if self.touched_one_time == False or pyxel.frame_count % 3 == 0:
                pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite, colkey=6)


    def clean_up (self):
        """
        This method will remove the elements that have been destroyed or have fallen through a hole
        """
        for enemy in self.enemies:
            # it the enemy has fallen through a hole, or is too far to the right
            if enemy.y > 256:
                self.enemies.remove(enemy)
            if enemy.x < -220:
                self.enemies.remove(enemy)

        for block in self.map.breackable_bricks:
            # if super mario has destroyed one of these blocks
            if block.keepalive == False:
                self.map.breackable_bricks.remove(block)

        for other_object in self.other_objects:
            # if they have fallen through a hole
            if other_object.y > 256:
                self.other_objects.remove(other_object)

        for map in self.map.map_lists_objects:
            # we remove the blocks that have dissapeared to the right
            for object in map:
                if object.x < -220:
                    self.map.map_lists_objects[self.map.map_lists_objects.index(map)].remove(object)

    def game_screens(self, types: str):
        """
        Mehtod that will change the screen depending on whether there is a restart
        """
        if types == "restart" and pyxel.frame_count % 99 == 0:
        # we restart the whole game, resetting yhe initial values except for the lives

            self.mario = Mario(20, 208)

            # we create the map which will have all the elements of the map again
            self.map = Map()

            # We change the values for the timer, coins and score that appear at the top of the screen
            self.user_interface()

            # we reset the necessary values of the game
            self.score = 0
            self.initiate_jump = False
            self.middle = False
            self.frame_counter = 0
            self.bushesmountains = Background(0, 0)

            # we empty the lists
            self.enemies.clear()
            self.other_objects.clear()
            self.shells.clear()

        if types == "win":
            self.win = True

        elif types == "start":
            if pyxel.btn(pyxel.KEY_ENTER):
                self.start_game = True

    def stop_start_music(self):
        # mehtod that stops and starts the music, updating the speaker icon
       if self.play_music == True:
           self.play_music = False
           self.speaker_symbol = Constants.SPEAKER_OFF_IMAGE
           pyxel.stop()
       else:
           self.play_music = True
           self.speaker_symbol = Constants.SPEAKER_ON_IMAGE


    def collision_music(self, music: int):
        # Method that will play the music when there is a collision
       if self.play_music == True:
            pyxel.stop()
            pyxel.play(0, music, loop=False)


    def user_interface(self):
        """
        This method will initialize the values for all the elements that appear on the top
        of the screen that tell the user the score, time left, coins and lives
        """

        # We initialize the values for the timer, coins and score that appear at the top of the screen

        # values for time
        self.hundredths_time = Number(4, 256 - 4*16, 16*2 - 8)
        self.tenths_time = Number(0, 256 - 3*16 + 1, 16*2 - 8)
        self.unit_time = Number(0, 256 - 2*16 + 1, 16*2 - 8)
        self.game_time = 400

        self.time = time.time()
        self.time_start = time.time()

        # values for coins
        self.tenths_coins = Number(0, 16*2 + 2, 16*3)
        self.unit_coins = Number(0, 16*3 + 5, 16*3)  # number of coins mario has won
        self.coin_symbol = Coin.sprite

        # number for the lives
        self.lives_number = Number(self.lives, 256 - 2*16, 16*3)

        # values for the score
        x_value_score = 16 # we go backwards
        self.score_numbers = []
        for number in range(6):
            score_number = Number(0, x_value_score, 16*2 - 8)
            x_value_score += 18
            self.score_numbers.append(score_number) # the number on the left is the first one in the list


