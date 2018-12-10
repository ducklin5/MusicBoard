# ---------------------------------------------------
#    Name: Azeez  Abass
#    ID: 1542780
#    Name: Matthew Braun
#    ID: 1497171
#    CMPUT 274 EA1, Fall  2018
#    Project: ZMat 2000 (Interface)
# ---------------------------------------------------

import pygame
import serialReader
import synthEngine as se
from threading import Thread

# inputs to be used
inputs = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
          "11": 0, "12": 0, "13": 0, "22": 0, "23": 0, "25": 0, "27": 0, "29": 0, "31": 0,
          "A0": 0, "A14": 0, "A15": 0}

# Loading font for text
pygame.font.init()
defaultFont = pygame.font.SysFont('ubuntumono', 50)
smallerFont = pygame.font.SysFont('ubuntumono', 30)
currentSynth = 1

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)


Volume = 1
# statemachine


def selectMode(j, JoystickButton, JoystickVer, JoystickHor, currentSynth, numSynths, synthUIs, state):
    if JoystickButton:
        pygame.time.delay(300) #prevents skipping selections
        if currentSynth == numSynths:
            synthUIs.append(SynthUI())
            numSynths = len(synthUIs)
            synthUIs[currentSynth - 1].name = defaultFont.render(
                "Synth {}".format(currentSynth), True, blue)
        else:
            state = 2
    if JoystickVer == 1000:
        if currentSynth == numSynths:
            currentSynth = 1
        else:
            currentSynth += 1
        pygame.time.delay(300)  # prevents skipping selections
    elif JoystickVer == 0:
        if currentSynth == 1:
            currentSynth = numSynths
        else:
            currentSynth -= 1
        pygame.time.delay(300)  # prevents skipping selections
    return j, state, currentSynth, numSynths


def selectGraphMode(JoystickButton, JoystickVer, JoystickHor, currentGraph, state):
    pygame.time.delay(300)  # prevents skipping modes
    if JoystickButton:
        if currentGraph[0] == 0:
            if currentGraph[1] == 0:
                state = 3  # Premixer Sound Wave Mode
            else:
                state = 4  # LFO Mode
        else:
            if currentGraph[1] == 0:
                state = 5  # Filter Mode
            else:
                state = 6  # ADSR Mode
    if JoystickVer == 1000 or JoystickVer == 0:
        currentGraph[1] = not currentGraph[1]
        pygame.time.delay(300)  # prevents skipping selections
    if JoystickHor == 1000 or JoystickHor == 0:
        currentGraph[0] = not currentGraph[0]
        pygame.time.delay(300)  # prevents skipping selections
    return state, currentGraph

def editSourcesMode(editingThisSource,Waves,updateSources,incrementValue,currentWaveForm,SourcesSelectList,WaveFormList,state,sources,currentSource,JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay):
    i = 0
    for string in SourcesSelectList:
        SourcesSelectString = smallerFont.render(string, True, blue)
        gameDisplay.blit(SourcesSelectString,(315,10+i))
        i+=40
    SourcesValueList = ['{}'.format(WaveFormList[currentWaveForm]),'{}'.format(sources[editingThisSource].scale),'{}'.format(sources[editingThisSource].shift),'{}'.format(len(sources)),'{}'.format(editingThisSource+1),'{}'.format(incrementValue),"Update","Back"]
    i = 0
    for value in SourcesValueList:
        SourcesSelectString = smallerFont.render(value, True, red)
        gameDisplay.blit(SourcesSelectString,(235,10+i))
        i+=40
    if RightButton:
        if currentSource == 0:
            if currentWaveForm >= len(WaveFormList)-1:
                currentWaveForm = 0
            else:
                currentWaveForm += 1
            sources[editingThisSource].form = Waves[currentWaveForm]
        elif currentSource == 1:
            sources[editingThisSource].scale = round(sources[editingThisSource].scale+incrementValue,3)
        elif currentSource == 2:
            sources[editingThisSource].shift = round(sources[editingThisSource].shift+incrementValue,3)
        elif currentSource == 3:
            sources.append(se.Oscillator())
        elif currentSource == 4:
            if editingThisSource >= len(sources)-1:
                editingThisSource = 0
            else:
                editingThisSource += 1

        elif currentSource == 5:
            if incrementValue >= 10:
                pass
            else:
                incrementValue = round(incrementValue*10,3)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if LeftButton:
        if currentSource == 0:
            if currentWaveForm <= 0:
                currentWaveForm = len(WaveFormList)-1
            else:
                currentWaveForm -= 1
            sources[editingThisSource].form = Waves[currentWaveForm]
        elif currentSource == 1:
            sources[editingThisSource].scale = round(sources[editingThisSource].scale-incrementValue,3)
        elif currentSource == 2:
            sources[editingThisSource].shift = round(sources[editingThisSource].shift-incrementValue,3)
        elif currentSource == 3:
            sources.append(se.Oscillator())
        elif currentSource == 4:
            if editingThisSource <= 0:
                editingThisSource = len(sources)-1
            else:
                editingThisSource -= 1

        elif currentSource == 5:
            if incrementValue <= 0.001:
                pass
            else:
                incrementValue = round(incrementValue/10,3)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickButton:
        if currentSource == 6:
            updateSources()
        elif currentSource == 7:
            updateSources()
            state = 1
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickVer == 1000:
        if currentSource == len(SourcesValueList)-1:
            currentSource = 0
        else:
            currentSource += 1
        pygame.time.delay(300) #prevents skipping selections
    elif JoystickVer == 0:
        if currentSource == 0:
            currentSource = len(SourcesValueList)-1
        else:
            currentSource -= 1
        pygame.time.delay(300) #prevents skipping selections
 
    # gameDisplay.blit(SourcesValueText,(220,10))

    return state, sources, currentSource, incrementValue, currentWaveForm, editingThisSource

