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
        self.sustains = {}
        self.useEnvelope = True

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
        pySound, pyChannel = playArray(tone, True)
        if self.useEnvelope:
            self.adsr.start(pySound)
        self.sustains[str(freq)] = pySound
        return pySound

    def release(self, freq):
        if self.useEnvelope:
            self.adsr.release(self.sustains[str(freq)])
        else:
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
        pySound, pyChannel = playArray(tone)
        return pySound

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

    def start(self, sound):
        Thread(target=self.__start__, args=(sound,)).run()

    def __start__(self, sound):
        sound.set_volume(0)
        start = time.time()
        elapsed = 0
        while elapsed < self.Adur:
            time.sleep(1/sample_rate)
            sound.set_volume(self.Dval * elapsed/self.Adur)
            elapsed = time.time() - start

        start = time.time()
        elapsed = 0
        while elapsed < self.Ddur:
            time.sleep(1/sample_rate)
            sound.set_volume(
                    self.Dval + (self.Sval-self.Dval)*elapsed/self.Ddur)
            elapsed = time.time() - start

    def release(self, sound):
        Thread(target=self.__release__, args=(sound,)).run()

    def __release__(self, sound):
        start = time.time()
        elapsed = 0
        while elapsed < self.Rdur:
            time.sleep(1/sample_rate)
            sound.set_volume(self.Sval-self.Sval*elapsed/self.Adur)
            elapsed = time.time() - start
        sound.stop()


if __name__ == "__main__":
    mySynth = synth()
    mySynth.sources[0].form = Wave.SQUARE
    mySynth.sources[0].scale = 0.25
    mySynth.draw(Note.A)

    myEnv = Envelope()
    while True:
        mySynth.play(Note.B)
        time.sleep(3)
        mySynth.release(Note.B)
        time.sleep(3)

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
