import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
import pygame
from enum import IntEnum, Enum
from threading import Thread

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


def playArray(array, repeat=False):
    pySound = Array2PySound(array)
    k = -1 if repeat else 0
    pyChannel = pySound.play(k)
    return pySound, pyChannel


def Array2PySound(array):
    scaledArray = 0.5 * array * 32768
    scaledArray = scaledArray.astype(np.int16)
    pySound = pygame.mixer.Sound(scaledArray)
    return pySound


class synth:
    def __init__(self, oscillators=2):

        self.sources = []
        for i in range(oscillators):
            self.sources.append(oscillator())
        self.adsr = Envelope()

    def getToneData(self, freq, dur):
        tone = 0
        for osc in self.sources:
            tone += osc.getToneData(freq, dur)
        tone /= np.amax(tone)
        return tone

    def draw(self, freq):
        plt.hold(True)

        for source in self.sources:
            source.plot(freq)

        y = self.getToneData(freq, 1/freq)
        t = np.linspace(0, 1/freq, y.size)
        plt.plot(t, y)

        plt.hold(False)
        plt.ylim(-1, 1)
        plt.xlim(0, 1/freq)
        plt.show()

    def play(self, freq):
        # get tone data of the synth at this frequency for 5 waves
        tone = self.getToneData(freq, 10/freq)
        if self.adsr.enabled:
            pass
        else:
            sustainTone, pyChannel = playArray(tone, True)
            self.sustains[str(freq)] = sustainTone

    def release(self, freq):
        # get release tone
        # play release tone
        # stop sustain tone:
        self.sustains[str(freq)].stop()


class oscillator:
    def __init__(self, form=Wave.SINE):
        self.form = form
        self.scale = 1

    # TODO: Implement form
    def getToneData(self, freq, dur):
        t = np.linspace(0, dur, dur * sample_rate, False)
        theta = 2 * np.pi * freq * t
        waveforms = {
            Wave.SINE: np.sin(theta),
            Wave.SAW: signal.sawtooth(theta, 0),
            Wave.SQUARE: signal.square(theta)
        }
        return self.scale * waveforms.get(self.form)

    def play(self, freq, dur):
        tone = self.getToneData(freq, dur)
        playArray(tone)

    def plot(self, freq):
        y = self.getToneData(freq, 1/freq)
        t = np.linspace(0, 1/freq, y.size)
        plt.plot(t, y)


class Envelope:
    def __init__(self):
        self.Adur = 0.5
        self.Dval = 0.5
        self.Ddur = 0.2
        self.Sval = 1
        self.Rdur = 0.3
        self.enabled = False
        self.sustains = {}

    def play(self, osc, freq):
        ADTone = self.getAttackDelay(osc, freq)
        pySound, pyChannel = playArray(ADTone)
        Thread(target=self.playSustain, args=(osc, freq, pyChannel)).run()

    def playSustain(self, osc, freq, channel=None):
        STone = self.getSustain(osc, freq)
        #SSound = Array2PySound(STone)
        #channel.queue(SSound)
        #while channel.get_busy():
        #    pass
        pySound, pyChannel = playArray(STone, True)
        self.sustains[str(freq)] = pySound

    def release(self, osc, freq):
        RTone = self.getRelease(osc, freq)
        playArray(RTone)
        self.sustains[str(freq)].stop()

    def getAttackDelay(self, osc, freq):
        oscData = osc.getToneData(freq, self.Adur + self.Ddur)
        AScaleArray = np.linspace(
                0, self.Dval, self.Adur*sample_rate)
        DScaleArray = np.linspace(
                self.Dval, self.Sval, self.Ddur*sample_rate)[:-1]
        ADScaleArray = np.concatenate((AScaleArray, DScaleArray))

        return np.multiply(oscData, ADScaleArray)

    def getSustain(self, osc, freq):
        oscData = osc.getToneData(freq, 1)
        return self.Sval * oscData

    def getRelease(self, osc, freq):
        oscData = osc.getToneData(freq, self.Rdur)
        RScaleArray = np.linspace(
                self.Sval, 0, self.Rdur*sample_rate)
        return np.multiply(oscData, RScaleArray)


if __name__ == "__main__":
    mySynth = synth()
    mySynth.sources[0].form = Wave.SQUARE
    mySynth.sources[0].scale = 0.25
    mySynth.draw(Note.A)

    myEnv = Envelope()
    while True:
        myEnv.play(mySynth, Note.B)
        time.sleep(4)
        myEnv.release(mySynth, Note.B)
        time.sleep(2)

    for i in range(3):

        mySynth.sources[0].play(Note.A, 2)
        time.sleep(3)
        mySynth.sources[1].play(Note.A, 2)
        time.sleep(3)
        print("Play Now!")
        mySynth.play(Note.A)
        time.sleep(3)
        print("Release Now!")
        mySynth.release(Note.A)
        time.sleep(3)
