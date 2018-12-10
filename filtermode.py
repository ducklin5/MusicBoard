def editFilterMode(FilterModeList,CurrentFilterMode,FilterSelectList,updateFilter,state,ffilter,currentFilter,JoystickVer,JoystickHor,JoystickButton,LeftButton,RightButton,gameDisplay):    
    
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