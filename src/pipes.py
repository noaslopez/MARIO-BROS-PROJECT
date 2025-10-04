""" This module contains the Pipes class """
class Pipes:
    def __init__(self, x, y, side, style):
        # Pipes will be static elements of the game 
        self.x = x
        self.y = y
        # The sprite is different according to position
        sprite = ()
        if side == "right" and style == "complex":
            sprite = (0, 56, 176, 56, 32)
        elif side == "left" and style == "complex":
            sprite = (0, 0, 176, 56, 32)
        elif side == "right" and style == "simple":
            sprite = (0, 48, 184, 32, 22)
        elif side == "left" and style == "simple":
            sprite = (0, 32, 184, 32, 22)

        self.sprite = sprite



    @property
    def x (self) -> float:
        return self.__x
    
    @x.setter
    def x(self,x) -> float:
        if type(x) != float and type(x) != int:
            raise TypeError
        elif x > (300) or x < 0:
            raise ValueError
        else:
            self.__x = x
            
    @property
    def y (self) -> float:
        return self.__y
    
    @y.setter
    def y (self, y:float):
        if type(y) != float and type(y) != int:
            raise TypeError
        elif y < 0  or y > (200):
            raise ValueError
        else:
            self.__y = y
            
    @property
    def side (self) -> str:
        return self.__side
    
    @side.setter
    def side(self, side) -> str:
        if type(side) != str:
            raise TypeError
        elif side != "right" and side != "left":
            raise ValueError("The only possible positions are right or left")
        else:
            self.__side = side

    @property
    def style(self) -> str:
        return self.__style

    @style.setter
    def style(self, style) -> str:
        if type(style) != str:
            raise TypeError
        elif style != "simple" and style != "complex":
            raise ValueError("The only possible styles are simple or complex")
        else:
            self.__style = style

    def __str__(self):
        return "Pipe"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.sprite == other.sprite, self.side == other.side)

