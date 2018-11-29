import pygame
import random
from threading import Thread
import numpy as np
import os
import serial

b1Pressed = False
def serialReader(): 
    global b1Pressed
    ser = serial.Serial("/dev/ttyACM0", 19200)

    pins = {}
    while True:
        line = str(ser.readline())[2:][:-5]
        # print(line)
        line = line.split(":")
        pin = line[0]
        value = line[1]
        pins[pin] = int(value)
        print(pins)
        print('\n')
        if pins.get("8") == 0:
            b1Pressed = True
        elif pins.get("8") == 1:
            b1Pressed = False


def interface():
    global b1Pressed
    # import your script B
    pygame.init()

    myFont = pygame.font.SysFont("Times New Roman", 18)

    display_width=947
    display_height=609

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

    BoxBackground = pygame.image.load('images/BoxBackground.png')
    Button1 = pygame.image.load('images/Button1.png')
    Button1Pressed = pygame.image.load('images/Button1Pressed.png')
    Knob1 = pygame.image.load('images/Knob1.png')
    quit = False
    xKnob1 = 500
    yKnob1 = 250
    xButton1 = 1
    yButton1 = 1
    xBoxBackground = 0
    yBoxBackground = 0
    #gameDisplay.fill(grey)
    gameDisplay.blit(BoxBackground,(xBoxBackground,yBoxBackground))
    while quit == False:
        # gameDisplay.blit(BoxBackground,xBoxBackground,yBoxBackground)
        if b1Pressed == True:
            gameDisplay.blit(Button1Pressed,(xButton1,yButton1))
        else:
            gameDisplay.blit(Button1,(xButton1,yButton1))
        gameDisplay.blit(Knob1,(xKnob1,yKnob1))
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        # gameDisplay.blit(,,)
        pygame.display.update()
        clock.tick(30)

    pygame.quit
    quit()


Thread(target = serialReader).start() 
Thread(target = interface).start()

# https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/

