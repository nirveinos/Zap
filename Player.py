import pygame
pygame.init()
from mapManager import Wall
class Player():
    def __init__(self,map):
        self.__position = (0,0)
        self.__sizex = map.Height()
        self.__map = map
        self.__sizey = map.Columns()#
        self.__offsetx,self.__offsety = map.Offset()
        self.__cellSize = map.cellSize()
        self.__grid = [[0 for _ in range(self.__sizey)] for _ in range(self.__sizex)]
        self.__grid[0][0] = 1
        self.numrows = (800/self.__cellSize)-1
        self.numcols = (600/self.__cellSize)-1
    def move(self, direction):
        dx, dy = direction
        row, col = self.__position

        new_row = row + dx
        new_col = col + dy
        if (0 <= new_row < len(self.__grid) and
            0 <= new_col < len(self.__grid[0]) and not isinstance(self.__map.Grid()[new_row][new_col],Wall)):
            self.__position = (new_row, new_col)
            self.__grid[new_row][new_col] = 1
            if self.__position[0] > self.numrows:
                self.__map.setOffset(0,-100)
                self.numrows += 1
            elif self.__position[0] < (self.numrows-(800/self.__cellSize)+1):
                self.__map.setOffset(0,100)
                self.numrows -= 1
            elif self.__position[1] < (self.numcols - (600/self.__cellSize)+1):
                self.__map.setOffset(100,0)
                self.numcols -= 1
            elif self.__position[1] > self.numcols:
                self.__map.setOffset(-100,0)
                self.numcols += 1               
            
    def drawPlayer(self,screen):
        plyer = pygame.Surface((25,25))
        plyer.fill("red")
        x,y = self.__position
        ox,oy = self.__map.Offset()
        screen.blit(plyer,(x* self.__cellSize + self.__offsetx + ox, y * self.__cellSize + self.__offsety + oy))

    def __str__(self):
        return str(self.__grid)

    def Position(self):
        return self.__position