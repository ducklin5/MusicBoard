import pygame
import serialReader
import synthEngine as se
from threading import Thread

# inputs to be used
inputs = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
          "11": 0, "12": 0, "13": 0, "22": 0, "23": 0, "25": 0, "27": 0, "29": 0, "31": 0}


class SynthUI():

    def __init__(self):
        self.synth = se.Synth()
        self.synthPlot = None
        self.lfoPlot = None
        self.filterPlot = None
        self.adsrPlot = None
        self.updatePlots()
        self.lastPiano = [0] * 12  # Initializes piano keys

    def doSomeChange(self):
        # change the wave Here
        # - > Do CHANGE
        # Update plot
        self.updatePlots()
        pass

    def playKeys(self, Piano, octavenum):

        for i in range(len(Piano)):
            state = (Piano[i], self.lastPiano[i])
            if state == (1, 0):
                self.synth.play(se.midi(i + octavenum))
            elif state == (0, 1):
                self.synth.release(se.midi(i + octavenum))
        self.lastPiano = Piano

    def drawPiano(self, gameDisplay, Piano, pKey, pianoPosx, pianoPosy):      
        i = 0
        while i < len(Piano):
            if Piano[i]==1:
                gameDisplay.blit(pKey[i],(pianoPosx,pianoPosy))
            i+=1

    def drawUI(self, gameDisplay):
        plotPosx = 100
        plotPosy = 100
        gameDisplay.blit(self.synthPlot, (0 + plotPosx, 0 + plotPosy))
        gameDisplay.blit(self.lfoPlot,  (210 + plotPosx, 0 + plotPosy))
        gameDisplay.blit(self.filterPlot, (420 + plotPosx, 0 + plotPosy))
        gameDisplay.blit(self.adsrPlot, (630 + plotPosx, 0 + plotPosy))

    def updatePlots(self):
        self.synthPlot = self.synth.draw(440, 200, 200, 50)
        self.filterPlot = self.synth.ffilter.draw(200, 200, 50)
        self.lfoPlot = self.synth.lfo.draw(200, 200, 50)
        self.adsrPlot = self.synth.adsr.draw(200, 200, 50)

def run():
    global inputs
    # import your script B
    pygame.init()

    myFont = pygame.font.SysFont("Times New Roman", 18)

    display_width = 947
    display_height = 609

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
    xButton1 = 10
    yButton1 = 500
    xButton2 = 210
    yButton2 = 500
    xBoxBackground = 1
    yBoxBackground = 1

    thePiano = pygame.image.load('images/piano.png')
    pianoPosx = 680
    pianoPosy = 400
    pKey = [0] * 12
    pKey[0] = pygame.image.load('images/pianoC.png')
    pKey[1] = pygame.image.load('images/pianoCS.png')
    pKey[2] = pygame.image.load('images/pianoD.png')
    pKey[3] = pygame.image.load('images/pianoDS.png')
    pKey[4] = pygame.image.load('images/pianoE.png')
    pKey[5] = pygame.image.load('images/pianoF.png')
    pKey[6] = pygame.image.load('images/pianoFS.png')
    pKey[7] = pygame.image.load('images/pianoG.png')
    pKey[8] = pygame.image.load('images/pianoGS.png')
    pKey[9] = pygame.image.load('images/pianoA.png')
    pKey[10] = pygame.image.load('images/pianoAS.png')
    pKey[11] = pygame.image.load('images/pianoB.png')    

    octaveTitle = pygame.image.load('images/octaveTitle.png')
    octavenum = 72
    # initialize synth fonts
    # i = 0
    # synthFonts=[]
    # while i < 20:
    #     synthFonts[i] = myFont.render('Synth {}'.format(i),
    #     i+=1
    #myFont.render('Synth {}').format(i)

    synth1UI = SynthUI()

    while not quit:
        Piano = [0] * 12
        Piano[0] = (inputs["2"])  # C
        Piano[1] = (inputs["3"])  # C sharp
        Piano[2] = (inputs["4"])  # D
        Piano[3] = (inputs["5"])  # D sharp
        Piano[4] = (inputs["6"])  # E
        Piano[5] = (inputs["7"])  # F
        Piano[6] = (inputs["8"])  # F sharp
        Piano[7] = (inputs["9"])  # G
        Piano[8] = (inputs["10"])  # G sharp
        Piano[9] = (inputs["11"])  # A
        Piano[10] = (inputs["12"])  # A sharp
        Piano[11] = (inputs["13"])  # B

        LeftButton = (inputs["23"])
        RightButton = (inputs["22"])

        gameDisplay.blit(BoxBackground, (xBoxBackground, yBoxBackground))
        gameDisplay.blit(thePiano,(pianoPosx,pianoPosy))
        gameDisplay.blit(octaveTitle,(10,390))
        if LeftButton:
            gameDisplay.blit(Button1Pressed, (xButton1,yButton1))
            octavenum = octavenum - 12
            pygame.time.delay(250) #prevents skipping octaves
        else:
            gameDisplay.blit(Button1, (xButton1,yButton1))

        if RightButton:
            gameDisplay.blit(Button1Pressed, (xButton2,yButton2))
            octavenum = octavenum + 12
            pygame.time.delay(250) #prevents skipping octaves
        else:
            gameDisplay.blit(Button1, (xButton2,yButton2))
        ####
        ###########

        # if PianoA:
        #     #gameDisplay.blit(Button1Pressed,(xButton1,yButton1))
        #     se.myK(Synth1,69)

        # if PianoAS
        # else:
        # gameDisplay.blit(Button1,(xButton1,yButton1))
        synth1UI.drawUI(gameDisplay)
        synth1UI.playKeys(Piano, octavenum)
        synth1UI.drawPiano(gameDisplay, Piano, pKey, pianoPosx, pianoPosy)
        pygame.display.update()
        clock.tick(30)

    pygame.quit
    quit()


Thread(target=serialReader.run, args=("/dev/ttyACM0", inputs, True)).start()
Thread(target=run).start()