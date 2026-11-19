import pygame
pygame.init()


class Wire():
  def __init__(self,location,facing,map):
    self.__location = location
    self.__map = map 
    self.__map.Place(self.__location,self)
    self.__connections = [0,0]
    self.__resistance = 1
    self.__current = 0
    self.__facing = facing
  def __str__(self,):
    return "wire"

  def resistance(self):
    return self.__resistance

  def setRessistance(self,value):
    self.__resistance = value
  def connect(self):
    col,row = self.__location
    grid = self.__map.Grid()

    directions = {
      "UP" : ((0,-1),"DOWN"),
      "DOWN" : ((0,1),"UP"),
      "RIGHT" : ((1,0),"LEFT"),
      "LEFT" : ((-1,0),"RIGHT")
    }
    self.__connections = [None,None]
    for idx,direction in enumerate(self.__facing):
      opperations,opposite = directions[direction]
      x,y = opperations
      targetColumn = col + x
      targetRow = row + y
      if (0 <= targetRow <= self.__map.Height() and 0 <= targetColumn <= self.__map.Columns()):
        target = grid[targetColumn][targetRow]
      else:
        target = None

      if target:
        if isinstance(target,Battery):
          target.connectWire(self)
          self.__connections[idx] = target
        elif isinstance(target,Wire):
          if opposite in target.facing():
            self.__connections[idx] = target
        elif isinstance(target,Gate):
          self.__connections[idx] = target

  def connections(self):
    return self.__connections

  def Current(self):
    return self.__current
  
  def location(self):
    return self.__location
  
  def turnWire(self):
    clockwise = {
      "UP" : "RIGHT",
      "RIGHT" : "DOWN",
      "DOWN" : "LEFT",
      "LEFT" : "UP"
    }
    for f,face in enumerate(self.__facing):
      self.__facing[f] = clockwise[face]
    self.__map.updateWires()
  def changeCurrent(self):
    self.__current = self.__current ^ 1
  def facing(self):
    return self.__facing
  def bendWire(self):
    bends = {
      "UP" : "DOWN",
      "DOWN" : "UP",
      "LEFT" : "RIGHT",
      "RIGHT" : "LEFT"
    }
    if self.__facing[0] == bends[self.__facing[1]]:
      if self.__facing[0] == "UP" or self.__facing[0] == "DOWN":
        self.__facing[1] = "RIGHT"
      elif self.__facing[0] == "LEFT" or self.__facing[0] == "RIGHT":
        self.__facing[1] = "UP"
    else:
      self.__facing[1] = bends[self.__facing[0]] 

class Resistor(Wire):
  def __init__(self,location,facing,map,resistance):
    super().__init__(location,facing,map)
    super().setRessistance(resistance)

class Battery():
  def __init__(self,charge,map,location):
    self.__location = location
    self.__map = map
    self.__charge = charge
    self.__map.Place(self.__location,self)
    self.__wiresConnected = []

  def discharge(self):
    if self.__wiresConnected:
      return self.__charge/len(self.__wiresConnected)
    else:
      return self.__charge
  def location(self):
    return self.__location
  def connectWire(self,wire):
    if wire not in self.__wiresConnected and wire:
      self.__wiresConnected.append(wire)
  def disconnect(self,wire):
    if wire in self.__wiresConnected:
      self.__wiresConnected.remove(wire)
  def connections(self):
    return self.__wiresConnected
  
class Gate():
  def __init__(self, location, map,chargerequired):
    self.__location = location
    self.__map = map
    self.__map.Place(self.__location,self)
    self.__chargerequired = chargerequired
    self.__opened = False
    self.__needed = self.__chargerequired
  def checkOpened(self,charge):
    if charge == self.__chargerequired:
      self.__opened = True
    else:
      self.__opened = False
    self.__needed = self.__chargerequired - charge
  def opened(self):
    return self.__opened

  def Needed(self):
    return self.__needed

  def reset(self):
    self.__needed = self.__chargerequired
    self.__opened = False
