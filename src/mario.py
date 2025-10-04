""" This module contains the Mario class """

class Mario :
    def __init__(self, x, y):
        self.x = x
        self.y = y
        jump = False
        self.jump = jump
        sprite = (0, 0, 0, 16, 24, 0)
        self.sprite = sprite
        speed_x = 2.5
        self.speed_x = speed_x
        speed_y = 0
        self.speed_y = speed_y
        direction = "right"
        self.direction = direction
        lifes = 3
        self.lifes = lifes
        killed = False
        self.killed = killed
        points = 0
        self.points = points

    @property
    def x (self) -> float:
        return self.__x
    
    @x.setter
    def x (self, x) -> float:
        if type(x) != int and type(x) != float:
            raise TypeError
        elif x> 300 - 16:
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
        elif y > 230 - 24:
            raise ValueError
        elif y < 0:
            raise ValueError
        else:
                self.__y = y

    @property
    def jump (self) -> bool:
        return self.__jump
    
    @jump.setter
    def jump (self, jump) -> bool:
        if type (jump) != bool:
            raise TypeError
        else:
            self.__jump = jump

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
    def lifes (self) -> int:
        return self.__lifes
    
    @lifes.setter
    def lifes (self, lifes) -> int:
        if type(lifes) != int:
            raise TypeError
        elif lifes < 0 :
            raise ValueError
        else:
            self.__lifes = lifes
            
    @property
    def killed (self) -> bool:
        return self.__killed
    
    @killed.setter
    def killed (self, killed) -> bool:
        if type (killed) != bool:
            raise TypeError
        else:
            self.__killed = killed
            
    @property
    def points (self) -> int:
        return self.__points
    
    @points.setter
    def points (self, points):
        if type(points) != int:
            raise TypeError
        elif points < 0:
            raise ValueError
        else:
            self.__points = points
            
    def __str__(self):
        return "Mario"
    def __repr__(self):
        return self.__str__()
    def __eq__(selfself, other):
        return (self.sprite == other.sprite, self.x == other.x, self.y == other.y,
                self.points == other.points, self.lifes == other.lifes)

    def change_sprite (self):
        """ Manage sprite change according to movement """
        if self.sprite == (0, 0, 0, 16, 24, 0):
            self.sprite = (0, 16, 0, 16, 24, 0)
        elif self.sprite == (0, 16, 0, 16, 24, 0):
            self.sprite = (0, 0, 0, 16, 24, 0)
        elif self.sprite == (0, 0, 0, -16, 24, 0):
                self.sprite = (0, 16, 0, -16, 24, 0)
        elif self.sprite == (0, 16, 0, -16, 24, 0):
                self.sprite = (0, 0, 0, 16, -24, 0)
                
    def move(self):
        """ Manage the movement to the left and right of Mario """
        if self.direction == "right":
            self.x += self.speed_x
            self.sprite = (0, 0, 0, 16, 24, 0)
        elif self.direction == "left":
            self.x -= self.speed_x
            self.sprite = (0, 0, 0, -16, 24, 0)
        self.change_sprite()

    def jumping(self):
        """ Manage jumping logic """
        # Gravity speed
        self.speed_y += 1
        self.y += self.speed_y
        # Horizontal movement during jump
        if self.direction == "left":
            self.sprite = (0, 64, 0, -16, 24, 0)
            self.x -= self.speed_x
        elif self.direction == "right":
            self.sprite = (0, 64, 0, 16, 24, 0)
            self.x += self.speed_x

















