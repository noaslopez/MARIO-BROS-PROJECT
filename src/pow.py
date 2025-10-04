""" This module contains the Pow class """

class Pow :
    def __init__(self,x,y):
        self.x = x
        self.y = y
        # Initially, the pow has not been used 
        self.uses = 0
        self.sprite = (0, 136, 176, 16, 16, 0)

    @property
    def x (self) -> float:
        return self.__x
    
    @x.setter
    def x (self, x) -> float:
        if type(x) != float and type(x) != int:
            raise TypeError
        elif x < 0 or x > 300 - 16:
            raise ValueError ("The pow element cannot be ouside the screen")
        else:
            self.__x = x
            
    @property
    def y (self) -> float:
        return self.__y
    
    @y.setter
    def y (self, y:float) -> float:
        if type (y) != float and type(y) !=int:
            raise TypeError
        elif y<0 or y>300-16:
            raise ValueError ("The pow element cannot be outside the screen")
        else:
            self.__y = y
            
    @property
    def uses (self) -> int:
        return self.__uses
    
    @uses.setter
    def uses (self, uses) -> int:
        if type(uses) != int:
            raise TypeError
        elif uses < 0 or uses > 3:
            raise ValueError
        else:
            self.__uses = uses
    def __str__(self):
        return "Pow"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.sprite == other.sprite, self.uses == other.uses)


    def change_sprite(self):
        """ Change the size of the pow according to how many times it has been used """
        if self.uses == 0:
            self.sprite = (0, 136, 176, 16, 16, 0)
        if self.uses == 1:
            self.sprite = (0, 152, 176, 16, 16, 0)
        elif self.uses == 2:
            self.sprite = (0, 168, 176, 16, 16, 0)





