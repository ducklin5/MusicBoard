import pygame
import random

https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/

pygame.init()

myFont = pygame.font.SysFont("Times New Roman", 18)

display_width=1024
display_height=960

points = 0

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grey = (128,128,128)


gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Music Board')
clock = pygame.time.Clock()

def score(points,health):
    pointsDisplay = myFont.render(str(points), 1, black)
    healthDisplay = myFont.render(str(health), 1, red)
    gameDisplay.blit(pointsDisplay, (display_width * 0.9,display_height * 0.9))
    gameDisplay.blit(healthDisplay, (display_width * 0.9,display_height * 0.1))


#def enemy(x1,y1):
#    gameDisplay.blit(enemy1, (x1,y1))

def walkRight(xStick,yStick,frame):
    xStickChange = +10
    xStick = xStick + xStickChange
    if frame == 1:
        gameDisplay.blit(StickWalk1, (xStick,yStick))
    elif frame == 2:
        gameDisplay.blit(StickWalk2, (xStick,yStick))
    elif frame == 3:
        gameDisplay.blit(StickWalk3, (xStick,yStick))
    elif frame == 4:
        gameDisplay.blit(StickWalk4, (xStick,yStick))
    elif frame == 5:
        gameDisplay.blit(StickWalk5, (xStick,yStick))
    frame = frame + 1
    if frame > 5:
        frame = 1
    return xStick,yStick,frame

def walkLeft(xStick,yStick,frame):
    xStickChange = -10
    xStick = xStick + xStickChange
    if frame == 1:
        gameDisplay.blit(pygame.transform.flip(StickWalk1, True, False), (xStick,yStick))
    elif frame == 2:
        gameDisplay.blit(pygame.transform.flip(StickWalk2, True, False), (xStick,yStick))
    elif frame == 3:
        gameDisplay.blit(pygame.transform.flip(StickWalk3, True, False), (xStick,yStick))
    elif frame == 4:
        gameDisplay.blit(pygame.transform.flip(StickWalk4, True, False), (xStick,yStick))
    elif frame == 5:
        gameDisplay.blit(pygame.transform.flip(StickWalk5, True, False), (xStick,yStick))
    frame = frame + 1
    if frame > 5:
        frame = 1
    return xStick,yStick,frame

def punchRight(xStick,yStick,frame,stickPunch,stickPunchLatch):
    if frame == 1:
        gameDisplay.blit(StickPunch1, (xStick,yStick))
    elif frame == 2:
        gameDisplay.blit(StickPunch2, (xStick,yStick))
    elif frame == 3:
        gameDisplay.blit(StickPunch3, (xStick,yStick))
    elif frame == 4:
        gameDisplay.blit(StickPunch4, (xStick,yStick))
    elif frame == 5:
        gameDisplay.blit(StickPunch5, (xStick,yStick))
    elif frame == 6:
        gameDisplay.blit(StickPunch6, (xStick,yStick))
    frame = frame + 1
    if frame > 6:
        stickPunch = False
        stickPunchLatch = True
        frame = 1
    return frame,stickPunch,stickPunchLatch

def punchLeft(xStick,yStick,frame,stickPunch,stickPunchLatch):
    if frame == 1:
        gameDisplay.blit(pygame.transform.flip(StickPunch1, True, False), (xStick,yStick))
    elif frame == 2:
        gameDisplay.blit(pygame.transform.flip(StickPunch2, True, False), (xStick,yStick))
    elif frame == 3:
        gameDisplay.blit(pygame.transform.flip(StickPunch3, True, False), (xStick,yStick))
    elif frame == 4:
        gameDisplay.blit(pygame.transform.flip(StickPunch4, True, False), (xStick,yStick))
    elif frame == 5:
        gameDisplay.blit(pygame.transform.flip(StickPunch5, True, False), (xStick,yStick))
    elif frame == 6:
        gameDisplay.blit(pygame.transform.flip(StickPunch6, True, False), (xStick,yStick))
    frame = frame + 1
    if frame > 6:
        stickPunch = False
        stickPunchLatch = True
        frame = 1
    return frame,stickPunch,stickPunchLatch

def stick(xStick,yStick,frame,stickStance,stickPunch,stickPunchLatch):
    if (stickPunch == True and stickPunchLatch == False):
        print("Punch!")
        if stickStance == "R":
            frame,stickPunch,stickPunchLatch = punchRight(xStick,yStick,frame,stickPunch,stickPunchLatch)
        elif stickStance == "L":
            frame,stickPunch,stickPunchLatch = punchLeft(xStick,yStick,frame,stickPunch,stickPunchLatch)

    else:
        if (stickRight == True and stickLeft == False and xStick <= 620):
            print(xStick)
            xStick,yStick,frame = walkRight(xStick,yStick,frame)

        elif (stickLeft == True and stickRight == False and xStick >= -120):
            print(xStick)
            xStick,yStick,frame = walkLeft(xStick,yStick,frame)

        else:
            xStickChange = 0
            gameDisplay.blit(Stick, (xStick,yStick))
    return xStick,yStick,frame,stickStance,stickPunch,stickPunchLatch


    


xStick = 0
yStick = 160
xStickChange = 0
yStickChange = 0
frame = 1
health = 100
points = 0
stickLeft = False
stickRight = False
stickStance = "R"
stickPunch = False
stickPunchLatch = False
while health >= 0:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                stickLeft = True
                stickStance = "L"
            if event.key == pygame.K_RIGHT:
                stickRight = True
                stickStance = "R"
            if (event.key == pygame.K_SPACE and stickPunchLatch == False):
                stickPunch = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                stickLeft = False
                frame = 1
            if event.key == pygame.K_RIGHT:
                stickRight = False
                frame = 1
            if event.key == pygame.K_SPACE:
                stickPunch = False
                stickPunchLatch = False
                frame = 1

    gameDisplay.fill(white)        
    xStick,yStick,frame,stickStance,stickPunch,stickPunchLatch = stick(xStick,yStick,frame,stickStance,stickPunch,stickPunchLatch)
    score(points,health)
    pygame.display.update()
    clock.tick(30)

pygame.quit
quit()