def editFilterMode(incrementValue,FilterModeList,CurrentFilterMode,FilterSelectList,updateFilter,state,ffilter,currentFilter,JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay):    
    i = 0
    for string in FilterSelectList:
        FilterSelectString = smallerFont.render(string, True, blue)
        gameDisplay.blit(FilterSelectString,(315,10+i))
        i+=40
    FilterValueList = ['{}'.format(ffilter.mode),'{}'.format(ffilter.cuttoff),'{}'.format(ffilter.width),'{}'.format(ffilter.mix),'{}'.format(ffilter.enabled),'{}'.format(ffilter.repeats),'{}'.format(incrementValue),"Update","Back"]
    i = 0
    for value in FilterValueList:
        FilterSelectString = smallerFont.render(value, True, red)
        gameDisplay.blit(FilterSelectString,(235,10+i))
        i+=40
    if RightButton:
        if currentFilter == 0:
            if CurrentFilterMode >= len(FilterModeList)-1:
                CurrentFilterMode = 0
            else:
                CurrentFilterMode += 1
            ffilter.mode = FilterModeList[CurrentFilterMode]
        elif currentFilter == 1:
            ffilter.cuttoff = round(ffilter.cuttoff+incrementValue)
        elif currentFilter == 2:
            ffilter.width = round(ffilter.width+incrementValue)
        elif currentFilter == 3:
            ffilter.mix = round(ffilter.mix+incrementValue)
        elif currentFilter == 4:
            ffilter.enabled = not ffilter.enabled
        elif currentFilter == 5:
            ffilter.repeats = round(ffilter.repeats+incrementValue)
        elif currentFilter == 6:
            if incrementValue >= 10000:
                pass
            else:
                incrementValue = round(incrementValue*10)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if LeftButton:
        if currentFilter == 0:
            if CurrentFilterMode <= 0:
                CurrentFilterMode = len(FilterModeList)-1
            else:
                CurrentFilterMode -= 1
            ffilter.mode = FilterModeList[CurrentFilterMode]
        elif currentFilter == 1:
            ffilter.cuttoff = round(ffilter.cuttoff-incrementValue)
        elif currentFilter == 2:
            ffilter.width = round(ffilter.width-incrementValue)
        elif currentFilter == 3:
            ffilter.mix = round(ffilter.mix-incrementValue)
        elif currentFilter == 4:
            ffilter.enabled = not ffilter.enabled
        elif currentFilter == 5:
            ffilter.repeats = round(ffilter.repeats-incrementValue)
        elif currentFilter == 6:
            if incrementValue <= 1:
                pass
            else:
                incrementValue = round(incrementValue/10)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickButton:
        if currentFilter == 4:
            ffilter.enabled = not ffilter.enabled
        elif currentFilter == 7:
            updateFilter()
        elif currentFilter == 8:
            updateFilter()
            state = 1
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickVer == 1000:
        if currentFilter == len(FilterValueList)-1:
            currentFilter = 0
        else:
            currentFilter += 1
        pygame.time.delay(300) #prevents skipping selections
    elif JoystickVer == 0:
        if currentFilter == 0:
            currentFilter = len(FilterValueList)-1
        else:
            currentFilter -= 1
        pygame.time.delay(300) #prevents skipping selections
 
    # gameDisplay.blit(FilterValueText,(220,10))

    return state, ffilter, currentFilter, incrementValue, CurrentFilterMode

