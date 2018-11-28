import numpy as np
import matplotlib.pyplot as plt
import time
import pygame


sample_rate = 44100
size = -16
channels = 2
buffersize = 4096

pygame.mixer.pre_init(int(sample_rate/2), size, channels, buffersize)
pygame.mixer.init()
pygame.mixer.set_num_channels(100)

frequencies = {'A': 440, 'B': 493.88, 'C': 523.25, 'D': 440, 'E': 440, 'F': 440}


class synth:
    def __init__(self):
        self.osc = oscillator(0)
        self.adsr = ADSREnvelope()

    def play(self, freq):
        tone = self.osc.getToneData(freq, 0.25)
        scaledTone = 0.5 * tone * 32768
        scaledTone = scaledTone.astype(np.int16)
        pySound = pygame.mixer.Sound(scaledTone)
        pySound.play()


class oscillator:
    def __init__(self, form=0):
        self.form = form

    # TODO: Implement form
    def getToneData(self, freq, T):
        t = np.linspace(0, T, T * sample_rate, False)
        return np.sin(2 * np.pi * freq * t)

    def from2Osc(self, wave1, wave2):
        pass

    def play(self, freq):
        newTone = sound(freq, self.getToneData(freq), self)
        newTone.play()

    def draw(self):
        # plt.plot(t, self.getToneData(440), 'x')
        plt.show()


# A sample set
class sound:
    def __init__(self, data):
        self.data = data

    def play(self):
        return(self)


class ADSREnvelope:
    def __init__(self):
        self.Adur = 0.1
        self.Astart = 0
        self.Astop = 1
        self.Ddur = 0.1
        self.Dstop = 0.5
        self.Rdur = 0.1
        self.Rstop = 0.1
        self.enabled = True

    def getSounds(self, tone):
        pass


mySynth = synth()
for i in range(25):
    start = time.time
    mySynth.play(frequencies['A'])
    time.sleep(2)
    mySynth.play(frequencies['C'])
    time.sleep(2)
