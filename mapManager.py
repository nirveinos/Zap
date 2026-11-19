import pygame
from puzzles import Battery,Wire,Gate,Resistor
pygame.init()

class Map():
  def __init__(self,sizex,sizey):
    self.__x = sizex
    self.__y = sizey
    self.__grid = [[0 for _ in range(sizey)] for _ in range(sizex)]
    self.__cellSize = 100
    self.__offsety = 0
    self.__offsetx = 0
  def Grid(self):
    return self.__grid
  
  def Height(self):
    return self.__x

  def Offset(self):
    return [self.__offsetx,self.__offsety]

  def cellSize(self):
    return self.__cellSize

  def setOffset(self,y,x):
    self.__offsetx += x
    self.__offsety += y
  def Place(self,coordinates,puzzle):
    x,y = coordinates
    if self.__grid[x][y]:
      return
    self.__grid[x][y] = puzzle

  def Columns(self):
    return self.__y
  
  def __str__(self):
    return str(self.__grid)

  def updateWires(self):
    for row in self.__grid:
      for thing in row:
        if isinstance(thing,Wire):
          thing.connect()
  def drawGrid(self,screen):
    for row in range(self.__y + 1):
      y = (row * self.__cellSize) + self.__offsety
      pygame.draw.line(screen, "white", (self.__offsetx, y), (self.__offsetx + self.__x * self.__cellSize, y), 1)

    for col in range(self.__x + 1):
      x = col * self.__cellSize + self.__offsetx
      pygame.draw.line(screen, "white", (x, self.__offsety), (x, self.__offsety + self.__y * self.__cellSize), 1)

    for r,row in enumerate(self.__grid):
      for i,item in enumerate(row):
        if item:
          if isinstance(item,Wire):
            if item.Current():
              colour = "green"
            else:
              if isinstance(item,Resistor):
                colour = "coral3"
              else:
                colour = "blue"
            for direction in item.facing():
              match direction:
                case "LEFT":
                  ox = 0
                  oy = (self.__cellSize - 10) / 2
                  size = (self.__cellSize / 2, 10)
                case "RIGHT":
                  ox = self.__cellSize / 2
                  oy = (self.__cellSize - 10) / 2
                  size = (self.__cellSize / 2, 10)
                case "DOWN":
                  oy = self.__cellSize / 2
                  ox = (self.__cellSize - 10) / 2
                  size = (10, self.__cellSize / 2)  
                case "UP":
                  oy = 0
                  ox = (self.__cellSize - 10) / 2
                  size = (10, self.__cellSize / 2)
              object = pygame.Surface(size)
              object.fill(colour)
              screen.blit(object,((r)*self.__cellSize +   self.__offsetx + ox,(i)*self.__cellSize + self.__offsety + oy))

          elif isinstance(item,Battery):
            object = pygame.Surface((60,60))
            object.fill("green")
            font = pygame.font.Font(None,32)
            text = font.render(f"{item.discharge()}", True ,"black")
            textpos = text.get_rect(centerx=self.__cellSize * (r) + self.__offsetx + 50, y=self.__cellSize * (i) + self.__offsety + 50)
            screen.blit(object,(self.__cellSize * (r) + self.__offsetx + 20,self.__cellSize * (i) + self.__offsety + 20))
            screen.blit(text,textpos)
          elif isinstance(item,Gate):
            object = pygame.Surface((60,60))
            if item.opened():
              object.fill("green")
            else:
              object.fill("white")
            font = pygame.font.Font(None,32)
            text = font.render(f"{item.Needed()}", True ,"black")
            textpos = text.get_rect(centerx=self.__cellSize * (r) + self.__offsetx + 50, y=self.__cellSize * (i) + self.__offsety + 50)
            screen.blit(object,(self.__cellSize * (r) + self.__offsetx + 20,self.__cellSize * (i) + self.__offsety + 20))
            screen.blit(text,textpos)
          elif isinstance(item,Wall):
            object = pygame.Surface((100,100))
            object.fill("purple")
            screen.blit(object,(self.__cellSize * r + self.__offsetx, self.__cellSize * i + self.__offsety))
class Wall():
  def __init__(self,map,position):
    self.__position = position
    self.__map = map
    self.__map.Place(position,self)