def editLFOMode(Waves,updateLFO,incrementValue,currentWaveForm,LFOSelectList,WaveFormList,state,lfo,currentLFO,JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay):
    i = 0
    for string in LFOSelectList:
        LFOSelectString = smallerFont.render(string, True, blue)
        gameDisplay.blit(LFOSelectString,(315,10+i))
        i+=40
    LFOValueList = ['{}'.format(WaveFormList[currentWaveForm]),'{}'.format(lfo.freq),'{}'.format(lfo.enabled),'{}'.format(lfo.mix),'{}'.format(incrementValue),"Update","Back"]
    i = 0
    for value in LFOValueList:
        LFOSelectString = smallerFont.render(value, True, red)
        gameDisplay.blit(LFOSelectString,(235,10+i))
        i+=40
    if RightButton:
        if currentLFO == 0:
            if currentWaveForm >= len(WaveFormList)-1:
                currentWaveForm = 0
            else:
                currentWaveForm += 1
            lfo.osc.form = Waves[currentWaveForm]
        elif currentLFO == 1:
            lfo.freq = round(lfo.freq+incrementValue,3)
        elif currentLFO == 2:
            lfo.enabled = not lfo.enabled
        elif currentLFO == 3:
            lfo.mix = round(lfo.mix+incrementValue,3)
        elif currentLFO == 4:
            if incrementValue >= 100:
                pass
            else:
                incrementValue = round(incrementValue*10,3)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if LeftButton:
        if currentLFO == 0:
            if currentWaveForm <= 0:
                currentWaveForm = len(WaveFormList)-1
            else:
                currentWaveForm -= 1
            lfo.osc.form = Waves[currentWaveForm]
        elif currentLFO == 1:
            lfo.freq = round(lfo.freq-incrementValue,3)
        elif currentLFO == 2:
            lfo.enabled = not lfo.enabled
        elif currentLFO == 3:
            lfo.mix = round(lfo.mix-incrementValue,3)
        elif currentLFO == 4:
            if incrementValue <= 0.001:
                pass
            else:
                incrementValue = round(incrementValue/10,3)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickButton:
        if currentLFO == 2:
            lfo.enabled = not lfo.enabled
        elif currentLFO == 5:
            updateLFO()
        elif currentLFO == 6:
            updateLFO()
            state = 1
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickVer == 1000:
        if currentLFO == len(LFOValueList)-1:
            currentLFO = 0
        else:
            currentLFO += 1
        pygame.time.delay(300) #prevents skipping selections
    elif JoystickVer == 0:
        if currentLFO == 0:
            currentLFO = len(LFOValueList)-1
        else:
            currentLFO -= 1
        pygame.time.delay(300) #prevents skipping selections
 
    # gameDisplay.blit(LFOValueText,(220,10))

    return state, lfo, currentLFO, incrementValue, currentWaveForm

