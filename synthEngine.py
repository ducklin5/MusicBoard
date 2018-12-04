import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
import pygame
from enum import Enum
from threading import Thread
import random

sample_rate = 44100
size = -16
channels = 1
# https://stackoverflow.com/questions/18273722/pygame-sound-delay
buffersize = 512
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


def myK(mySynth,k):
        mySynth.play(midi(k))
        time.sleep(0.100)
        mySynth.release(midi(k))
        time.sleep(0.25)

def synthInit(mySynth):
    #mySynth.ffilter.draw()
    mySynth.ffilter.mix = 0
    #mySynth.draw(440)
    mySynth.ffilter.mix = 0
    #mySynth.draw(440)

    mySynth.adsr.Adur = 2
    mySynth.adsr.Ddur = 0.4
    mySynth.adsr.ADval = 1
    mySynth.adsr.Sval = 0.5
    mySynth.adsr.Rdur = 2
    mySynth.adsr.enabled = False

    mySynth.lfo.freq = 0.75
    mySynth.lfo.mix = 0.75
    mySynth.lfo.osc.form = Wave.SAW
    mySynth.lfo.enabled = False


# https://docs.python.org/3/library/enum.html
class Wave(Enum):
    SAW = 0
    SINE = 1
    SQUARE = 2
    TRIANGLE = 3
    NOISE = 4


def playArray(array, repeat=False):
    scaledArray = 0.5 * array * 32768
    scaledArray = scaledArray.astype(np.int16)
    pySound = pygame.sndarray.make_sound(scaledArray)

   # pySound = Array2PySound(array)
    k = -1 if repeat else 0
    pyChannel = pySound.play(k)
    return pySound, pyChannel


def Array2PySound(array):
    scaledArray = 0.5 * array * 32768
    scaledArray = scaledArray.astype(np.int16)
    pySound = pygame.mixer.Sound(scaledArray)
    return pySound


def noise(input):
    if input is (int or float):
        return 2 * random.random() - 1
    elif input is (iter):
        out = []
        random.seed()
        for i in input:
            out.append(2 * random.random() - 1)
        return np.array(out)


class Synth:
    def __init__(self, oscillators=2):

        self.sources = []
        for i in range(oscillators):
            self.sources.append(Oscillator())
        self.adsr = Envelope()
        self.ffilter = Filter()
        self.lfo = LFO()
        self.sustains = {}
        self.vol = 1

    def getToneData(self, freq):
        tone = 0
        period = 1/freq
        for osc in self.sources:
            tone += osc.getToneData(freq, period*10)
        tone /= np.amax(abs(tone))
        tone = self.ffilter.run(tone)
        return self.vol * tone

    def draw(self, freq):
        y = self.getToneData(freq)
        dur = y.size/sample_rate
        t = np.linspace(0, y.size/sample_rate, y.size)

        for source in self.sources:
            source.plot(freq, dur)

        plt.plot(t, y)

        plt.ylim(-1, 1)
        plt.show()

    def play(self, freq):
        if str(freq) not in self.sustains:
            self.sustains[str(freq)] = None

        if self.sustains[str(freq)] is None:
            # get tone data of the Synth at this frequency for 5 waves
            tone = self.getToneData(freq)

            pySound, pyChannel = playArray(tone, True)
            sController = SoundController(pySound)
            self.adsr.start(sController, "adsr")
            self.lfo.start(sController, "lfo")
            self.sustains[str(freq)] = sController
            return sController
        else:
            print("Frequency: " + str(freq) + " has not been released!")

    def release(self, freq):
        sController = self.sustains[str(freq)]
        self.adsr.release(sController, "adsr") # the adsr will kill the controller when its done with delay
        self.sustains[str(freq)] = None


class Oscillator:
    def __init__(self, form=Wave.SINE, scale=1, fine=0, shift=0):
        self.form = form
        self.scale = scale
        self.shift = 0

    def getToneData(self, freq, dur, singular=False):
        if singular:
            t = dur
        else:
            t = np.linspace(0, dur, dur * sample_rate, False)
        theta = 2 * float(np.pi) * freq * t + self.shift
        waveforms = {
                Wave.SINE: np.sin(theta),
                Wave.SAW: signal.sawtooth(theta, 0),
                Wave.SQUARE: signal.square(theta),
                Wave.TRIANGLE: signal.sawtooth(theta, 0.5),
                Wave.NOISE: noise(theta)
                }
        return self.scale * waveforms.get(self.form)

    def play(self, freq, dur):
        tone = self.getToneData(freq, dur)
        pySound, pyChannel = playArray(tone)
        return pySound

    def plot(self, freq, dur):
        y = self.getToneData(freq, dur)
        t = np.linspace(0, dur, y.size)
        plt.plot(t, y)

class LFO:
    def __init__(self, form=Wave.SINE, freq=10):
        self.osc = Oscillator()
        self.osc.form = form
        self.freq = freq
        self.enabled = True
        self.active = []
        self.time = time.time()
        self.sync = False
        self.mix = 1

    # def run(self, inputData, freq):
    #     # assuming that inputData is a whole number of waves
    #     inputPeriod = 1/freq
    #     samplesPerWave = round(inputPeriod*sample_rate)
    #     singleWave = inputData[:samplesPerWave]
    #     lfoPeriod = 1/self.freq
    #     outPeriod = lcm(inputPeriod, lfoPeriod)
    #     repeats = outPeriod/inputPeriod
    #
    #     output = np.zeros(0)
    #     for i in range(round(repeats)):
    #         output = np.append(output, singleWave)
    #
    #     lfoData = self.osc.getToneData(self.freq, float(output.size)/sample_rate )
    #
    #     if self.mode == 'velocity':
    #         output = np.multiply(lfoData, output)
    #
    #     return output

    def start(self, sController, id):
        if self.enabled:
            thread = Thread(target=self.__start__, args=(sController,id))
            thread.daemon = True
            thread.start()

    def __start__(self, sController, id):
        if self.enabled:
            self.active.append(sController)
            if self.sync:
                start = time.time()
            else:
                start = self.time
            while sController in self.active and sController.alive:
                # work at half the sample rate
                time.sleep(1/sample_rate)
                elapsed = time.time() - start
                vol = self.osc.getToneData(self.freq, elapsed, singular=True)
                vol = (vol + 1)/2
                sController.set_volume(
                   vol * (self.mix) + 1 *(1-self.mix), id
                )
            self.active.remove(sController)


