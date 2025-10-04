#This class contains the pipes
class Pipes:
    def __init__(self, x, y, side, style):
        #The pipes will be at the same place all program long
        #There are two types of pipes, those that look towards the right and are placed at the left of the screen
        #and those that look to the left and are at the right
        #we create an attribute x, that is where in the x axis the pipe will be placed
        self.x = x
        #Now the other attribute will be the height at which the pipe is placed
        self.y = y
        #I also create an attribute which determines where the pipe is placed and what is its style
        #We have to take into account that the position determines what is the actual sprite we are using
        sprite = ()
        if side == "right" and style == "complex":
            #This is the sprite position that corresponds to the pipe situated at the right
            sprite = (0, 56, 176, 56, 32)
        elif side == "left" and style == "complex":
            #This is the sprite position of the pipe situated at the left
            sprite = (0, 0, 176, 56, 32)
        elif side == "right" and style == "simple":
            #This is the sprite position that corresponds to the pipe situated at the right
            sprite = (0, 48, 184, 32, 22)
        elif side == "left" and style == "simple":
            #This is the sprite position of the pipe situated at the left
            sprite = (0, 32, 184, 32, 22)

        #Now I generate the attribute of teh sprite
        self.sprite = sprite



    @property
    def x (self) -> float:
        return self.__x
    @x.setter
    def x(self,x) -> float:
        if type(x) != float and type(x) != int:
            raise TypeError
        elif x > (300) or x < 0:
            #As I know which is the value of the width (300) in the game, I need to make sure that the pipes are
            #all the same length and are not getting ouside of the screen
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
            #As I know which is the value of the height (200) in the game, I need to make sure that the pipes are
            #all the same length and are not getting outside of the screen
            raise ValueError
        else:
            self.__y = y
    @property
    def side (self) -> str:
        return self.__side
    @side.setter
    def side(self, side) -> str:
        #The only sides at which the pipe might be positioned are the right and the left, other values would raise an error
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
        # The only sides at which the pipe might be positioned are the right and the left, other values would raise an error
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