def editADSRMode(ADSRSelectList,incrementValue,updateADSR,adsr,JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay,state,currentADSR):
    ADSRValueList = ['{}'.format(adsr.Adur),'{}'.format(adsr.ADval),'{}'.format(adsr.Ddur),'{}'.format(adsr.Sval),'{}'.format(adsr.Rdur),'{}'.format(adsr.enabled),'{}'.format(incrementValue),'Update','Back']
    i = 0
    for string in ADSRSelectList:
        ADSRSelectString = smallerFont.render(string, True, blue)
        gameDisplay.blit(ADSRSelectString, (315, 10 + i))
        i += 40
    ADSRValueList = ['{}'.format(adsr.Adur), '{}'.format(adsr.ADval), '{}'.format(adsr.Ddur), '{}'.format(
        adsr.Sval), '{}'.format(adsr.Rdur), '{}'.format(adsr.enabled), '{}'.format(incrementValue), 'Update', 'Back']
    i = 0
    for value in ADSRValueList:
        ADSRSelectString = smallerFont.render(value, True, red)
        gameDisplay.blit(ADSRSelectString, (235, 10 + i))
        i += 40
    if RightButton:
        if currentADSR == 0:
            adsr.Adur = round(adsr.Adur + incrementValue, 3)
        elif currentADSR == 1:
            adsr.ADval = round(adsr.ADval + incrementValue, 3)
        elif currentADSR == 2:
            adsr.Ddur = round(adsr.Ddur + incrementValue, 3)
        elif currentADSR == 3:
            adsr.Sval = round(adsr.Sval + incrementValue, 3)
        elif currentADSR == 4:
            adsr.Rdur = round(adsr.Rdur + incrementValue, 3)
        elif currentADSR == 5:
            adsr.enabled = not adsr.enabled
        elif currentADSR == 6:
            if incrementValue >= 1:
                pass
            else:
                incrementValue = round(incrementValue * 10, 3)
        else:
            pass
        pygame.time.delay(300)  # prevents skipping selections

    if LeftButton:
        if currentADSR == 0:
            adsr.Adur = round(adsr.Adur - incrementValue, 3)
        elif currentADSR == 1:
            adsr.ADval = round(adsr.ADval - incrementValue, 3)
        elif currentADSR == 2:
            adsr.Ddur = round(adsr.Ddur - incrementValue, 3)
        elif currentADSR == 3:
            adsr.Sval = round(adsr.Sval - incrementValue, 3)
        elif currentADSR == 4:
            adsr.Rdur = round(adsr.Rdur - incrementValue, 3)
        elif currentADSR == 5:
            adsr.enabled = not adsr.enabled
        elif currentADSR == 6:
            if incrementValue <= 0.001:
                pass
            else:
                incrementValue = round(incrementValue / 10, 3)
        else:
            pass
        pygame.time.delay(300)  # prevents skipping selections

    if JoystickButton:
        if currentADSR == 5:
            adsr.enabled = not adsr.enabled
        elif currentADSR == 7:
            updateADSR()
        elif currentADSR == 8:
            updateADSR()
            state = 1
        else:
            pass
        pygame.time.delay(300)  # prevents skipping selections

    if JoystickVer == 1000:
        if currentADSR == len(ADSRValueList) - 1:
            currentADSR = 0
        else:
            currentADSR += 1
        pygame.time.delay(300)  # prevents skipping selections
    elif JoystickVer == 0:
        if currentADSR == 0:
            currentADSR = len(ADSRValueList) - 1
        else:
            currentADSR -= 1
        pygame.time.delay(300)  # prevents skipping selections

    # gameDisplay.blit(ADSRValueText,(220,10))

    return state, adsr, currentADSR, incrementValue


class SynthUI():

    def __init__(self):
        self.synth = se.Synth()
        self.vol = Volume
        self.name = defaultFont.render("+ Synth", True, blue)
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
        pass

    def setVol(self, Volume):
        self.synth.vol = Volume

    def playKeys(self, Piano, octavenum):

        for i in range(len(Piano)):
            state = (Piano[i], self.lastPiano[i])
            if state == (1, 0):
                self.synth.play(se.midi(i + octavenum))
            elif state == (0, 1):
                self.synth.release(se.midi(i + octavenum))
        self.lastPiano = Piano

    def drawPiano(self, gameDisplay, Piano, pKey, xThePiano, yThePiano):
        i = 0
        while i < len(Piano):
            if Piano[i] == 1:
                gameDisplay.blit(pKey[i], (xThePiano, yThePiano))
            i += 1

    def drawUI(self, gameDisplay):
        plotPosx = 560
        plotPosy = 7
        gameDisplay.blit(self.synthPlot, (0 + plotPosx, 0 + plotPosy))
        gameDisplay.blit(self.lfoPlot,  (0 + plotPosx, 190 + plotPosy))
        gameDisplay.blit(self.filterPlot, (190 + plotPosx, 0 + plotPosy))
        gameDisplay.blit(self.adsrPlot, (190 + plotPosx, 190 + plotPosy))

    def updateSources(self):
        self.synthPlot = self.synth.draw(440, 180, 180, 50)

    def updateFilter(self):
        self.filterPlot = self.synth.ffilter.draw(180, 180, 50)

    def updateLFO(self):
        self.lfoPlot = self.synth.lfo.draw(180, 180, 50)

    def updateADSR(self):
        self.adsrPlot = self.synth.adsr.draw(180, 180, 50)

    def updatePlots(self):
        self.updateSources()
        self.updateFilter()
        self.updateLFO()
        self.updateADSR()

