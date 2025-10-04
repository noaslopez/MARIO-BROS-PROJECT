#This is the class that controls the coins that mario will take

class Coins:
    def __init__(self, x, y):
        self. x = x
        self.y = y
        sprite = (0 , 16, 212, 8, 12, 0)
        self. sprite = sprite
        self.change_time = 0

    @property
    def x (self) -> float:
        return self.__x
    @x.setter
    def x (self, x) -> float:
        if type(x) != int and type(x) != float:
            raise TypeError
        elif x < 0 or x > 300 - 8:
            raise ValueError
        else:
            self.__x = x
    @property
    def y (self) -> float:
        return self.__y
    @y.setter
    def y (self, y) -> float:
        if type(y) != float and type(y) != int:
            raise TypeError
        elif y < 0 or y > 230 - 10:
            raise ValueError
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

    #@property
    #def change_time

    def __str__(self):
        return "Coin"
    def __repr__(self):
        return self.__str__()


    #METHODS OF THE CLASS
    def change_sprite (self):
        if self.change_time%2 == 0:
            if self.sprite == (0 , 16, 212, 8, 12, 0):
                self.sprite = (0, 24, 212, 8, 12, 0)
            elif self.sprite == (0, 24, 212, 8, 12, 0):
                self.sprite = (0, 32, 212, 8, 12, 0)
            elif self.sprite == (0, 32, 212, 8, 12, 0):
                self.sprite = (0, 0, 212, 8, 12, 0)
            elif self.sprite == (0, 0, 212, 8, 12, 0):
                self.sprite = (0, 8, 212, 8, 12, 0)
            elif self.sprite == (0, 8, 212, 8, 12, 0):
                self.sprite = (0, 16, 212, 8, 12, 0)