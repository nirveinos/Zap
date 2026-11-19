import pygame
import math
from puzzles import Wire,Battery,Gate
from mapManager import Map
pygame.init()

def findStarting(mymap):
  grid = mymap.Grid()
  for row in grid:
    for cell in row:
      if type(cell) == Battery:
        return cell

def runLevel(mymap):
  battery = findStarting(mymap)
  connections = battery.connections()
  check = -1
  for wire in connections:
    wireConnections = wire.connections()
    
    check = 1 ^ wireConnections.index(battery)
    currentWire = wire
    
    Charge = math.floor(battery.discharge())
    done = [currentWire]
    while Charge > 0:
      if currentWire:
        if isinstance(currentWire,Gate):
          currentWire.checkOpened(Charge)
          if currentWire.opened():
            return True,done
          else:
            return False,done
        Charge -= currentWire.resistance()
        currentWire.changeCurrent()
        if currentWire.connections()[check]:
          if currentWire.connections()[check] in done:
            check = 1 ^ check
          
          currentWire = currentWire.connections()[check]
          if isinstance(currentWire,Wire):
            done.append(currentWire)
          
        else:
          return False,done
      else:
        return False,done
    return False,done
  return False,[]
