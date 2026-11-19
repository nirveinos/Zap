import pygame
from mapManager import Map,Wall
from puzzles import Wire,Battery,Gate
from Player import Player
from puzzleManager import runLevel
width,height = 800,600
running = True
test = True
pygame.init()
display = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.update()
mymap = Map(10,9)
battery = Battery(10,mymap,(0,0))
player = Player(mymap)
wire1 = Wire((1, 0), ["LEFT", "RIGHT"], mymap,1)
wire2 = Wire((2, 0), ["LEFT", "DOWN"], mymap,2)
wire3 = Wire((2, 1), ["UP", "DOWN"], mymap,3)
wire4 = Wire((2,2),["UP","DOWN"], mymap,4)
wire5 = Wire((2,3),["UP","RIGHT"],mymap,5)
wire6 = Wire((3,3),["LEFT","UP"],mymap,6)
wire7 = Wire((3,2),["DOWN","UP"],mymap,7)
gate = Gate((3,1),mymap,3)
wall1 = Wall(mymap,(1,1))
mymap.updateWires()
previous = []
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        for wire in battery.connections():
          battery.disconnect(wire)
        mymap.updateWires()
        if test:
          won,previous = runLevel(mymap)
          test = False
        else:
          for wire in previous:
            wire.changeCurrent()
          gate.reset()
          test = True
        if won:
          running = True
      if event.key == pygame.K_a:
        player.move((-1,0))
      elif event.key == pygame.K_w:
        player.move((0,-1))
      elif event.key == pygame.K_d:
        player.move((1,0))
      elif event.key == pygame.K_s:
        player.move((0,1))
      elif event.key == pygame.K_r:
        if test:
          px,py = player.Position()
          item = mymap.Grid()[px][py]
          if isinstance(item,Wire):
            item.turnWire()
      elif event.key == pygame.K_b:
        if test:
          px,py = player.Position()
          item = mymap.Grid()[px][py]
          if isinstance(item,Wire):
            item.bendWire()

  display.fill("black")
  mymap.drawGrid(display)
  player.drawPlayer(display)
  pygame.display.update()
