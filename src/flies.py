#This is the class of the flies
#Flies move by jumping so to be flipped they have to be touching the platform
import random


class Flies:
    def __init__(self, x, y):
        start_direction = random.randint(0,1)
        if start_direction == 0:
            self.direction = "left"
            sprite = (0, 16, 56, 16, 16, 0)
        elif start_direction == 1:
            self.direction = "right"
            sprite = (0, 16, 56, -16, 16, 0)
        self.sprite = sprite
        self.x = x
        self.y = y
        speed_x = 2
        self.speed_x = speed_x
        #I add a negative speed so that the fly jumps upwards
        speed_y = -5
        self.speed_y = speed_y
        #This is an attribute that controls if the fly is touching the platform
        self.landed = False
        #This other attribute controls that the enemy has been killed
        self.jumping = True

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x) -> float:
        if type(x) != int and type(x) != float:
            raise TypeError
        elif x > 300:
            self.__x = 0
        elif x < 0:
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
    @property
    def jumping (self) -> bool:
        return self.__jumping
    @jumping.setter
    def jumping (self, jumping) -> bool:
        if type (jumping) != bool:
            raise TypeError
        else:
            self.__jumping = jumping

    def __str__(self):
        return "Crab"
    def __repr__(self):
        return self.__str__()


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
        return "Fly"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.sprite == other.sprite, self.x == other.x, self.y == other.y, self.speed_x == other.speed_x,
                self.speed_y == other.speed_y)


    def move (self):
        if self.landed == True:
            self.jumping = True

        # If the enemy moves to the left, then we substract the value of the speed
        if self.direction == "left":
            self.x -= self.speed_x
            self.sprite = (0, 16, 56, 16, 16, 0)
        # If the enemy moves to the right, then we add the value of the speed
        elif self.direction == "right":
            self.x += self.speed_x
            self.sprite = (0, 16, 56, -16, 16, 0)

    def gravity (self):
        if self.landed == False:
            # This is the acceleration due to the force of gravity
            self.speed_y += 1
            # This is what varies the value of the position y
            self.y += self.speed_y

    def back_to_life (self):
        if self.time_turned > 80:
            self.sprite = (0, 120, 144, 16, 16, 0)
            self.speed_x = 2
            self.turned = False
            self.time_turned = 0