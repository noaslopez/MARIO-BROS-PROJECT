""" This module contains the Platform class """

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #In the stage 0 we have the basic brown platforms
        sprite = (0, 8, 232, 8, 8, 0)
        self.sprite = sprite

    @property
    def x (self) -> float:
        return self.__x
    @x.setter
    def x (self, x:float) -> float:
        if type (x) != int and type(x) != float:
            raise TypeError
        elif x < 0 or x > 300:
            raise ValueError ("The platforms cannot be placed outside the screen")
        else:
            self.__x = x
    @property
    def y (self) -> float:
        return self.__y
    @y.setter
    def y (self, y:float) -> float:
        if type(y) != int and type(y) != float:
            raise TypeError
        elif y < 0 or y > 230 - 8:
            raise ValueError ("The platforms cannot be placed outside the screen")
        else:
            self.__y = y

    @property
    def sprite (self) -> tuple:
        return self.__sprite
    @sprite.setter
    def sprite (self, sprite) -> tuple:
        if type(sprite) != tuple:
            raise TypeError
        else:
            self.__sprite = sprite

    def __str__ (self):
        return "Platform"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.x == other.x, self.y == other.y, self,sprite == other.sprite)






