import pygame
from mapManager import Map,Wall
from puzzles import Wire,Battery,Gate,Resistor
from Player import Player
from MenuManager import StartingScreen,getInputs,LevelMenu
from levelmanager import loadLevel,levels
from puzzleManager import runLevel
width,height = 800,600
started = False
running = True
test = True
won = False
pygame.init()
display = pygame.display.set_mode((width, height),pygame.RESIZABLE)
previous = []
while not started:
  started = StartingScreen(display)
if started == "quit":
  running = False
while running:
  levelNumber=LevelMenu(display)
  
  if levelNumber:
    display.fill("black")
    mymap,player,battery,gate = loadLevel(levelNumber)
    pygame.display.flip()
    levelrunning = True
  else:
    running = False
    break
  while levelrunning:
    running,test,previous,won = getInputs(player,battery,mymap,gate,test,previous,won)      
    display.fill("black")
    mymap.drawGrid(display)
    player.drawPlayer(display)
    pygame.display.update()
    if won:
      if player.Position() == gate.Position():
        levels[levelNumber]["completed"] = True
        levelrunning = False
    if not running:
      break



