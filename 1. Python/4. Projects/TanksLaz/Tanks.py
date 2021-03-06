from email import message
import pygame
import random
import math

#ep65

#initializes the pygame module
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Tanks')

#icon = pygame.image.load("Apple.png")
#pygame.display.set_icon(icon) # best size for this is 32x32
#img = pygame.image.load("SnakeHead.png")
#appleimg = pygame.image.load("Apple.png")

white = (255,255,255)
black = (0,0,0)

red = (200,0,0)
light_red = (255,0,0)

green = (0,155,0)
light_green = (0,255,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5

clock = pygame.time.Clock()

block_size = 20
appleThic = 30

smallfont = pygame.font.SysFont("Verdana",25)
medfont = pygame.font.SysFont("Verdana",40)
largefont = pygame.font.SysFont("Verdana",65)

def pause():
  paused = True

  message_to_screen("Paused", black, -100, size = "large")
  message_to_screen("Press C to continue or Q to quit.", black, 25)
  pygame.display.update()

  while paused:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
          paused = False

        if event.key == pygame.K_q:
          pygame.quit()
          quit()
    
    #gameDisplay.fill(white)
    clock.tick(5)

def score(score):
  text = smallfont.render("Score: " +str(score) ,True, black)
  gameDisplay.blit(text, [0,0])

def barrier(xlocation,randomHeight, barrier_width):
  pygame.draw.rect(gameDisplay, black, [xlocation, display_height-randomHeight,barrier_width, randomHeight])


def game_intro():

  intro = True

  while intro:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
          intro = False

        if event.key == pygame.K_q:
          pygame.quit()
          quit()

    gameDisplay.fill(white)
    message_to_screen("Welcome to Tanks!", green, -100, "large")
    message_to_screen("The objective is to shoot and destroy the ", black, -30)
    message_to_screen("enemy tank before they destroy you", black, 10)
    #message_to_screen("Press C to play, P to pause or Q to quit", black, 100)

    button("play", 150,500,100,50, green, light_green, action="play")
    button("controls", 350,500,100,50, yellow, light_yellow,action = "controls")
    button("quit", 550,500,100,50, red, light_red, action = "quit")


    pygame.display.update()
    clock.tick(15)

def text_to_button(msg, color, buttonx,buttony,buttonw,buttonh, size ="small"):
  textSurf, textRect = text_objects(msg,color,size)
  textRect.center = ((buttonx+(buttonw/2), buttony + (buttonh/2)))
  gameDisplay.blit(textSurf, textRect)

def text_objects(text,color,size):
  if size == "small":
    textSurface = smallfont.render(text,True,color)
  elif size == "medium":
    textSurface = medfont.render(text,True,color)
  elif size == "large":
    textSurface = largefont.render(text,True,color)

  return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace = 0, size = "small"):
  #screen_text = font.render(msg, True, color)
  #gameDisplay.blit(screen_text, [display_width/3, display_height/2])
  textSurf, textRect = text_objects(msg,color,size)
  textRect.center = (display_width/2), (display_height/2) + y_displace
  gameDisplay.blit(textSurf, textRect)

def tank(x,y,turPos):
  x = int(x)
  y = int(y)

  possibleTurrets = [(x-27, y-2),(x-26,y-5),(x-25,y-8),(x-23,y-12),(x-20,y-14),
                      (x-18,y-15),(x-15,y-17),(x-13,y-19),(x-11,y-21)]

  pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
  pygame.draw.rect(gameDisplay,black,(x-tankHeight,y, tankWidth, tankHeight))

  pygame.draw.line(gameDisplay,black,(x,y), possibleTurrets[turPos], turretWidth)

  startX = 15
  for i in range(7):
    pygame.draw.circle(gameDisplay,black,(x-startX, y+17), wheelWidth)
    startX -=5

def button(text, x,y,w,h,inactive_color, active_color, action = None):
  cur = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  if x + w > cur[0] > x and y + h > cur[1] > y:
    pygame.draw.rect(gameDisplay, active_color, (x,y,w,h))
    if click[0] == 1 and action != None:
      if action == "quit":
        pygame.quit()
        quit()

      if action == "controls":
        game_controls()

      if action == "play":
        gameLoop()

      if action == "menu":
        game_intro()

  else:
    pygame.draw.rect(gameDisplay, inactive_color, (x,y,w,h))

  text_to_button(text,black,x,y,w,h)

def game_controls():

  gcont = True

  while gcont:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      
    gameDisplay.fill(white)
    message_to_screen("Controls", green, -100, "large")
    message_to_screen("Fire: Spacebar ", black, -30)
    message_to_screen("Move turret: up and down arrows", black, 10)
    message_to_screen("Move Tank: Left and Right arrows", black, 50)
    message_to_screen("Pause: P", black, 90)

    button("play", 150,500,100,50, green, light_green, action="play")
    button("menu", 350,500,100,50, yellow, light_yellow,action = "menu")
    button("quit", 550,500,100,50, red, light_red, action = "quit")


    pygame.display.update()
    clock.tick(15)

def gameLoop():
  gameExit = False
  gameOver = False

  xlocation = (display_width/2) + random.randint(-0.2 * display_width, 0.2 * display_width)
  randomHeight = random.randrange(display_height*0.1, display_height*0.6)
  barrier_width = 50

  mainTankX = display_width * 0.9
  mainTankY = display_height * 0.9

  tankMove = 0

  currentTurPos = 0
  changeTur = 0

  fps = 15

  while not gameExit:

    if gameOver == True:
      message_to_screen("Game over", red, -50, size="large")
      message_to_screen("Press C to play again or Q to quit", black, 50, size="medium")
      pygame.display.update()

    while gameOver == True:
      #gameDisplay.fill(white)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          gameOver = False
          gameExit = True

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            gameExit = True
            gameOver = False
          if event.key == pygame.K_c:
            gameLoop()

    #events part of loop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gameExit = True

      #any keydown
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            tankMove = -5

        elif event.key == pygame.K_RIGHT:
          tankMove = 5

        elif event.key == pygame.K_UP:
          changeTur = 1

        elif event.key == pygame.K_DOWN:
          changeTur = -1
        
        elif event.key == pygame.K_p:
          pause()
      
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          tankMove = 0
        
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          changeTur = 0


    gameDisplay.fill(white)

    # logic

    mainTankX += tankMove
    currentTurPos = currentTurPos + changeTur

    if currentTurPos > 8:
      currentTurPos = 8
    elif currentTurPos < 0:
      currentTurPos = 0

    if mainTankX - (tankWidth/2) < xlocation + barrier_width:
      mainTankX += 5
    

    tank(mainTankX,mainTankY,currentTurPos)

    barrier(xlocation, randomHeight, barrier_width)

    pygame.display.update()
    clock.tick(fps)

  pygame.quit()
  quit()

game_intro()
gameLoop()