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

with open("SaveFile.txt","r",encoding="utf-8") as f:
  for line in f:
    level,completed = line.split(",")
    if levels[int(level)]:
      levels[int(level)]["completed"] = bool(int(completed))
      print(levels[int(level)]["completed"])
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((width, height))
previous = []
pygame.mixer.music.load("Assets/Soundtrack.mp3")
pygame.mixer.music.play(-1,0,26000)

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
    flags = pygame.display.get_surface().get_flags()
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


with open("SaveFile.txt","w",encoding="utf-8") as f:
  for num,data in levels.items():
    if levels[num]:
      f.write(f"{num},{int(levels[num]["completed"])}")

