#This is the most important class of the game.
#In this class we manage collisions and the prints in pyxel

import pyxel
import random
import time
from collisions import Collisions
from pipes import Pipes
from platforms import Platform
from floor import Floor
from pow import Pow
from mario import Mario
from crab import Crab
from turtles import Turtles
from flies import Flies
from coins import Coins

class Board:
    def __init__(self, width, height):
        # These are the values that make the area of our screen
        self.width = width
        self.height = height
        # The stage is the level of the game that is being played, we start at the value 0, but it will change eventually
        stage = 0
        self.stage = stage
        #This attributes will control the pauses of the game
        pause_counter = 0
        self.pause_counter = pause_counter
        #This is a boolean that will control that the method controlling the pauses of the game are invoked
        pause = False
        self.pause = pause

        # To store all the pipes and work with them, I create a list of the four pipes that the program will have
        # To each of the pipes I assign a value for the position (taking into account we work with the top left corner)
        # which are the two first coordinates and the value of the side of the screen they are positioned in
        #It is very important that I now which are the upper and the lower pipes
        #the upper pipes are in positions 0 and 1, the lower ones are in positions 2 and 3, this will be very important
        list_of_pipes = [Pipes(0, 47, "right", "complex"),
                         Pipes(244, 47, "left", "complex"),
                         Pipes(0, 188, "right", "simple"),
                         Pipes(268, 188, "left", "simple")]
        self.pipes = list_of_pipes
        self.pow = Pow(width//2 - 8, 168)

        # To store the values of the platforms I generate a list of platforms that contains them all
        list_of_platforms = self.__generate_list_of_platforms()
        # With the list I created on the method y generate the object of teh scree platforms
        self.platforms = list_of_platforms

        # Now I create the floor of the game with a list called list_floor which contains the small squares that
        # generate the floor of the screen
        list_floor = []
        x = 0
        for i in range(19):
            list_floor.append(Floor(x, height - 16))
            x += 16
        self.floor = list_floor

        # The following conditions will control what is the number of enemies according to the stage of the game we are in
        # The number of enemies increases according to the level of difficulty of the game
        #this will be controlled in a method of the class
        number_enemies = 0
        self.number_enemies = number_enemies
        #This will control that the number of enemies that should be created is only introduced once
        self.generated_enemies = False
        # Now I create an attribute to represent the enemies, as the enemies are created in relation to the time intervals
        # that happen in the update, the list has to be inicialised empty and then the enemies will be appended if
        # the timer conditions are met
        list_enemies = []
        self.enemies = list_enemies
        # This two attributes are the ones that control that the enemies do not appear all at once but that they appear
        # with a 4 seconds time interval
        # this first attribute will be the counter that will count what the intervals are
        enemy_counter = 0
        self.enemy_counter = enemy_counter

        #This is the attribute that controls the coins inside the game
        list_of_coins = []
        self.coins = list_of_coins
        #Now I generate a counter that will control from which time to which time the coins appear of screen
        coins_counter = 0
        self.coins_counter = coins_counter

        # Now I need to create an attribute that represent the character Mario and in this case I give it the standard value
        # This is because most of the modifications that involve its changes have to be developed on the update function
        # I have written the y coordinate so that the character appears at the center of the screen and touching the floor
        mario = Mario(width // 2 - 12, self.floor[0].y - 24)
        self.mario = mario

        # This initializes the pyxel program with the values of the width and the height that have been given
        pyxel.init(self.width, self.height, title="MARIO BROS", fps=40)
        pyxel.load("../assets/sprites-jjsv-ndb.pyxres")
        pyxel.image(1).load(0, 0, "../assets/mariobros.png")
        pyxel.image(2).load(0, 0, "../assets/game over.png")
        pyxel.image(2).load(100, 100, "../assets/win.png")
        pyxel.run(self.update, self.draw)

    @property
    def width(self) -> int:
        return self.__width
    @width.setter
    def width(self, width) -> int:
        if type(width) != int:
            raise TypeError("Width must be an integer")
        elif width != 300:
            raise ValueError("It is though to have width 300")
        else:
            self.__width = width
    @property
    def height(self) -> int:
        return self.__height
    @height.setter
    def height(self, height) -> int:
        if type(height) != int:
            raise TypeError("Height must be an integer")
        elif height != 230:
            raise ValueError("Height is thought to be 210")
        else:
            self.__height = height
    @property
    def stage(self) -> int:
        return self.__stage
    @stage.setter
    def stage (self, stage) -> int:
        if type(stage) != int:
            raise TypeError
        elif stage < 0 or stage > 5:
            raise ValueError
        else:
            self.__stage = stage
    @property
    def pause_counter (self) -> int:
        return self.__pause_counter
    @pause_counter.setter
    def pause_counter (self, pause_counter) -> int:
        if type (pause_counter) != int:
            raise TypeError
        elif pause_counter < 0:
            raise ValueError
        else:
            self.__pause_counter = pause_counter
    @property
    def pause (self) -> bool:
        return self.__pause
    @pause.setter
    def pause (self, pause) -> bool:
        if type(pause) != bool:
            raise TypeError
        else:
            self.__pause = pause
    @property
    # This will make the pauses of the game to last for 2 seconds. It is read only because it shouldn't be modified
    def pause_interval (self):
        return 80
    @property
    def number_enemies (self) -> int:
        return self.__number_enemies
    @number_enemies.setter
    def number_enemies (self, number_enemies) -> int:
        if type(number_enemies) != int:
            raise TypeError
        elif number_enemies < 0:
            raise ValueError
        else:
            self.__number_enemies = number_enemies
    @property
    def enemy_counter (self) -> int:
        return self.__enemy_counter
    @enemy_counter.setter
    def enemy_counter (self, enemy_counter) -> int:
        if type(enemy_counter) != int:
            raise TypeError
        elif enemy_counter < 0:
            raise ValueError
        else:
            self.__enemy_counter = enemy_counter
    @property
    # this is the interval at which the enemies will appear, as the fps are 40 if I multiply that by 3 I get an
    # interval of 3 second between each enemy appearance. It is private because I don't want it to be modified
    def enemy_interval (self) -> int:
        return 120
    @property
    def coins_counter (self)-> int:
        return self.__coins_counter
    @coins_counter.setter
    def coins_counter (self, coins_counter):
        if type(coins_counter) != int:
            raise TypeError
        elif coins_counter < 0:
            raise ValueError
        else:
            self.__coins_counter = coins_counter
    @property
    def coin_interval (self) -> int:
        #The interval at which the coins will appear will be every 5 seconds, so (40fps * 5 = 200)
        return 200
    @property
    def mario (self) -> object:
        return self.__mario
    @mario.setter
    def mario (self, mario) -> object:
        if isinstance(mario, Mario) != True:
            raise TypeError
        else:
            self.__mario = mario

    def __str__(self):
        return "Main Board of the game"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.stage == other.stage, self.mario == other.mario, self.enemies == other.enemies,
                self.platforms == other.platforms, self.floor == other.floor)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        #this controls the restart of the game when the user has finished and wants to play more
        if pyxel.btnp(pyxel.KEY_RETURN):
            #This controls the  start of the game and the change from the opening screen to the actual game
            if self.stage == 0:
                self.stage = 1
            #this controls the restart of the game
            if self.mario.lifes == 0 or self.stage == 5:
                self.__restart()

        #this code is the one that controls the actual game
        if self.stage > 0 and self.stage < 5 and self.mario.lifes > 0:
            #here we control the pauses of the game
            if self.pause == True:
                self.pause_counter += 1
                self.__game_pause()
            else:
                self.mario.killed = False

            #This is what defines what the elements and platforms of the screen look like:
            self.__sprite_platforms()
            #first I make sure what the number of enemies that will be created is but this should only be created once
            if self.generated_enemies == False:
                self.__number_of_enemies()

            # this code here is what controls the counter that makes sure enemies appear every 4 seconds, for that, every time
            # the update is updated (40 times per second) the interval will add one
            self.enemy_counter += 1

            # this controls that I do not create more enemies than I want to
            if len(self.enemies) < self.number_enemies:
                # first of all I append the enemies to make sure they are created, for that I make sure that the length of the
                # list that contains them is not longer than the number of enemies I want to create, I have to make sure
                # that the list is appending an enemy and not a None, because otherwise I would have problems with my code
                new_enemy = self.__generate_enemies()
                # this second if controls that I only add enemies and not None
                if new_enemy != None:
                    self.enemies.append(new_enemy)
            #here I control the movement of the coins
            for index in range (len(self.coins)):
                self.coins[index].change_sprite()
            #this code here will control that I generate new coins and that they appear on screen, the logic will be
            #the same as the enemies creation logic
            self.coins_counter += 1
            #here I generate the new coins that will appear on screen
            new_coin = self.__generate_coins()
            #now I control that I have generated an enemy
            if self.coins_counter % self.coin_interval == 0:
                self.coins.append(new_coin)
            #this code will help to control that the turning of the coins is not that fast
            for index in range (len(self.coins)):
                self.coins[index].change_time += 1
            #now other movement functions are to be taken
            # I control that mario can only move if it is on top of a platform or on top of the floor
            if self.mario_landed() == True:
                # The following ifs control that if I touch a certain key the object moves to the left or to the right
                # I should also add a variation in where does mario look according to where is he moving
                if pyxel.btn(pyxel.KEY_LEFT):
                    self.mario.direction = "left"
                    self.mario.move()
                elif pyxel.btn(pyxel.KEY_RIGHT):
                    self.mario.direction = "right"
                    self.mario.move()
                # The following code controls the jumping
                if pyxel.btnp(pyxel.KEY_SPACE) and not self.mario.jump:
                    self.mario.jump = True
                    # this represents the force that is made by mario to jump
                    self.mario.speed_y = -11
                if self.mario.jump == True:
                    self.mario.jumping()
            # Then if mario is not on top of any platform or floor, then force of gravity will affect him
            else:
                self.mario_platform()
                self.mario_pow()
                self.mario.jumping()
                self.mario_landed()

            #this code controls the movement of the enemies according to the methods created in their class
            for index in range(len(self.enemies)):
                enemy = self.enemies[index]
                if self.enemy_landed(enemy) == True:
                    if isinstance(enemy, Flies):
                        if enemy.jumping == True:
                            enemy.speed_y = -6
                            enemy.gravity()
                    self.enemies[index].move()
                    self.enemy_pipes(enemy)
                else:
                    self.enemies[index].gravity()
                    self.enemies[index].move()
            #here I add a counter that controls how many time an enemy has been turned for, when it has turned for that
            #time (2.5 seconds = 80) they come back to life
            for index in range (len(self.enemies)):
                if self.enemies[index].turned == True:
                    self.enemies[index].time_turned += 1
                    self.enemies[index].back_to_life()
            #this two methods manage the collisions between the elements of the game
            self.enemy_enemy()
            self.mario_enemy()
            self.mario_coins()

            #If all the enemies have been killed, then I enter into a new stage of the game because I have succeded
            if self.number_enemies == 0:
                self.generated_enemies = False
                #on the change of stages, the game experiences a small pause so that it's not that abrupt
                self.pause = True
                #when we have killed all the enemies, we have to change the stage of the game because we would have
                #finished the task of that stage
                self.stage += 1

    def draw(self):
        pyxel.cls(0)
        for index in range(len(self.floor)):
            # This is the function that prints the floor of the game
            pyxel.blt(self.floor[index].x, self.floor[index].y, *self.floor[index].sprite)

        # Here I print the lifes that mario has
        x = 30
        for index in range(self.mario.lifes):
            pyxel.blt(x, 5, 0, 88, 208, 16, 16, 0)
            x += 20
        #Here I print the points obtained by the player:
        pyxel.text (230, 8, "POINTS:" + str(self.mario.points), 7)

        if self.stage == 0:
            pyxel.blt(50, 30, 1, 0, 0, 200, 103)
            pyxel.text (55, 140, "To start the game press ENTER", 5)
            pyxel.text(55, 150, "To exit press ESCAPE", 5)
            pyxel.text ( 55, 160, "RULES OF THE GAME: \n  To jump press SPACE \n  "
            "To move use the key arrows \n  To kill enemies, kick their platform \n  once they're turned, touch them",
            5)
            pyxel.text (55, 195, "You only have 3 lives. GOOD LUCK!", 5)

        if (self.stage > 0 and self.stage < 5) and self.mario.lifes > 0:
            for index in range(len(self.pipes)):
                # This is the function that prints the graphics containing the pipes
                pyxel.blt(self.pipes[index].x, self.pipes[index].y, *self.pipes[index].sprite)

            for index in range(len(self.platforms)):
                # This is the function that prints the graphics containing the platforms
                pyxel.blt(self.platforms[index].x, self.platforms[index].y, *self.platforms[index].sprite)

            # This is the function that draws the pow it only appears while it is available, otherwise it will disappear
            if self.pow.uses < 3:
                pyxel.blt(self.pow.x, self.pow.y, *self.pow.sprite)

            #This is the function that prints the coins
            for index in range(len(self.coins)):
                pyxel.blt(self.coins[index].x, self.coins[index].y, *self.coins[index].sprite)

            # This is the function that prints Mario
            if self.mario.killed == False and self.pause == False:
                pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
            elif self.mario.killed == True:
                pyxel.blt(self.mario.x, self.mario.y, *(0, 112, 0, 16, 24))

            #This function prints the enemies
            for index in range (len(self.enemies)):
                pyxel.blt (self.enemies[index].x, self.enemies[index].y, *self.enemies[index].sprite)

        if self.mario.lifes <= 0:
            pyxel.blt(118, 90, 2, 0, 0, 62, 36, 0)
            pyxel.text(100, 130, "YOU HAVE OBTAINED " + str(self.mario.points) + " POINTS", 8)
            pyxel.text (100, 140, "TO START AGAIN PRESS ENTER", 8)
            pyxel.text (100, 150, "TO EXIT PRESS ESCAPE OR Q", 8)
            pyxel.blt (142, self.floor[0].y - 24, 0,112, 0, 16, 24)

        if self.stage >= 5:
            pyxel.blt (118, 90, 2, 100, 100, 62, 36, 0)
            pyxel.text (100, 130, "YOU HAVE OBTAINED " + str(self.mario.points) + " POINTS", 8)
            pyxel.text (100, 140, "TO START AGAIN PRESS ENTER", 8)
            pyxel.text (100, 150, "TO EXIT PRESS ESCAPE OR Q", 8)
            pyxel.blt(142, self.floor[0].y - 24, 0, 96, 0, 16, 24)


    # METHODS RELATED TO THE CREATION OF GAME ELEMENTS AND TO CONTROL OF THE THINGS HAPPENING ON SCREEN:
    def __sprite_platforms (self):
        # The platforms vary in each stage of the game, the stages of the game are managed by the class board and the
        # coins obtained , however, we need to knw in which stage we are tio control the sprites of the platforms
        # We have 4 stages of the game and therefore we need 4 cases of the sprite
        for index in range (len(self.platforms)):
            if self.stage == 1:
                # In the stage 0 we have the basic brown platforms
                sprite = (0, 8, 232, 8, 8)
            elif self.stage == 2:
                # In the stage 1 we have the ones that are brick-like
                sprite = (0, 8, 224, 8, 8)
            elif self.stage == 3:
                # In the stage 2 we have the blue ones
                sprite = (0, 0, 224, 8, 8)
            elif self.stage == 4:
                # In the last stage we have the green platform
                sprite = (0, 0, 232, 8, 8)
            self.platforms[index].sprite = sprite
    def __number_of_enemies (self):
        # The following conditions will control what is the number of enemies according to the stage of the game we are in
        # The number of enemies increases according to the level of difficulty of the game
        if self.stage == 1:
            number_enemies = 5
        elif self.stage == 2:
            number_enemies = 7
        elif self.stage == 3:
            number_enemies = 10
        elif self.stage == 4:
            number_enemies = 12
        self.number_enemies = number_enemies
        self.generated_enemies = True
    def __generate_list_of_platforms(self):
        # I also create a list of the platforms so that I can control where they are placed better
        # I do it with the help of a loop so that they are easier to generate
        # The range of the loop is the number of platforms that will be sticked in a same line (long platform)

        list_of_platforms = []
        # this first loop corresponds to the creation of the platforms up and down of the left side of the screen
        y = 80
        for i in range(2):
            x = 0
            # Each platform will have 5 small squares in it
            for j in range(12):
                list_of_platforms.append(Platform(x, y))
                # as each small square has side 8, the position should be incremented by 8
                x += 8
            # as I want the platforms to be separated by 42, I increase y by 42
            y += 92
        # now I do the same thing but for those platforms on the right side of the screen
        y = 80
        for i in range(2):
            x = self.width
            # Each platform will have 5 small squares in it
            for j in range(12):
                list_of_platforms.append(Platform(x, y))
                # as each small square has side 8, the position should be incremented by 8
                x -= 8
            # as I want the platforms to be separated by 42, I increase y by 42
            y += 92
        # Now I do a similar loop for the platforms that correspond to the center of the screen
        x = 0
        for i in range(6):
            list_of_platforms.append(Platform(x, 127))
            x += 8
        x = self.width
        for i in range(6):
            list_of_platforms.append(Platform(x, 127))
            x -= 8
        # and now the last platform on the center
        x = 102
        for i in range(12):
            list_of_platforms.append(Platform(x, 127))
            x += 8
        return list_of_platforms
    def __generate_enemies (self):
        #The enemies and their type will be random however they will all appear from one of the upper pipes
        #The pipe they come from will also be random.
        #Each type of enemy will have one number assigned and so they will be appended

        #the position at which it will start will be also random so I generate a random number [0, 1]
        position = random.randint(0, 1)
        # now I finally generate the enemy
        if position == 0:
            #in this case the enemy will appear at the left pipe
            x = self.pipes[0].x + 56
            y = self.pipes[0].y
        elif position == 1:
            #in this case the enemy will appear at the right pipe
            x = self.pipes[1].x - 16
            y = self.pipes[1].y
        #As I have three types of enemies I have to generate random numbers from 1 to 3
        if self.stage < 3:
            number = random.randint(1,2)
        else:
            number = random.randint(1, 3)
        # I have to add the condition that 4 seconds have passed between the previous creation of the enemy, as
        # i don't want the first enemy to appear at the beginning of the game but with that time interval I have to
        #check that the timer is a divisior of the interval that I want the enmies to be created in for that I check
        #for that if I divide the counter with the interval, the reminder is 0, if that condition is not met, the
        # enemy will not be added to the list
        if self.enemy_counter % self.enemy_interval == 0:
            #now this assigns the type of enemy according to the random number that has been given
            if number == 1:
                enemy = Turtles(x,y)
            elif number == 2:
                enemy = Crab(x,y)
            elif number == 3:
                enemy = Flies(x,y)
            #I return the enemy that I have just generated so that I can append it to the list of enemies
            return enemy
    def __generate_coins (self):
        #The coins will be placed on random parts of the platform, but always on top of them
        x = random.randint(10, 220)
        #Now I control that it does not coincide with the pow
        if x + 8 >= self.pow.x and x <= self.pow.x + 16:
            x = random.randint (10, 210)

        y = random.randint(65, 160)
        # Now I control it does not coincide with the pow
        if y + 10 >= self.pow.y and y <= self.pow.y + 16:
            y = random.randint(65, 160)
        #Then I control that it doesnt coincide with the platforms
        for index in range (len(self.platforms)):
            if y + 12 >= self.platforms[index].y and y <= self.platforms[index].y + 8:
                #Now I move the coin so that It's not placed on top of the platforms
                if y > self.platforms[index].y:
                    #this means that the coin is below
                    y += 15
                elif y < self.platforms[index].y:
                    #this means that the coin is above
                    y -= 15

        coin = Coins(x, y)
        return coin

    #This method controls that when mario is killed, the game is paused for some time and then it's "restarted" from
    #the point in which it was left
    def __game_pause (self):
        if self.pause_counter != self.pause_interval:
            self.mario.speed_x = 0
            for index in range(len(self.enemies)):
                self.enemies[index].speed_x = 0
        if self.pause_counter == self.pause_interval:
            self.mario.x = self.width // 2 - 8
            self.mario.y = self.floor[0].y - 24
            self.pause_counter = 0
            self.mario.speed_x = 2.5
            self.enemies = []
            self.coins = []
            self.pause = False
    def __restart(self):
        #here I reset all the values to those that had been established at the beginning of the game
        self.stage = 0
        self.mario.lifes = 3
        self.generated_enemies = False
        self.mario.points = 0
        self.pow.uses = 0
        self.pow.change_sprite()
        self.enemy_counter = 0
        self.enemies = []
        self.coins = []


    #COLLISION METHODS
    def mario_landed(self) -> bool:
        landed = False
        for index in range(len(self.platforms)):
            # This first condition controls that mario is on the same position of the y axis as the platforms
            if (self.mario.y + self.mario.sprite[4] >= self.platforms[index].y and
                    self.mario.y + self.mario.sprite[4] <= self.platforms[index].y + self.platforms[index].sprite[4]):
                # this second condition checks that mario is on the same position of the x axis as the platforms
                # it could have been written on the same condition but this is a bit easier to read and comprehend
                if (self.mario.x + 16 >= self.platforms[index].x and
                        self.mario.x <= self.platforms[index].x + self.platforms[index].sprite[3]):
                    landed = True
                    # this changes the sprite according to what is necessary
                    if self.mario.direction == "right":
                        self.mario.sprite = (0, 0, 0, 16, 24, 0)
                    elif self.mario.direction == "left":
                        self.mario.sprite = (0, 0, 0, -16, 24, 0)
                    # this sets the position of mario to that of the platform so that it can walk there
                    self.mario.y = self.platforms[index].y - self.mario.sprite[4]
                    # now this two expressions make mario stop moving vertically (falling) because it has fallen fully
                    self.mario.jump = False
                    self.mario.speed_y = 0
        # This code controls when mario lands on the floor
        for index in range(len(self.floor)):
            # in this one we only check the y because the floor oes all along the x-axis so checking that is not needed
            if self.mario.y + self.mario.sprite[4] >= self.floor[index].y:
                landed = True
                if self.mario.direction == "right":
                    self.mario.sprite = (0, 0, 0, 16, 24, 0)
                elif self.mario.direction == "left":
                    self.mario.sprite = (0, 0, 0, -16, 24, 0)
                self.mario.y = self.floor[index].y - 24
                self.mario.jump = False
                self.mario.speed_y = 0
        # This condition will control that the pow only works for a maximum of 3 times as according to the rules
        if self.pow.uses < 3:
            # now this controls when mario lands on the pow the loic is the same one as that of the previous conditionals as
            # the process in them is very similar (see explanation on the first one)
            if self.mario.y + self.mario.sprite[4] >= self.pow.y and self.mario.y + self.mario.sprite[4] <= self.pow.y + self.pow.sprite[4]:
                if self.mario.x + self.pow.sprite[3] >= self.pow.x and self.mario.x <= self.pow.x + self.pow.sprite[3]:
                    landed = True
                    if self.mario.direction == "right":
                        self.mario.sprite = (0, 0, 0, 16, 24, 0)
                    elif self.mario.direction == "left":
                        self.mario.sprite = (0, 0, 0, -16, 24, 0)
                    self.mario.y = self.pow.y - self.mario.sprite[4]
                    self.mario.jump = False
                    self.mario.speed_y = 0
        return landed
    def mario_platform(self):
        # This method controls the collisions with the platforms
        # In this method I also have to control that if mario kicks a platform and an enemy is placed just where he has
        # kicked, then, the enemy should turn around so that it can be killed
        for index in range(len(self.platforms)):
            # This condition controls that the coordinates of mario are those that correspond to the platform
            if (self.mario.y >= self.platforms[index].y and
                self.mario.y <= self.platforms[index].y + self.platforms[index].sprite[4]):
                if (self.mario.x + 16 > self.platforms[index].x and
                    self.mario.x < self.platforms[index].x + self.platforms[index].sprite[3]):
                    # This will let us handle how many times has mario touched the platform and allow us to work better
                    self.mario.y = self.platforms[index].y + self.platforms[index].sprite[4]
                    # Once mario has hit the platform we turn his velocity on the y axis to 0  so that when then we
                    # apply on him the force of gravity so that he falls back down
                    self.mario.speed_y = 0
                    # now here I control that if there is an enemy in that same position, the enemy is turned around
                    #or killed according to its type
                    i = 0
                    touches = 1

                    while i < len(self.enemies):
                        #this controls that they are at the same height as the platforms
                        if (self.enemies[i].y + self.enemies[i].sprite[4] >= self.platforms[index].y and
                            self.enemies[i].y + self.enemies[i].sprite[4] <= self.platforms[index].y + self.platforms[index].sprite[4]):
                            #this controls that they are at the same position as the platform that mario is touching
                            if (self.enemies[i].x + 16 >= self.platforms[index].x and
                                self.enemies[i].x <= self.platforms[index].x + self.platforms[index].sprite[3]):
                                #now according to what the enemy type is, they do a different thing accordingly
                                if isinstance(self.enemies[i], Turtles):
                                    self.enemies[i].turn_sprite()
                                elif isinstance(self.enemies[i], Crab):
                                    touches += 1
                                    if touches == 2:
                                        self.enemies[i].turn_sprite()
                                elif isinstance(self.enemies[i], Flies):
                                    self.enemies.pop(i)
                                    #this are the points you get for killing a fly
                                    self.mario.points += 200
                        i += 1
    # We apply the same logic than we have applied in the previous method to the pow, however this has to be done on a
    # different method because of the specific things that touching the pow imply
    def mario_pow(self):
        # This condition will control that the pow only works for a maximum of 3 times as according to the rules
        if self.pow.uses < 3:
            # This condition controls that the coordinates of mario are those that correspond to the platform
            if (self.mario.y >= self.pow.y and self.mario.y <= self.pow.y + self.pow.sprite[4]):
                if (self.mario.x + 16 > self.pow.x and self.mario.x < self.pow.x + self.pow.sprite[3]):
                    # Once mario has hit the platform we turn his velocity on the y axis to 0  so that when then we
                    # apply on him the force of gravity so that he falls back down
                    self.mario.speed_y = 0
                    # I have to add this because otherwise the program will count all the time that mario is on that position
                    # interval and that would make it very difficult to control the actual times it has touched the pow
                    self.mario.y = self.pow.y + self.pow.sprite[4]
                    self.pow.uses += 1
                    self.pow.change_sprite()
                    # now here I control that if there is an enemy in that same position, the enemy is turned around
                    #or that it is directly killed, according to its type. That's why we use a while.
                    index = 0
                    while index < len(self.enemies):
                        if isinstance(self.enemies[index], Turtles) or  isinstance(self.enemies[index], Crab):
                            self.enemies[index].turn_sprite()
                        else:
                            #when I press the pow, the flies re directly killed as tthey cannot be turned
                            self.enemies.pop(index)
                        index += 1
    # the relation with the platforms and elements on the game logic of the enemies is similar to the one of mario
    def enemy_landed(self, enemy: object):
        landed = False
        for index in range(len(self.platforms)):
            # This first condition controls that the enemy is on the same position of the y axis as the platforms
            if (enemy.y + enemy.sprite[4] >= self.platforms[index].y and
                enemy.y + enemy.sprite[4] <= self.platforms[index].y + self.platforms[index].sprite[4]):
                # this second condition checks that the enemy is on the same position of the x axis as the platforms
                # it could have been written on the same condition but this is a bit easier to read and comprehend
                if enemy.x + 16 >= self.platforms[index].x and enemy.x <= self.platforms[index].x + self.platforms[index].sprite[3]:
                    landed = True
                    # this sets the position of enemy to the position platform so that it can move
                    enemy.y = self.platforms[index].y - 16
                    # this makes the enemy to stop falling
                    enemy.speed_y = 0

        # this does the same but with the floor
        for index in range(len(self.floor)):
            # in this one we only check the y because the floor oes all along the x axis so checking that is not needed
            if enemy.y + enemy.sprite[4] >= self.floor[index].y:
                landed = True
                enemy.y = self.floor[index].y - enemy.sprite[4]
                enemy.speed_y = 0
        return landed
    # this method is the one that controls that when the enemies touch a lower pipe, they have to appear on an
    # upper pipe
    def enemy_pipes(self, enemy: object):
        # the upper pipes are in positions 1 and 0, and the lower pipes in positions 2 and 3 of the pipes list
        # the lower one on the right side is position 2, and the lower one on the left side is position 3
        # their width is 32, and their height is 22
        # first, I control that they are on the same x position as the pipes
        if ((self.pipes[2].y < enemy.y < self.pipes[2].y + self.pipes[2].sprite[4]) or
                (self.pipes[3].y < enemy.y < self.pipes[3].y + self.pipes[3].sprite[4])):
            # next, I control that they are on the same y position, I do it separately because they are easier to read
            if (enemy.x <= self.pipes[2].x + self.pipes[2].sprite[3]) or (enemy.x + 16 >= self.pipes[3].x):
                # Now I generate a random number between 0 and 1 so that the enemy appears at a random upper pipe
                # The 0 is the pipe on the right and the 1 is the pipe on the left
                number = random.randint(0, 1)
                # this makes the enemy to reappear on the upper pipe of the right
                if number == 0:
                    enemy.x = self.pipes[0].x + self.pipes[0].sprite[3]
                    enemy.y = self.pipes[0].y
                # this makes the enemy to appear on the upper left pipe
                elif number == 1:
                    enemy.x = self.pipes[1].x - 16
                    enemy.y = self.pipes[1].y
    # this method controls the collisions between enemies
    def enemy_enemy(self):
        collision = False
        for i in range(len(self.enemies)):
            for j in range(len(self.enemies)):
                # this checks that we are not comparing the same enemies
                if i != j and collision == False:
                    # this checks their x position is the same
                    if self.enemies[i].x + 16 >= self.enemies[j].x and self.enemies[i].x <= self.enemies[j].x:
                        # this checks their y position is the same
                        if (self.enemies[i].y >= self.enemies[j].y and
                            self.enemies[i].y + self.enemies[i].sprite[4] <= self.enemies[j].y + self.enemies[j].sprite[4]):
                            collision = True
                            # now I implement the logic so that they go to opposite directions
                            if self.enemies[i].direction == self.enemies[j].direction:
                                if self.enemies[i].direction == "left":
                                    self.enemies[i].direction = "right"
                                    self.enemies[i].x += 16
                                    self.enemies[j].x -= 16
                                elif self.enemies[i].direction == "right":
                                    self.enemies[i].direction = "left"
                                    self.enemies[j].x += 16
                                    self.enemies[i].x -= 16
                            elif self.enemies[i].direction != self.enemies[j].direction:
                                if self.enemies[i].direction == "left" and self.enemies[j].direction == "right":
                                    self.enemies[i].direction = "right"
                                    self.enemies[j].direction = "left"
                                    self.enemies[i].x += 16
                                    self.enemies[j].x -= 16
                                elif self.enemies[i].direction == "right" and self.enemies[j].direction == "left":
                                    self.enemies[i].direction = "left"
                                    self.enemies[j].direction = "right"
                                    self.enemies[j].x += 16
                                    self.enemies[i].x -= 16
    # this method controls the collisions between mario and the enemies
    def mario_enemy(self):
        index = 0
        while index < len(self.enemies) and self.mario.killed == False:
            # this checks the position of mario and the position of the enemy is the same
            if self.enemies[index].x <= self.mario.x + 16 and self.enemies[index].x + 16 >= self.mario.x:
                # this checks their y position is the same
                if (self.enemies[index].y >= self.mario.y and
                    self.enemies[index].y + self.enemies[index].sprite[4]<= self.mario.y + self.mario.sprite[4]):
                    #if the enemy has been turned then I can kill it
                    if self.enemies[index].turned == True:
                        if isinstance(self.enemies[index], Turtles) or isinstance(self.enemies[index], Crab):
                            self.enemies[index].killed()
                        #This controls how many points you get for killing each type of enemy
                        if isinstance(self.enemies[index], Turtles):
                            self.mario.points += 100
                        elif isinstance(self.enemies[index], Crab):
                            self.mario.points += 300
                        self.enemies.pop(index)
                        self.number_enemies -= 1
                    elif self.enemies[index].turned == False:
                        if self.enemies[index].x < self.mario.x:
                            self.mario.x = self.enemies[index].x + 17
                        else:
                            self.mario.x = self.enemies[index].x - 17
                        self.mario.killed = True
                        self.mario.lifes -= 1
                        self.pause = True
            index += 1
    #this method controls the collisions between mario and the coins
    def mario_coins (self):
        index = 0
        #I use a while so that I don't get out of range because I will be deleting the coins that I have already taken
        while index < len(self.coins):
            if self.mario.x + 16 >= self.coins[index].x and self.mario.x <= self.coins[index].x + self.coins[index].sprite[3]:
                # this checks their y position is the same
                if (self.coins[index].y >= self.mario.y and
                    self.coins[index].y + self.coins[index].sprite[4] <= self.mario.y + self.mario.sprite[4]):
                    self.mario.points += 500
                    self.coins.pop(index)
            index += 1
