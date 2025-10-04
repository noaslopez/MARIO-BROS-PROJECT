#This is the class that corresponds to the floor of the game

class Floor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        sprite = (0, 120, 176, 16, 16)
        self.sprite = sprite

    @property
    def x (self) -> float:
        return self.__x
    @x.setter
    def x(self, x: float) -> float:
        if type(x) != int and type(x) != float:
            raise TypeError
        elif x < 0 or x > 300:
            raise ValueError("The platforms cannot be placed outside the screen")
        else:
            self.__x = x

    @property
    def y (self) -> float:
        return  self.__y
    @y.setter
    def y (self, y:float) -> float:
        if type(y) != int and type(y) != float:
            raise TypeError
        elif y < 0 or y > 230 - 16:
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
        elif sprite != (0, 120, 176, 16, 16):
            raise ValueError
        else:
            self.__sprite = sprite

    def __str__(self):
        return "floor"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.sprite == other.sprite, self.x == other.x , self.y == other.y)
