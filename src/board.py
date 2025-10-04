""" This class manages the complete logic of the game creating the elements and managing screen display """

import pyxel
import random
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
        """ Start the game building the elements, initializing pyxel and managing pause options"""
        self.width = width
        self.height = height
        stage = 0
        self.stage = stage
        pause_counter = 0
        self.pause_counter = pause_counter
        pause = False
        self.pause = pause
        # Generate the pipes with fixed sizes and positions
        list_of_pipes = [Pipes(0, 47, "right", "complex"),
                         Pipes(244, 47, "left", "complex"),
                         Pipes(0, 188, "right", "simple"),
                         Pipes(268, 188, "left", "simple")]
        self.pipes = list_of_pipes
        self.pow = Pow(width//2 - 8, 168)

        # Generate the platforms and floot to allow movement
        list_of_platforms = self.__generate_list_of_platforms()
        self.platforms = list_of_platforms
        
        list_floor = []
        x = 0
        for i in range(19):
            list_floor.append(Floor(x, height - 16))
            x += 16
        self.floor = list_floor

        # Generate the enemies to be displayed
        number_enemies = 0
        self.number_enemies = number_enemies
        self.generated_enemies = False
        list_enemies = []
        self.enemies = list_enemies
        # Interval of enemy appearance
        enemy_counter = 0
        self.enemy_counter = enemy_counter

        # Coins control and appearance
        list_of_coins = []
        self.coins = list_of_coins
        coins_counter = 0
        self.coins_counter = coins_counter

        # Mario creation
        mario = Mario(width // 2 - 12, self.floor[0].y - 24)
        self.mario = mario

        # Pyxel initialization
        pyxel.init(self.width, self.height, title="MARIO BROS", fps=40)
        pyxel.load("../assets/sprites-jjsv-ndb.pyxres")
        pyxel.image(1).load(0, 0, "../assets/mariobros.png")
        pyxel.image(2).load(0, 0, "../assets/game over.png")
        pyxel.image(2).load(100, 100, "../assets/win.png")
        pyxel.run(self.update, self.draw)

    # PROPERTIES OF THE CLASS
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
        """ Method to contol the updates and restarts of the game"""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.stage == 0:
                self.stage = 1
            if self.mario.lifes == 0 or self.stage == 5:
                self.__restart()

        if self.stage > 0 and self.stage < 5 and self.mario.lifes > 0:
            if self.pause == True:
                self.pause_counter += 1
                self.__game_pause()
            else:
                self.mario.killed = False

            self.__sprite_platforms()
            if self.generated_enemies == False:
                self.__number_of_enemies()

            # We increase the counter to manage enemy appearance
            self.enemy_counter += 1

            if len(self.enemies) < self.number_enemies:
                new_enemy = self.__generate_enemies()
                if new_enemy != None:
                    self.enemies.append(new_enemy)
                    
            # manage coins appearance        
            for index in range (len(self.coins)):
                self.coins[index].change_sprite()
            self.coins_counter += 1
            new_coin = self.__generate_coins()
            
            if self.coins_counter % self.coin_interval == 0:
                self.coins.append(new_coin)
                
            # Rotation of the coins 
            for index in range (len(self.coins)):
                self.coins[index].change_time += 1
                
            # Management of Marios movement
            if self.mario_landed() == True:
                if pyxel.btn(pyxel.KEY_LEFT):
                    self.mario.direction = "left"
                    self.mario.move()
                elif pyxel.btn(pyxel.KEY_RIGHT):
                    self.mario.direction = "right"
                    self.mario.move()
                # The following code controls the jumping
                if pyxel.btnp(pyxel.KEY_SPACE) and not self.mario.jump:
                    self.mario.jump = True
                    self.mario.speed_y = -11
                if self.mario.jump == True:
                    self.mario.jumping()
            # Gravity force is applied when not on a surface
            else:
                self.mario_platform()
                self.mario_pow()
                self.mario.jumping()
                self.mario_landed()

            #Enemies movements
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
            # Management of enemies kills and survivance
            for index in range (len(self.enemies)):
                if self.enemies[index].turned == True:
                    self.enemies[index].time_turned += 1
                    self.enemies[index].back_to_life()
                    
            # Manage collisions 
            self.enemy_enemy()
            self.mario_enemy()
            self.mario_coins()

            # Stage change control
            if self.number_enemies == 0:
                self.generated_enemies = False
                self.pause = True
                self.stage += 1

    def draw(self):
        """ Method to draw the elements to be displayed on teh screen"""
        # Print the floor
        pyxel.cls(0)
        for index in range(len(self.floor)):
            pyxel.blt(self.floor[index].x, self.floor[index].y, *self.floor[index].sprite)
        
        # This prints the lives
        x = 30
        for index in range(self.mario.lifes):
            pyxel.blt(x, 5, 0, 88, 208, 16, 16, 0)
            x += 20
        
        # This prints the points obtained
        pyxel.text (230, 8, "POINTS:" + str(self.mario.points), 7)

        # This prints the starting screen of the game
        if self.stage == 0:
            pyxel.blt(50, 30, 1, 0, 0, 200, 103)
            pyxel.text (55, 140, "To start the game press ENTER", 5)
            pyxel.text(55, 150, "To exit press ESCAPE", 5)
            pyxel.text ( 55, 160, "RULES OF THE GAME: \n  To jump press SPACE \n  "
            "To move use the key arrows \n  To kill enemies, kick their platform \n  once they're turned, touch them",
            5)
            pyxel.text (55, 195, "You only have 3 lives. GOOD LUCK!", 5)

        # Print the game screen 
        if (self.stage > 0 and self.stage < 5) and self.mario.lifes > 0:
            # Pipes
            for index in range(len(self.pipes)):
                pyxel.blt(self.pipes[index].x, self.pipes[index].y, *self.pipes[index].sprite)
            
            # Platforms
            for index in range(len(self.platforms)):
                pyxel.blt(self.platforms[index].x, self.platforms[index].y, *self.platforms[index].sprite)

            # Pow
            if self.pow.uses < 3:
                pyxel.blt(self.pow.x, self.pow.y, *self.pow.sprite)

            # Coins 
            for index in range(len(self.coins)):
                pyxel.blt(self.coins[index].x, self.coins[index].y, *self.coins[index].sprite)

            # Mario
            if self.mario.killed == False and self.pause == False:
                pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
            elif self.mario.killed == True:
                pyxel.blt(self.mario.x, self.mario.y, *(0, 112, 0, 16, 24))

            # Enemies
            for index in range (len(self.enemies)):
                pyxel.blt (self.enemies[index].x, self.enemies[index].y, *self.enemies[index].sprite)
                
        # Game over screen and win screen
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


    
    def __sprite_platforms (self):
        """ Manages the appearance of the platforms according to the stage of the game"""
        for index in range (len(self.platforms)):
            if self.stage == 1:
                sprite = (0, 8, 232, 8, 8)
            elif self.stage == 2:
                sprite = (0, 8, 224, 8, 8)
            elif self.stage == 3:
                sprite = (0, 0, 224, 8, 8)
            elif self.stage == 4:
                sprite = (0, 0, 232, 8, 8)
            self.platforms[index].sprite = sprite
            
            
    def __number_of_enemies (self):
        """ Manages the number of enemies that will appear according to the stage of the game"""
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
        """ Generates a list of platforms for the game """
        
        list_of_platforms = []
        y = 80
        for i in range(2):
            x = 0
            for j in range(12):
                list_of_platforms.append(Platform(x, y))
                x += 8
            y += 92
        y = 80
        for i in range(2):
            x = self.width
            for j in range(12):
                list_of_platforms.append(Platform(x, y))
                x -= 8
            y += 92
        x = 0
        for i in range(6):
            list_of_platforms.append(Platform(x, 127))
            x += 8
        x = self.width
        for i in range(6):
            list_of_platforms.append(Platform(x, 127))
            x -= 8
        x = 102
        for i in range(12):
            list_of_platforms.append(Platform(x, 127))
            x += 8
        return list_of_platforms
    
    
    def __generate_enemies (self):
        """ Generates enemies at random positions and of random types"""

        # Manage the appearance position of the enemies
        position = random.randint(0, 1)
        if position == 0:
            x = self.pipes[0].x + 56
            y = self.pipes[0].y
        elif position == 1:
            x = self.pipes[1].x - 16
            y = self.pipes[1].y
            
        # Generate enemies of different types
        if self.stage < 3:
            number = random.randint(1,2)
        else:
            number = random.randint(1, 3)
        # Enemies creation intercal    
        if self.enemy_counter % self.enemy_interval == 0:
            if number == 1:
                enemy = Turtles(x,y)
            elif number == 2:
                enemy = Crab(x,y)
            elif number == 3:
                enemy = Flies(x,y)
            return enemy
        
    def __generate_coins (self):
        """ Management of the random appearance of coins through the game"""
        x = random.randint(10, 220)
        
        # avoid appearance at unreachable positions
        if x + 8 >= self.pow.x and x <= self.pow.x + 16:
            x = random.randint (10, 210)
        y = random.randint(65, 160)
        if y + 10 >= self.pow.y and y <= self.pow.y + 16:
            y = random.randint(65, 160)
        for index in range (len(self.platforms)):
            if y + 12 >= self.platforms[index].y and y <= self.platforms[index].y + 8:
                if y > self.platforms[index].y:
                    y += 15
                elif y < self.platforms[index].y:
                    y -= 15

        coin = Coins(x, y)
        return coin

    def __game_pause (self):
        """ Manages Mario dead and pauses in the game"""
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
        """ Method to manage the restarting of the game """
        self.stage = 0
        self.mario.lifes = 3
        self.generated_enemies = False
        self.mario.points = 0
        self.pow.uses = 0
        self.pow.change_sprite()
        self.enemy_counter = 0
        self.enemies = []
        self.coins = []


    def mario_landed(self) -> bool:
        """ Method to manage the colision of Mario with walkable surfaces"""
        landed = False
        for index in range(len(self.platforms)):
            if (self.mario.y + self.mario.sprite[4] >= self.platforms[index].y and
                    self.mario.y + self.mario.sprite[4] <= self.platforms[index].y + self.platforms[index].sprite[4]):
                if (self.mario.x + 16 >= self.platforms[index].x and
                        self.mario.x <= self.platforms[index].x + self.platforms[index].sprite[3]):
                    landed = True
                    # Change sprite according to movement direction
                    if self.mario.direction == "right":
                        self.mario.sprite = (0, 0, 0, 16, 24, 0)
                    elif self.mario.direction == "left":
                        self.mario.sprite = (0, 0, 0, -16, 24, 0)
                    # Manage landing 
                    self.mario.y = self.platforms[index].y - self.mario.sprite[4]
                    self.mario.jump = False
                    self.mario.speed_y = 0
                    
        for index in range(len(self.floor)):
            if self.mario.y + self.mario.sprite[4] >= self.floor[index].y:
                landed = True
                if self.mario.direction == "right":
                    self.mario.sprite = (0, 0, 0, 16, 24, 0)
                elif self.mario.direction == "left":
                    self.mario.sprite = (0, 0, 0, -16, 24, 0)
                self.mario.y = self.floor[index].y - 24
                self.mario.jump = False
                self.mario.speed_y = 0
                
        # Manage the pow usage and its colision with mario
        if self.pow.uses < 3:
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
        """ Method to manage collisions with the platforms in case it hits them with the top of its head"""
        for index in range(len(self.platforms)):
            if (self.mario.y >= self.platforms[index].y and
                self.mario.y <= self.platforms[index].y + self.platforms[index].sprite[4]):
                if (self.mario.x + 16 > self.platforms[index].x and
                    self.mario.x < self.platforms[index].x + self.platforms[index].sprite[3]):
                    self.mario.y = self.platforms[index].y + self.platforms[index].sprite[4]
                    # We apply the force of gravity to fall back 
                    self.mario.speed_y = 0
                    i = 0
                    touches = 1

                    while i < len(self.enemies):
                        if (self.enemies[i].y + self.enemies[i].sprite[4] >= self.platforms[index].y and
                            self.enemies[i].y + self.enemies[i].sprite[4] <= self.platforms[index].y + self.platforms[index].sprite[4]):
            
                            if (self.enemies[i].x + 16 >= self.platforms[index].x and
                                self.enemies[i].x <= self.platforms[index].x + self.platforms[index].sprite[3]):
                                
                                if isinstance(self.enemies[i], Turtles):
                                    self.enemies[i].turn_sprite()
                                elif isinstance(self.enemies[i], Crab):
                                    touches += 1
                                    if touches == 2:
                                        self.enemies[i].turn_sprite()
                                elif isinstance(self.enemies[i], Flies):
                                    self.enemies.pop(i)
                                    
                                    self.mario.points += 200
                        i += 1
    
    def mario_pow(self):
        """ Method to apply collision with the pow logic"""
        if self.pow.uses < 3:
            
            if (self.mario.y >= self.pow.y and self.mario.y <= self.pow.y + self.pow.sprite[4]):
                if (self.mario.x + 16 > self.pow.x and self.mario.x < self.pow.x + self.pow.sprite[3]):
                    # Apply landing logic
                    self.mario.speed_y = 0
                    
                    self.mario.y = self.pow.y + self.pow.sprite[4]
                    self.pow.uses += 1
                    self.pow.change_sprite()
                    
                    index = 0
                    while index < len(self.enemies):
                        if isinstance(self.enemies[index], Turtles) or  isinstance(self.enemies[index], Crab):
                            self.enemies[index].turn_sprite()
                        else:
                            # Manage movement stop when we touch the pow
                            self.enemies.pop(index)
                        index += 1
    
    def enemy_landed(self, enemy: object):
        """ Method to control landings of enemies following the exact logic as Mario's one"""
        landed = False
        for index in range(len(self.platforms)):
            if (enemy.y + enemy.sprite[4] >= self.platforms[index].y and
                enemy.y + enemy.sprite[4] <= self.platforms[index].y + self.platforms[index].sprite[4]):
                if enemy.x + 16 >= self.platforms[index].x and enemy.x <= self.platforms[index].x + self.platforms[index].sprite[3]:
                    landed = True
                    enemy.y = self.platforms[index].y - 16
                    enemy.speed_y = 0

        for index in range(len(self.floor)):
            if enemy.y + enemy.sprite[4] >= self.floor[index].y:
                landed = True
                enemy.y = self.floor[index].y - enemy.sprite[4]
                enemy.speed_y = 0
        return landed
    
    def enemy_pipes(self, enemy: object):
        """ Method to control the collisions of enemies with the pipes"""
        
        if ((self.pipes[2].y < enemy.y < self.pipes[2].y + self.pipes[2].sprite[4]) or
                (self.pipes[3].y < enemy.y < self.pipes[3].y + self.pipes[3].sprite[4])):
            if (enemy.x <= self.pipes[2].x + self.pipes[2].sprite[3]) or (enemy.x + 16 >= self.pipes[3].x):
                # Manage appearance at a random upper pipe
                number = random.randint(0, 1)
                
                if number == 0:
                    enemy.x = self.pipes[0].x + self.pipes[0].sprite[3]
                    enemy.y = self.pipes[0].y
                elif number == 1:
                    enemy.x = self.pipes[1].x - 16
                    enemy.y = self.pipes[1].y

    def enemy_enemy(self):
        """ Method to manage collsions between enemies """
        collision = False
        for i in range(len(self.enemies)):
            for j in range(len(self.enemies)):
                # Make sure not to check the same enemies
                if i != j and collision == False:
                    
                    if self.enemies[i].x + 16 >= self.enemies[j].x and self.enemies[i].x <= self.enemies[j].x:
                        if (self.enemies[i].y >= self.enemies[j].y and
                            self.enemies[i].y + self.enemies[i].sprite[4] <= self.enemies[j].y + self.enemies[j].sprite[4]):
                            collision = True
                            # If collision occurs they go to opposite directions
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
                                    
    def mario_enemy(self):
        """ Manage collisions between Mario and the enemies"""
        index = 0
        while index < len(self.enemies) and self.mario.killed == False:
            # Check equal position
            if self.enemies[index].x <= self.mario.x + 16 and self.enemies[index].x + 16 >= self.mario.x:
                if (self.enemies[index].y >= self.mario.y and
                    self.enemies[index].y + self.enemies[index].sprite[4]<= self.mario.y + self.mario.sprite[4]):
                    # Manage killing the enemies
                    if self.enemies[index].turned == True:
                        if isinstance(self.enemies[index], Turtles) or isinstance(self.enemies[index], Crab):
                            self.enemies[index].killed()
                        # Point addition according to the enemy type
                        if isinstance(self.enemies[index], Turtles):
                            self.mario.points += 100
                            
                        elif isinstance(self.enemies[index], Crab):
                            self.mario.points += 300
                        self.enemies.pop(index)
                        self.number_enemies -= 1
                        
                    # Manage Mario death
                    elif self.enemies[index].turned == False:
                        if self.enemies[index].x < self.mario.x:
                            self.mario.x = self.enemies[index].x + 17
                        else:
                            self.mario.x = self.enemies[index].x - 17
                        self.mario.killed = True
                        self.mario.lifes -= 1
                        self.pause = True
            index += 1

    def mario_coins (self):
        """ Method to manage how coins are being catched by Mario"""
        index = 0
        
        while index < len(self.coins):
            if self.mario.x + 16 >= self.coins[index].x and self.mario.x <= self.coins[index].x + self.coins[index].sprite[3]:
                if (self.coins[index].y >= self.mario.y and
                    self.coins[index].y + self.coins[index].sprite[4] <= self.mario.y + self.mario.sprite[4]):
                    self.mario.points += 500
                    self.coins.pop(index)
            index += 1
