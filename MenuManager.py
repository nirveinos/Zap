import pygame
from puzzleManager import runLevel
from puzzles import Wire
from levelmanager import levels
pygame.init()
buttonClick = pygame.mixer.Sound("Assets/buttonClick.mp3")
def StartingScreen(display):
    pygame.mixer.init()
    
    startButton = pygame.image.load("Assets/playButton.png")
    startx = 100
    starty = 47
    startingButtonx = ((800-100)/2)
    startingButtony = ((600-50)/2)
    button = pygame.Rect(startingButtonx, startingButtony, startx, starty)
    pygame.display.set_caption("Starting Screen")
    font = pygame.font.Font("Assets/ElectricKicksItalic-PKW5g.ttf",128)
    logo = font.render("ZAP!",True,"white")

    started = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            started = "quit"
            return started
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                buttonClick.play()
                started = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
    display.fill("black")
    display.blit(startButton,(startingButtonx,startingButtony))
    display.blit(logo,(275,100))
    pygame.display.flip()
    return started
    

def getInputs(player,battery,mymap,gate,test,previous,won):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return False,True,previous,won
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
              return True,test,previous,won
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
          elif event.key == pygame.K_F11:
             pygame.display.toggle_fullscreen()
    return True,test,previous,won

def LevelMenu(display):
    pygame.mixer.init()
    buttons = {}
    closeButton = pygame.Rect(730,30,30,30)
    
    for i, levelNumber in enumerate(levels.keys()):
        
        if int(levelNumber) <= 4:
           y = 100
           x = 50 + 200 * i
        elif int(levelNumber) <=8: 
           y = 200
           x = 50 + 200 * (i - 4)
        else:
           y = 300
           x = 50+ 200 * (i-8)
        buttons[levelNumber] = pygame.Rect(x, y, 50, 50)

    font = pygame.font.Font(None, 36)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                for levelNumber, button in buttons.items():
                    if button.collidepoint(event.pos):
                        buttonClick.play()
                        print(levelNumber)
                        return levelNumber
                if closeButton.collidepoint(event.pos):
                   return None
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_F11:
                  pygame.display.toggle_fullscreen()
        display.fill("black")

        for levelNumber, button in buttons.items():
            colour = "blue"
            if levels[levelNumber]:
                if levels[levelNumber]["completed"]:
                    colour = "green"
            pygame.draw.rect(display, colour, button)
            pygame.draw.circle(display,"red",(745,45),15)

            text = font.render(
                f"Level {levelNumber}", True, "white"
            )

            display.blit(text, text.get_rect(center=button.center))

        pygame.display.flip()
   