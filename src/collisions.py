""" Manage collisions in the game and their effects"""
import random

class Collisions:
    
    def mario_landed(self):
        """ Mario landing on platforms, floor and pow"""
        landed = False
        for index in range(len(self.platforms)):
            if self.mario.y + 24 >= self.platforms[index].y and self.mario.y + 24 <= self.platforms[index].y + 8:
                if self.mario.x + 16 >= self.platforms[index].x and self.mario.x <= self.platforms[index].x + 8:
                    landed = True
                    # Change sprite according to the direction
                    if self.mario.direction == "right":
                        self.mario.sprite = (0, 0, 0, 16, 24, 0)
                    elif self.mario.direction == "left":
                        self.mario.sprite = (0, 0, 0, -16, 24, 0)
                    # Allow walkning on the platform 
                    self.mario.y = self.platforms[index].y - 24
                    
                    self.mario.jump = False
                    self.mario.speed_y = 0
                    
        # Manage landing on the floor
        for index in range(len(self.floor)):
            if self.mario.y + 24 >= self.floor[index].y:
                landed = True
                if self.mario.direction == "right":
                    self.mario.sprite = (0, 0, 0, 16, 24, 0)
                elif self.mario.direction == "left":
                    self.mario.sprite = (0, 0, 0, -16, 24, 0)
                self.mario.y = self.floor[index].y - 24
                self.mario.jump = False
                self.mario.speed_y = 0
        
        # Pow management
        if self.pow.uses < 3:
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
        """ Control the collisions with platforms """
        for index in range(len(self.platforms)):
            if (self.mario.y >= self.platforms[index].y and self.mario.y <= self.platforms[index].y + 8):
                if (self.mario.x + 16 > self.platforms[index].x and self.mario.x < self.platforms[index].x + 8):
                    # Apply gravity again
                    self.mario.y = self.platforms[index].y + 8
                    self.mario.speed_y = 0
                    for i in range(len(self.enemies)):
                        times = 0
                        if (self.enemies[i].y + 16 >= self.platforms[index].y and
                                self.enemies[i].y + 16 <= self.platforms[index].y + 8):
                            if (self.enemies[i].x + 16 >= self.platforms[index].x and
                                    self.enemies[i].x <= self.platforms[index].x + 8):
                                self.enemies[i].turn_sprite()

    
    def mario_kicked_pow(self):
        """ Manage kicking the pow platform """
        if self.pow.uses < 3:
            if (self.mario.y >= self.pow.y and self.mario.y <= self.pow.y + 16):
                if (self.mario.x + 16 > self.pow.x and self.mario.x < self.pow.x + 8):
                    # Manage gravity again
                    self.mario.speed_y = 0
                    
                    self.mario.y = self.pow.y + 16
                    self.pow.uses += 1
                    self.pow.change_sprite()
                    
                    for i in range(len(self.enemies)):
                        self.enemies[i].turn_sprite()

    def enemy_landed(self, enemy: object):
        """ Enemies landing exact replica of Marios """
        landed = False
        # Platform landing
        for index in range(len(self.platforms)):
            if enemy.y + 16 >= self.platforms[index].y and enemy.y + 16 <= self.platforms[index].y + 8:
                if enemy.x + 16 >= self.platforms[index].x and enemy.x <= self.platforms[index].x + 8:
                    landed = True
                    enemy.y = self.platforms[index].y - 16
                    enemy.speed_y = 0

        # Floor landing
        for index in range(len(self.floor)):
            if enemy.y + 16 >= self.floor[index].y:
                landed = True
                enemy.y = self.floor[index].y - 16
                enemy.speed_y = 0
        return landed

    def enemy_pipes(self, enemy: object):
        """ Manage interaction between enemies and pipes """
        if ((self.pipes[2].y < enemy.y < self.pipes[2].y + 22) or
                (self.pipes[3].y < enemy.y < self.pipes[3].y + 22)):
            if (enemy.x <= self.pipes[2].x + 32) or (enemy.x + 16 >= self.pipes[3].x):
                # Random appearance at an upper pipe 
                number = random.randint(0, 1)
                # Rightt pipe
                if number == 0:
                    enemy.x = self.pipes[0].x + 56
                    enemy.y = self.pipes[0].y
                # Left pipe
                elif number == 1:
                    enemy.x = self.pipes[1].x - 16
                    enemy.y = self.pipes[1].y


    def enemy_enemy(self):
        """ Manage enemy-to-enemy collisions """
        collision = False
        for i in range(len(self.enemies)):
            for j in range(len(self.enemies)):
                if i != j and collision == False:
                    if self.enemies[i].x + 16 >= self.enemies[j].x and self.enemies[i].x <= self.enemies[j].x:
                        if self.enemies[i].y >= self.enemies[j].y and self.enemies[i].y + 16 <= self.enemies[j].y + 16:
                            collision = True
                            # After collision the must go on opposite directions
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


