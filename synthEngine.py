import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
import pygame
from enum import IntEnum, Enum

sample_rate = 44100
size = -16
channels = 2
buffersize = 4096

pygame.mixer.pre_init(int(sample_rate/2), size, channels, buffersize)
pygame.mixer.init()
pygame.mixer.set_num_channels(100)


# https://docs.python.org/3/library/enum.html
class Note(IntEnum):
    A = 440
    B = 493.88
    C = 523.25
    D = 440
    E = 440
    F = 440


class Wave(Enum):
    SAW = 0
    SINE = 1
    SQUARE = 2


def playArray(array):
    scaledArray = 0.5 * array * 32768
    scaledArray = scaledArray.astype(np.int16)
    pySound = pygame.mixer.Sound(scaledArray)
    pySound.play()


class synth:
    def __init__(self):
        self.sources = [oscillator(Wave.SINE), oscillator(Wave.SAW)]
        self.adsr = ADSREnvelope()
        self.adsr.enabled = False

    def combine(self, freq, dur):
        tone = 0
        for osc in self.sources:
            tone += osc.getToneData(freq, dur)
        tone /= np.amax(tone)
        return tone

    def draw(self, freq):
        plt.hold(True)

        for source in self.sources:
            source.plot(freq)

        y = self.combine(freq, 1/freq)
        t = np.linspace(0, 1/freq, y.size)
        plt.plot(t, y)

        plt.hold(False)
        plt.ylim(-1, 1)
        plt.xlim(0,1/freq)
        plt.show()

    def play(self, freq, dur):
        tone = self.combine(freq, dur)
        if self.adsr.enabled:
            pass
        else:
            playArray(tone)


class oscillator:
    def __init__(self, form=Wave.SINE):
        self.form = form

    # TODO: Implement form
    def getToneData(self, freq, dur):
        t = np.linspace(0, dur, dur * sample_rate, False)
        if self.form == Wave.SINE:
            return np.sin(2 * np.pi * freq * t)
        elif self.form == Wave.SAW:
            return signal.sawtooth(2 * np.pi * freq * t, 0)
        elif self.form == Wave.SQUARE:
            return signal.square(2 * np.pi * freq * t)

    def play(self, freq, dur):
        tone = self.getToneData(freq, dur)
        playArray(tone)

    def plot(self, freq):
        y = self.getToneData(freq, 1/freq)
        t = np.linspace(0, 1/freq, y.size)
        plt.plot(t, y)


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


if __name__ == "__main__":
    mySynth = synth()
    mySynth.draw(Note.A)
    for i in range(3):
        mySynth.sources[0].play(Note.A, 2)
        time.sleep(3)
        mySynth.sources[1].play(Note.A, 2)
        time.sleep(3)
        mySynth.play(Note.A, 2)
        time.sleep(3)
