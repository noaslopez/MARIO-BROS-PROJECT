#This class manages the collisions between the different elements of the game
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
class Collisions:
    # METHODS RELATED TO THE MOVEMENTS OF MARIO
    def mario_landed(self):
        landed = False
        for index in range(len(self.platforms)):
            # This first condition controls that mario is on the same position of the y axis as the platforms
            if self.mario.y + 24 >= self.platforms[index].y and self.mario.y + 24 <= self.platforms[index].y + 8:
                # this second condition checks that mario is on the same position of the x axis as the platforms
                # it could have been written on the same condition but this is a bit easier to read and comprehend
                if self.mario.x + 16 >= self.platforms[index].x and self.mario.x <= self.platforms[index].x + 8:
                    landed = True
                    # this changes the sprite according to what is necessary
                    if self.mario.direction == "right":
                        self.mario.sprite = (0, 0, 0, 16, 24, 0)
                    elif self.mario.direction == "left":
                        self.mario.sprite = (0, 0, 0, -16, 24, 0)
                    # this sets the position of mario to that of teh platform so that it can walk there
                    self.mario.y = self.platforms[index].y - 24
                    # now this two expressions make mario stop moving vertically (falling) because it has fallen fully
                    self.mario.jump = False
                    self.mario.speed_y = 0
        # This code controls when mario lands on the floor
        for index in range(len(self.floor)):
            # in this one we only check the y because the floor oes all along the x axis so checking that is not needed
            if self.mario.y + 24 >= self.floor[index].y:
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
            if self.mario.y + 24 >= self.pow.y and self.mario.y + 24 <= self.pow.y + 16:
                if self.mario.x + 16 >= self.pow.x and self.mario.x <= self.pow.x + 16:
                    landed = True
                    if self.mario.direction == "right":
                        self.mario.sprite = (0, 0, 0, 16, 24, 0)
                    elif self.mario.direction == "left":
                        self.mario.sprite = (0, 0, 0, -16, 24, 0)
                    self.mario.y = self.pow.y - 24
                    self.mario.jump = False
                    self.mario.speed_y = 0
        return landed

    def mario_kicked_platform(self):
        # This method controls the collisons with the platforms
        # In this method I also have to control that if mario kicks a platform and an enemy is placed just where he has
        # kicked, then, the enemy should turn around so that it can be killed
        for index in range(len(self.platforms)):
            # This condition controls that the coordinates of mario are those that correspond to the platform
            if (self.mario.y >= self.platforms[index].y and self.mario.y <= self.platforms[index].y + 8):
                if (self.mario.x + 16 > self.platforms[index].x and self.mario.x < self.platforms[index].x + 8):
                    # This will let us handle how many times has mario touched the platform and allow us to work better
                    self.mario.y = self.platforms[index].y + 8
                    # Once mario has hit the platform we turn his velocity on the y axis to 0  so that when then we
                    # apply on him the force of gravity so that he falls back down
                    self.mario.speed_y = 0
                    # now here I control that if there is an enemy in that same position, the enemy is turned around
                    for i in range(len(self.enemies)):
                        times = 0
                        if (self.enemies[i].y + 16 >= self.platforms[index].y and
                                self.enemies[i].y + 16 <= self.platforms[index].y + 8):
                            if (self.enemies[i].x + 16 >= self.platforms[index].x and
                                    self.enemies[i].x <= self.platforms[index].x + 8):
                                self.enemies[i].turn_sprite()

    # We apply the same logic than we have applied in the previous method to the pow, however this has to be done on a
    # different method because of the specific things that touching the pow imply
    def mario_kicked_pow(self):
        # This condition will control that the pow only works for a maximum of 3 times as according to the rules
        if self.pow.uses < 3:
            # This condition controls that the coordinates of mario are those that correspond to the platform
            if (self.mario.y >= self.pow.y and self.mario.y <= self.pow.y + 16):
                if (self.mario.x + 16 > self.pow.x and self.mario.x < self.pow.x + 8):
                    # Once mario has hit the platform we turn his velocity on the y axis to 0  so that when then we
                    # apply on him the force of gravity so that he falls back down
                    self.mario.speed_y = 0
                    # I have to add this because otherwise the program will count all the time that mario is on that position
                    # interval and that would make it very difficult to control the actual times it has touched the pow
                    self.mario.y = self.pow.y + 16
                    self.pow.uses += 1
                    self.pow.change_sprite()
                    # now here I control that if there is an enemy in that same position, the enemy is turned around
                    for i in range(len(self.enemies)):
                        self.enemies[i].turn_sprite()

    # the relation with the platforms and elements on the game logic of the enemies is similar to the one of mario
    def enemy_landed(self, enemy: object):
        landed = False
        for index in range(len(self.platforms)):
            # This first condition controls that the enemy is on the same position of the y axis as the platforms
            if enemy.y + 16 >= self.platforms[index].y and enemy.y + 16 <= self.platforms[index].y + 8:
                # this second condition checks that the enemy is on the same position of the x axis as the platforms
                # it could have been written on the same condition but this is a bit easier to read and comprehend
                if enemy.x + 16 >= self.platforms[index].x and enemy.x <= self.platforms[index].x + 8:
                    landed = True
                    # this sets the position of enemy to the position platform so that it can move
                    enemy.y = self.platforms[index].y - 16
                    # this makes the enemy to stop falling
                    enemy.speed_y = 0

        # this does the same but with the floor
        for index in range(len(self.floor)):
            # in this one we only check the y because the floor oes all along the x axis so checking that is not needed
            if enemy.y + 16 >= self.floor[index].y:
                landed = True
                enemy.y = self.floor[index].y - 16
                enemy.speed_y = 0
        return landed

    # this method its the one that controls that when the enemies touch a lower pipe, they have to appear on an
    # upper pipe
    def enemy_pipes(self, enemy: object):
        # the upper pipes are in positions 1 and 0, and the lower pipes in positions 2 and 3 of the pipes list
        # the lower one on the right side is position 2, and the lower one on the left side is position 3
        # their width is 32, and their height is 22
        # first, I control that they are on the same x position as the pipes
        if ((self.pipes[2].y < enemy.y < self.pipes[2].y + 22) or
                (self.pipes[3].y < enemy.y < self.pipes[3].y + 22)):
            # next, I control that they are on the same y position, I do it separately because they are easier to read
            if (enemy.x <= self.pipes[2].x + 32) or (enemy.x + 16 >= self.pipes[3].x):
                # Now I generate a random number between 0 and 1 so that the enemy appears at a random upper pipe
                # The 0 is the pipe on the right and the 1 is the pipe on the left
                number = random.randint(0, 1)
                # this makes the enemy to reapear on the upper pipe of the right
                if number == 0:
                    enemy.x = self.pipes[0].x + 56
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
                        if self.enemies[i].y >= self.enemies[j].y and self.enemies[i].y + 16 <= self.enemies[j].y + 16:
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


