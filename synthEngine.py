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


def playArray(array, repeat=False):
    scaledArray = 0.5 * array * 32768
    scaledArray = scaledArray.astype(np.int16)
    pySound = pygame.mixer.Sound(scaledArray)
    k = -1 if repeat else 0
    pySound.play(k)
    return pySound


class synth:
    def __init__(self, oscillators=2):

        self.sources = []
        for i in range(oscillators):
            self.sources.append(oscillator())
        self.adsr = ADSREnvelope()
        self.sustains = {}

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
            sustainTone = playArray(tone, True)
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


class ADSREnvelope:
    def __init__(self):
        self.Adur = 0.1
        self.Dval = 1
        self.Ddur = 0.1
        self.Sval = 0.1
        self.Rdur = 0.1
        self.enabled = False

    def getSounds(self, tone, freq):
        repeats = 1
        samplePerWave = round(sample_rate/freq)
        samplesForRepeats = int(repeats*sample_rate/freq)

        multiWave = tone[:samplesForRepeats]
        singleWave = tone[:samplePerWave]

        y_orig = multiWave
        y_concatanated = singleWave
        for i in range(repeats-1):
            y_concatanated = np.concatenate((y_concatanated, singleWave))

        plt.hold(True)
        t = np.linspace(0, repeats/freq, y_orig.size)
        tc = np.linspace(0, repeats/freq, y_concatanated.size)
        plt.plot(t, y_orig, 'o')
        plt.plot(tc, y_concatanated, '*')

        plt.ylim(-1, 1)
        plt.xlim(0, repeats/freq)
        plt.show()

    def getAttackDelay(self, tone, freq):
        pass

    def getSustain(self, tone, freq):
        pass

    def getRelease(self, tone, freq):
        pass


if __name__ == "__main__":
    mySynth = synth()
    mySynth.sources[0].form = Wave.SQUARE
    mySynth.sources[0].scale = 0.25
    mySynth.draw(Note.A)
    q = mySynth.getToneData(Note.A, 16)

    myAdsrE = ADSREnvelope()
    myAdsrE.getSounds(q, Note.B)

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