def run():
    global inputs
    # import your script B
    pygame.init()

    display_width = 947
    display_height = 609

    gameDisplay = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('Music Board')
    clock = pygame.time.Clock()
    BoxBackground = pygame.image.load('images/BoxBackground.png')
    Button1 = pygame.image.load('images/Button1Small.png')
    Button1Pressed = pygame.image.load('images/Button1PressedSmall.png')
    Knob1 = pygame.image.load('images/Knob1.png')
    SynthList = pygame.image.load('images/SynthList.png')
    quit = False

    # Defining GUI positions in window
    xKnob1 = 500
    yKnob1 = 250
    xButton1 = 600
    yButton1 = 420
    xButton2 = 600
    yButton2 = 500
    xSynthList = 1
    ySynthList = 1
    xThePiano = 680
    yThePiano = 400
    xScrollBar = 215
    yScrollBar = 1

    # Loading GUI images
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
    thePiano = pygame.image.load('images/piano.png')
    octaveTitle = pygame.image.load('images/octaveTitle.png')
    ScrollBar = pygame.image.load('images/ScrollBar.png')
    Scroller = pygame.image.load('images/Scroller.png')
    SelectSynthBox = pygame.image.load('images/SelectSynthBox.png')
    SelectGraphBox = pygame.image.load('images/SelectGraphBox.png')
    SelectADSRBox = pygame.image.load('images/SelectADSRBox.png')

    currentSynth = 1

    octavenum = 72
    synthUIs = [SynthUI()]
    fullSynthList = False
    if fullSynthList == True:
        while len(synthUIs) < 10:
            synthUIs.append(SynthUI())
            numSynths = len(synthUIs)
            synthUIs[currentSynth - 1].name = defaultFont.render(
                "Synth {}".format(currentSynth), True, blue)
            currentSynth += 1
    else:
        currentSynth = 1
        numSynths = 1

    state = 1
    currentGraph = [0, 0]
    currentADSR = 0
    currentLFO = 0
    currentFilter = 0
    currentSource = 0
    incrementValue = 0.1

    j = 0
    ADSRSelectList = ["Attack Duration","Attack Value","Decay Duration","Sustain Value","Release Duration","Enabled","Increment Value"]
    LFOSelectList = ["Waveform","Frequency","Enabled","Mix","Increment Value"]
    FilterSelectList = ["Mode","Cutoff","Width","Mix","Enabled","# Repeats","Increment Value"]
    FilterModeList = ['low','high','band']
    CurrentFilterMode = 0
    WaveFormList = ["Sine","Saw","Square","Triangle","Noise"]
    currentWaveForm = 0
    SourcesSelectList = ["Waveform","Scale","Shift","# of Sources","Current Source","Increment Value"]
    currentSource = 0
    Waves = [se.Wave.SINE,se.Wave.SAW,se.Wave.SQUARE,se.Wave.TRIANGLE,se.Wave.NOISE]
    editingThisSource = 0
    while not quit:

        # Reading piano input
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
        Volume = (inputs["A0"])
        JoystickHor = (inputs["A14"])
        JoystickVer = (inputs["A15"])
        JoystickButton = (inputs["25"])
        LeftButton = (inputs["23"])
        RightButton = (inputs["22"])
        synthUIs[currentSynth - 1].setVol(Volume / 1000)

        # Displaying UI
        gameDisplay.blit(BoxBackground, (1, 1))
        gameDisplay.blit(thePiano, (xThePiano, yThePiano))
        gameDisplay.blit(ScrollBar, (xScrollBar, yScrollBar))

        # Displaying selection box
        gameDisplay.blit(SelectSynthBox, (5, -55 - j + (currentSynth * 60)))

        # Displaying all available synths
        i = 10
        if numSynths >= 11:
            if currentSynth >= 10:
                j = (currentSynth - 10) * 60
                yNewScrollBar = round(
                    display_height * (1 - (10 / numSynths) - (1 - (currentSynth / numSynths))))
            else:
                j = 0
                yNewScrollBar = yScrollBar
            NewScroller = pygame.image.load('images/Scroller.png')
            xNewScrollerSize = 20
            yNewScrollerSize = round(display_height * (10 / numSynths))

            gameDisplay.blit(pygame.transform.scale(
                NewScroller, (xNewScrollerSize, yNewScrollerSize)), (xScrollBar, yNewScrollBar))
        else:
            gameDisplay.blit(Scroller, (xScrollBar, yScrollBar))

        for synth in synthUIs:
            # print(synth.name)
            gameDisplay.blit(synth.name, (10, i - j))
            i += 60

        if state == 1:
            if LeftButton:
                gameDisplay.blit(Button1Pressed, (xButton1, yButton1))
                octavenum = octavenum - 12
                pygame.time.delay(300)  # prevents skipping octaves
            else:
                gameDisplay.blit(Button1, (xButton1, yButton1))

            if RightButton:
                gameDisplay.blit(Button1Pressed, (xButton2, yButton2))
                octavenum = octavenum + 12
                pygame.time.delay(300)  # prevents skipping octaves
            else:
                gameDisplay.blit(Button1, (xButton2, yButton2))

        # Displaying graph selection box if applicable
        if state > 1:
            plotPosx = 560
            plotPosy = 7
            gameDisplay.blit(SelectGraphBox, (plotPosx - 5 + (currentGraph[0] * 190), plotPosy - 5 + (currentGraph[1] * 190)))

        if state == 3:
            gameDisplay.blit(SelectADSRBox,(230,5+(40*currentSource)))

        #Displaying LFO selection box if applicable
        if state == 4:
            gameDisplay.blit(SelectADSRBox,(230,5+(40*currentLFO)))

        #Displaying Filter selection box if applicable
        if state == 5:
            gameDisplay.blit(SelectADSRBox,(230,5+(40*currentFilter)))

        #Displaying ADSR selection box if applicable
        if state == 6:
            gameDisplay.blit(SelectADSRBox, (230, 5 + (40 * currentADSR)))

        synthUIs[currentSynth - 1].drawUI(gameDisplay)
        synthUIs[currentSynth - 1].playKeys(Piano, octavenum)
        synthUIs[currentSynth - 1].drawPiano(gameDisplay, Piano, pKey, xThePiano, yThePiano)
        if state == 1:
            j, state, currentSynth, numSynths = selectMode(
                j, JoystickButton, JoystickVer, JoystickHor, currentSynth, numSynths, synthUIs, state)
        elif state == 2:
            state, currentGraph = selectGraphMode(
                JoystickButton, JoystickVer, JoystickHor, currentGraph, state)
        elif state == 3:
            state, synthUIs[currentSynth-1].synth.sources, currentSource, incrementValue, currentWaveForm, editingThisSource = editSourcesMode(editingThisSource,
                Waves,synthUIs[currentSynth-1].updateSources,incrementValue,currentWaveForm,SourcesSelectList,WaveFormList,state,synthUIs[currentSynth-1].synth.sources,
                currentSource,JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay)
        elif state == 4:
            state, synthUIs[currentSynth-1].synth.lfo, currentLFO, incrementValue, currentWaveForm = editLFOMode(
                Waves,synthUIs[currentSynth-1].updateLFO,incrementValue,currentWaveForm,LFOSelectList,WaveFormList,
                state,synthUIs[currentSynth-1].synth.lfo,currentLFO,JoystickVer,JoystickHor,JoystickButton,
                LeftButton,RightButton,gameDisplay)
        elif state == 5:
            state, synthUIs[currentSynth-1].synth.ffilter, currentFilter, incrementValue, CurrentFilterMode = editFilterMode(
                incrementValue,FilterModeList,CurrentFilterMode,FilterSelectList,synthUIs[currentSynth-1].updateFilter,
                state,synthUIs[currentSynth-1].synth.ffilter,currentFilter,JoystickVer,JoystickHor,JoystickButton,
                LeftButton,RightButton,gameDisplay)
        elif state == 6:
            state, synthUIs[currentSynth-1].synth.adsr, currentADSR, incrementValue = editADSRMode(
                ADSRSelectList,incrementValue,synthUIs[currentSynth-1].updateADSR,synthUIs[currentSynth-1].synth.adsr,
                JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay,state,currentADSR)

        pygame.display.update()
        clock.tick(30)

    pygame.quit
    quit()


Thread(target=serialReader.run, args=("/dev/ttyACM0", inputs, True)).start()
Thread(target=run).start()
