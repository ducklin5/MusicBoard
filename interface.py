import pygame
import serialReader
from threading import Thread

# inputs to be used
inputs = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "22": 0, "23": 0, "25": 0, "27": 0, "29": 0, "31": 0}


def run():
    global inputs
    prevInputs = {}
    # import your script B
    pygame.init()

    myFont = pygame.font.SysFont("Times New Roman", 18)

    display_width=947
    display_height=609

    points = 0

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    gray = (128, 128, 128)

    gameDisplay = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('Music Board')
    clock = pygame.time.Clock()
    # print(pygame.image.get_extended())
    BoxBackground = pygame.image.load('images/BoxBackground.png')
    Button1 = pygame.image.load('images/Button1.png')
    Button1Pressed = pygame.image.load('images/Button1Pressed.png')
    Knob1 = pygame.image.load('images/Knob1.png')
    quit = False

    xKnob1 = 500
    yKnob1 = 250
    xButton1 = 1
    yButton1 = 1
    xBoxBackground = 1
    yBoxBackground = 1
    gameDisplay.fill(gray)
    
    while not quit:
        b1Pressed = (inputs["13"])
        gameDisplay.blit(BoxBackground,(xBoxBackground,yBoxBackground))
        if b1Pressed:
            gameDisplay.blit(Button1Pressed, (xButton1, yButton1))
        else:
            gameDisplay.blit(Button1, (xButton1, yButton1))
        
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        prevInputs = inputs
        pygame.display.update()
        clock.tick(30)

    pygame.quit
    quit()


Thread(target=serialReader.run, args=("/dev/ttyACM0", inputs)).start()
Thread(target=run).start()