# sound Wrapper to enable multiple volume knobs on a sound file
class SoundController:
    def __init__(self, sound):
        self.knobs = {}
        self.sound = sound
        self.alive = True

    def set_volume(self, vol, knobkey):
        self.knobs[knobkey] = vol
        combined = 1
        for key, value in self.knobs.items():
            combined *= value

        self.sound.set_volume(0.9*combined)
    
    def stop(self):
        self.sound.stop()


class Envelope:
    def __init__(self):
        self.Adur = 0.1
        self.ADval = 1
        self.Ddur = 0.1
        self.Sval = 0.5
        self.Rdur = 0.3
        self.enabled = True

    def start(self, sController, id):
        if self.enabled:
            # http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
            thread = Thread(target=self.__start__, args=(sController,id))
            thread.daemon = True
            thread.start()

    def __start__(self, sController, id):
        sController.set_volume(0, id)
        start = time.time()
        elapsed = 0
        while elapsed < self.Adur:
            time.sleep(1/sample_rate)
            sController.set_volume(
                self.ADval * elapsed/self.Adur, id
            )
            elapsed = time.time() - start

        start = time.time()
        elapsed = 0
        while elapsed < self.Ddur:
            time.sleep(1/sample_rate)
            sController.set_volume(
                    self.ADval + (self.Sval-self.ADval)*elapsed/self.Ddur, id
            )

            elapsed = time.time() - start

        sController.set_volume(self.Sval, id)

    def release(self, sController, id):
        thread = Thread(target=self.__release__, args=(sController, id))
        thread.daemon = True
        thread.start()

    def __release__(self, sController, id):
        if self.enabled:
            start = time.time()
            elapsed = 0
            while elapsed < self.Rdur:
                time.sleep(1/sample_rate)
                sController.set_volume(self.Sval-self.Sval*elapsed/self.Rdur, id)
                elapsed = time.time() - start
        sController.stop()
        sController.alive = False


class Filter:
    def __init__(self, mode='low', cuttoff=200, width=1000, repeats=4, mix=1):
        self.mode = mode
        self.cuttoff = cuttoff
        self.width = width
        self.mix = mix
        self.enabled = True
        self.repeats = repeats

    def draw(self):
        b, a = self.__createButter__()
        angularFreq, response = signal.freqz(b, a)
        realFreq = sample_rate * angularFreq/ (2*np.pi)

        plt.semilogx(realFreq, abs(response))
        ticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k"]
        plt.xticks(ticks, labels)

        plt.xlim([20, 20000])
        plt.show()

    def run(self,  inputSignal):
        if self.enabled:
            b, a = self.__createButter__()
            outputSignal = signal.filtfilt(b, a, inputSignal)
            outputSignal = self.mix * outputSignal + (1-self.mix) * inputSignal
            return outputSignal
        else:
            return inputSignal


    def __createButter__(self):
        # https://dsp.stackexchange.com/questions/49460/apply-low-pass-butterworth-filter-in-python
        if self.mode == ('low' or 'high'):
            normalizedCuttoff = self.cuttoff / (sample_rate / 2)  # Normalize the frequency
            butter = signal.butter(1 + self.repeats, normalizedCuttoff, btype=self.mode)
        elif self.mode == 'band':
            low = self.cuttoff / (sample_rate / 2)
            high = (self.cuttoff + self.width) / (sample_rate / 2)
            butter = signal.butter(1 + self.repeats, [low, high], btype=self.mode)

        return butter

if __name__ == "__main__":

    mySynth = Synth(2)
    mySynth.sources[0].form = Wave.SINE
    mySynth.sources[1].form = Wave.SQUARE
    #mySynth.sources[2].form = Wave.SINE

    mySynth.sources[0].scale = 0.5
    #mySynth.sources[1].scale = 0.5
    #mySynth.sources[2].scale = 1

    #mySynth.sources[1].shift = 4 * np.pi/3

    #mySynth.ffilter.draw()
    mySynth.ffilter.mix = 0
    #mySynth.draw(440)
    mySynth.ffilter.mix = 0
    #mySynth.draw(440)

    mySynth.adsr.Adur = 2
    mySynth.adsr.Ddur = 0.4
    mySynth.adsr.ADval = 1
    mySynth.adsr.Sval = 0.5
    mySynth.adsr.Rdur = 2
    mySynth.adsr.enabled = False

    mySynth.lfo.freq = 0.75
    mySynth.lfo.mix = 0.75
    mySynth.lfo.osc.form = Wave.SAW
    mySynth.lfo.enabled = False
    

    while True:
        myK(mySynth,69)
        # myK(mySynth,73)
        # myK(mySynth,69)
        # myK(mySynth,73)
        # myK(mySynth,69)
        # myK(mySynth,73)
        # myK(mySynth,69)
        # myK(mySynth,73)