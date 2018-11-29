import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
import pygame
from enum import Enum
from threading import Thread

sample_rate = 44100
size = -16
channels = 2
buffersize = 4096

pygame.mixer.pre_init(int(sample_rate/2), size, channels, buffersize)
pygame.mixer.init()
pygame.mixer.set_num_channels(100)


# https://en.wikipedia.org/wiki/MIDI_tuning_standard
def midi(midiKey):
    # midi key 69 --> A4
    # midi key 70 --> A#4
    # midi key 71 --> B4
    freq = (440) * (2**((midiKey-69)/12))
    return freq


# https://docs.python.org/3/library/enum.html
class Wave(Enum):
    SAW = 0
    SINE = 1
    SQUARE = 2
    TRIANGLE = 3


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
            Wave.SQUARE: signal.square(theta),
            Wave.TRIANGLE: signal.sawtooth(theta, 0.5)
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
        self.Adur = 0.05
        self.Dval = 0.5
        self.Ddur = 0.2
        self.Sval = 1
        self.Rdur = 0.3
        self.enabled = False
        self.sustains = {}

    def start(self, sound):
        # http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
        thread = Thread(target=self.__start__, args=(sound,))
        thread.daemon = True
        thread.start()

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

        sound.set_volume(self.Sval)

    def release(self, sound):
        thread = Thread(target=self.__release__, args=(sound,))
        thread.daemon = True
        thread.start()

    def __release__(self, sound):
        start = time.time()
        elapsed = 0
        while elapsed < self.Rdur:
            time.sleep(1/sample_rate)
            sound.set_volume(self.Sval-self.Sval*elapsed/self.Rdur)
            elapsed = time.time() - start
        sound.stop()


if __name__ == "__main__":
    # create a synth
    mySynth = synth()

    # with 3 oscillators
    mySynth.sources[0].form = Wave.SQUARE
    mySynth.sources[1].form = Wave.TRIANGLE
    mySynth.sources.append(oscillator())
    mySynth.sources[2].form = Wave.SINE

    # set the oscillator volumes
    mySynth.sources[0].scale = 0.5
    mySynth.sources[1].scale = 0.75
    mySynth.sources[2].scale = 0.75

    # draw this output pf the synth (and its oscillators)
    # for freq = midi(69)
    mySynth.draw(midi(69))

    #
    mySynth.adsr.Adur = 0.3
    mySynth.adsr.Ddur = 0.1
    mySynth.adsr.Dval = 1
    mySynth.adsr.Sval = 0.1
    mySynth.adsr.Rdur = 0.2

    def myK(k):
        mySynth.play(midi(k))
        time.sleep(0.4)
        mySynth.release(midi(k))
        time.sleep(0.1)

    while True:
        myK(69)
        myK(71)
        myK(72)
        myK(74)
        myK(69)
        myK(71)
        myK(72)
        myK(77)
