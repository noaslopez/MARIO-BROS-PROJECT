#This is the class of the crab
#Crabs are fliped by being hit twice
import random

class Crab:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        start_direction = random.randint(0,1)
        if start_direction == 0:
            self.direction = "right"
        elif start_direction == 1:
            self.direction = "left"
        self.sprite = (0, 0, 40, 16, 16, 0)
        speed_x = 2
        self.speed_x = speed_x
        speed_y = 0
        self.speed_y = speed_y
        # This is an attribute that controls if the fly is touching the platform
        self.landed = False
        # This other attribute controls that the enemy has been killed
        self.turned = False
        self.time_turned = 0

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x (self, x) -> float:
        if type(x) != int and type(x) != float:
            raise TypeError
        elif x> 300:
            self.__x = 0
        elif x<0:
            self.__x = 300 - 16
        else:
            self.__x = x

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y) -> float:
        if type(y) != int and type(y) != float:
            raise TypeError
        elif y > 230 - 16:
            raise ValueError
        elif y < 0:
            raise ValueError
        else:
            self.__y = y


    @property
    def speed_x(self) -> float:
        return self.__speed_x

    @speed_x.setter
    def speed_x(self, speed_x) -> float:
        if type(speed_x) != int and type(speed_x) != float:
            raise TypeError
        else:
            self.__speed_x = speed_x

    @property
    def speed_y(self) -> float:
        return self.__speed_y

    @speed_y.setter
    def speed_y(self, speed_y) -> float:
        if type(speed_y) != int and type(speed_y) != float:
            raise TypeError
        else:
            self.__speed_y = speed_y

    @property
    def direction (self) -> str:
        return self.__direction
    @direction.setter
    def direction (self, direction) -> str:
        if type (direction) != str:
            raise TypeError
        elif direction != "right" and direction != "left":
            raise ValueError
        else:
            self.__direction = direction

    @property
    def landed (self) -> bool:
        return self.__landed
    @landed.setter
    def landed (self, landed) -> bool:
        if type(landed) != bool:
            raise TypeError
        else:
            self.__landed = landed
    @property
    def turned (self) -> bool:
        return self.__turned
    @turned.setter
    def turned (self, turned) -> bool:
        if type (turned) != bool:
            raise TypeError
        else:
            self.__turned = turned
    @property
    def time_turned (self) -> int:
        return self.__time_turned
    @time_turned.setter
    def time_turned (self, time_turned) -> int:
        if type(time_turned) != int:
            raise TypeError
        elif time_turned < 0:
            raise ValueError
        else:
            self.__time_turned = time_turned

    def __str__(self):
        return "Crab"
    def __repr__(self):
        return self.__str__()


    # METHODS:

    def move(self):
        if self.turned == False:
            # If the enemy moves to the left, then we substract the value of the speed
            if self.direction == "left":
                self.x -= self.speed_x
            # If the enemy moves to the right, then we add the value of the speed
            elif self.direction == "right":
                self.x += self.speed_x

    def gravity(self):
        # This is the acceleration due to the force of gravity
        self.speed_y += 1
        # This is what varies the value of the position y
        self.y += self.speed_y

    def turn_sprite (self):
        self.turned = True
        if self.sprite == (0, 0, 40, 16, 16, 0):
            self.sprite = (0, 168, 40, 16, 16, 0)
        elif self.sprite == (0, 120, 144, 16, 16, 0):
            self.sprite = (0, 168, 144, 16, 16, 0)
        self.speed_x = 0

    def back_to_life (self):
        if self.time_turned > 90:
            self.sprite = (0, 120, 144, 16, 16, 0)
            self.speed_x = 2
            self.turned = False
            self.time_turned = 0
    def killed (self):
        if self.sprite == (0, 168, 40, 16, 16, 0):
            self.sprite = (0, 80, 40, 8, 16, 0)
        elif self.sprite == (0, 120, 144, 16, 16, 0):
            self.sprite = (0, 80, 144, 16, 16, 0)



