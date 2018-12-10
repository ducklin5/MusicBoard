LFOSelectList = ["Waveform","Frequency","Enabled","Mix?","Increment Value","Update","Back"]
WaveFormList = ["SINE","SAW","SQUARE","TRIANGLE","NOISE"]
    i = 0
    for string in LFOSelectList:
        LFOSelectString = smallerFont.render(string, True, blue)
        gameDisplay.blit(LFOSelectString,(315,10+i))
        i+=40
    LFOValueList = ['{}'.format(lfo.form),'{}'.format(lfo.freq),'{}'.format(lfo.enabled),'{}'.format(lfo.sync),'{}'.format(lfo.mix),'{}'.format(lfo.active),'{}'.format(incrementValue),'Update','Back']
    i = 0
    for value in LFOValueList:
        LFOSelectString = smallerFont.render(value, True, red)
        gameDisplay.blit(LFOSelectString,(235,10+i))
        i+=40
    if RightButton:
        if currentLFO == 0:
            lfo.form = 
        elif currentLFO == 1:
            lfo.freq = round(lfo.freq+incrementValue,3)
        elif currentLFO == 2:
            lfo.enabled = not lfo.enabled
        elif currentLFO == 3:
            lfo.sync = not lfo.enabled
        elif currentLFO == 4:
            lfo.mix = round(lfo.mix+incrementValue,3)
        elif currentLFO == 5:
            lfo.active = round(lfo.active+incrementValue,3)
        elif currentLFO == 6:
            if incrementValue >= 100:
                pass
            else:
                incrementValue = round(incrementValue*10,3)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if LeftButton:
        if currentLFO == 0:
            lfo.form = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        elif currentLFO == 1:
            lfo.freq = round(lfo.freq-incrementValue,3)
        elif currentLFO == 2:
            lfo.enabled = not lfo.enabled
        elif currentLFO == 3:
            lfo.sync = not lfo.enabled
        elif currentLFO == 4:
            lfo.mix = round(lfo.mix-incrementValue,3)
        elif currentLFO == 5:
            lfo.active = round(lfo.active-incrementValue,3)
        elif currentLFO == 6:
            if incrementValue <= 0.001:
                pass
            else:
                incrementValue = round(incrementValue/10,3)
        else:
            pass
        pygame.time.delay(300) #prevents skipping selections

    if JoystickButton:
        if currentLFO == 7:
            updateLFO()
        elif currentLFO == 8:
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

    return state, lfo, currentLFO, incrementValue