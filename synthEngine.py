# ---------------------------------------------------
#    Name: Azeez  Abass
#    ID: 1542780
#    Name: Matthew Braun
#    ID: 1497171
#    CMPUT 274 EA1, Fall  2018
#    Project: ZMat 2000 (SynthEngine)
# ---------------------------------------------------

###########
# Imports
###########
import numpy as np  # numpy for some math functions
from scipy import signal  # for signal generation and butterworth filter
import time  # for timing
import pygame  # for playing sounds/ buffer manager
from enum import Enum  # to enumarate wave types
from threading import Thread  # mixing sounds while playing
import random  # noise generator
import matplotlib  # plot graphs of waves, envelopes and filters
# The folling imports were needed to convert plots to images for pygame
# http://www.pygame.org/wiki/MatplotlibPygame
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt


# set the sample rate, bit rate, channels used. and initialize the mixer
sample_rate = 22050
size = -16
channels = 1  # Number of channels to use, ie. mono/stereo. 1 means mono

# https://stackoverflow.com/questions/18273722/pygame-sound-delay
buffersize = 256  # reduced the buffer size to reduce lag

pygame.mixer.pre_init(int(sample_rate), size, channels, buffersize)
pygame.mixer.init()
pygame.mixer.set_num_channels(100)  # Number of sounds that can play at once


###############################
# HELPER FUNCTIONS AND CLASSES
###############################
def plt2Img(width, height):
    """
    Converts Matplotlib plot to pygame image
    Inputs:
        width: output image width
        height: output image height
    Returns:
        image (pygame.Surface): the plot as a pygame image/Surface
    Refrences:
        http://www.pygame.org/wiki/MatplotlibPygame
    """
    fig = plt.gcf()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    plt.close(fig)
    imgString = renderer.tostring_rgb()
    image = pygame.image.fromstring(imgString, (width, height), "RGB")
    return image


def midi(midiKey):
    """
    Midi number to note frequency converter
    Inputs:
        midiKey: midi number
    Returns:
        freq (float): frequency
    Refrences:
        https://en.wikipedia.org/wiki/MIDI_tuning_standard
    """
    # midi key 69 --> A4
    # midi key 70 --> A#4
    # midi key 71 --> B4
    freq = (440) * (2**((midiKey - 69) / 12))
    return freq


def Array2PySound(array):
    """
    Converts a numpy array to a pygme Sound object
    Function assumes array values range from 0 to 1
    Inputs:
        array (np.array): array to be converted
    Returns:
        pySound (pygame.mixer.Sound): pygame sound object
    """
    # pygame mixer was initialized with a bit rate of 16
    # so Arrays must be scaled to 16 bits. Where the MSB is a sign bit
    # so max 32738; min -32737 per sample
    # reduced to 90% to avoid volume clipping
    scaledArray = 0.9 * array * 32767
    scaledArray = scaledArray.astype(np.int16)
    pySound = pygame.mixer.Sound(scaledArray)
    return pySound


def playArray(array, repeat=False):
    """
    Converts and plays a numpy array in the pygame mixer
    Function assumes array values range from 0 to 1
    Inputs:
        array (np.array): array to be played
    Returns:
        pySound (pygame.mixer.Sound): pygame sound object that was created
        pyChannel (pygame.mixer.Channel): mixer channel it is being played on
    """
    pySound = Array2PySound(array)
    k = -1 if repeat else 0
    pyChannel = pySound.play(k)
    return pySound, pyChannel


def noise(timePoint):
    """
    Generates a single random floats (0 to 1) or an array of random floats
    depending on the input
    Inputs:
        timePoint: time points to generate noise #  values dont actually matter
    Returns:
        A random float if input is an int or float
        An array of random floats the size of the input if it is an iterable
    """
    random.seed()
    if np.size(timePoint) > 1 :
        out = []
        for i in timePoint:
            out.append(2 * random.random() - 1)
        return np.array(out)
    else:
        return 2 * random.random() - 1


class Wave(Enum):
    """
    Enums for the wave types so they can easily be accessed
    Refrences:
        https://docs.python.org/3/library/enum.html
    """
    SAW = 0
    SINE = 1
    SQUARE = 2
    TRIANGLE = 3
    NOISE = 4


class SoundController:
    """
    pygame.mixer.Sound Wrapper that enables multiple object
    to control its volume or stop it
    Properties:
        knobs (dictionary): a dictionary of volumes to combine for the sound
        sound (pygame.mixer.Sound): the sound object to be controlled
    Methods:
        set_volume: set the volume of a knob in self.knobs
        stop: stops the sound from playing
    """
    def __init__(self, sound):
        """
        Create a SoundController object for the given sound
        Inputs:
            sound: pygame.mixer.Sound object to be controlled
        Returns:
            A SoundController Object
        """
        self.knobs = {}
        self.sound = sound
        self.alive = True

    def set_volume(self, vol, knobkey):
        """
        Set the volume of a knob (in the dictionary) with key knobkey
        Then combine all the knobs and set the final volume to the sound
        Inputs:
            knobkey: the name of the knob to change
            vol: the volume to set on that knob
        """
        # the volume the given knob
        self.knobs[knobkey] = vol
        # combine all the knobs
        combined = 1
        for key, value in self.knobs.items():
            combined *= value
        # set the combined volume on the sound
        self.sound.set_volume(combined)

    def stop(self):
        """
        Stops wrapped sound from playing
        """
        self.sound.stop()


#####################
# THE MAGIC STARTS HERE
####################
class Oscillator:
    """
    The Oscillator class is for defining a new signal generator. An Oscillator
    can be of 5 forms: SAW, SINE, SQUARE, TRIANGLE and NOISE
    Properties:
        form (int): the form of oscillator (0,1,2,3,4) or using the Wave Enum
        scale (float): Amplitude of the waveform
        shift (float): Phase shift of the waveform in radians
    Methods:
        getToneData: get array data at a given frequency
        plot: plot the waveform at a given frequency
        play: play a given frequency for some duration
    """

    def __init__(self, form=Wave.SQUARE, scale=1, shift=0):
        """
        Create a Oscillator with all its properties
        Inputs:
            form, scale and shift : same as properties
        Returns:
            An Oscillator Object
        """
        self.form = form
        self.scale = scale
        self.shift = 0

    def getToneData(self, freq, dur, singular=False):
        """
        Get the signal data of this oscillator at frequency "freq" for "dur"
        amout of time. If singular is true, the amplitude at a single time
        "dur" is returned instead
        Inputs:
            freq (float): frequency of data to generate
            dur (float): duration of the outpu waveform
            singular (bool): return data for a single point
        Returns:
            output: A list of amplitudes or a single amplitude of the
            oscillator's wave
        """
        if singular:
            t = dur
        else:
            # create an array of time points to calculate amplitudes for
            t = np.linspace(0, dur, dur * sample_rate, False)
        # convert the time point/s to radians
        theta = 2 * float(np.pi) * freq * t + self.shift
        # compute coresponding wave form
        waveforms = {
            Wave.SINE: np.sin(theta),
            Wave.SAW: signal.sawtooth(theta, 0),
            Wave.SQUARE: signal.square(theta),
            Wave.TRIANGLE: signal.sawtooth(theta, 0.5),
            Wave.NOISE: noise(theta)
        }

        output = self.scale * waveforms.get(self.form)
        return output

    def play(self, freq, dur):
        """
        play the Signal Data of this oscillator at frequency "freq" for "dur"
        amout of time.
        Inputs:
            freq (float): frequency of data to generate
            dur (float): duration of the outpu waveform
        Returns:
            pySound: pygame.mixer.Sound object that was created
        """
        tone = self.getToneData(freq, dur)
        pySound, pyChannel = playArray(tone)
        return pySound

    def plot(self, freq, dur):
        """
        Plot the tone data at frequency "freq" for duration "dur" to current
        figure/plot
        Inputs:
            freq (float): frequency (Hz) of the data to be plotted
            dur (float): duration of data to be plotted
        """

        y = self.getToneData(freq, dur)
        t = np.linspace(0, dur, y.size)
        plt.plot(t, y)


class Synth:
    """
    The Sound Synthesizer Class
    Properties:
        sources (list): list of Oscillator objects the synth combines
        ffilter (object): A Filter object (removes unwanted frequencies)
        adsr (object): An Envelope object (controls volume while note plays)
            controls the volume by time period: Attack,Decay,Sustain,Release
        lfo (object): A LFO object (controls volume while note plays)
            controls the volume using an oscillator
        sustains (dictionary): list of SoundController object currently active.
            Keeps track of all the notes(frequency) in sustain.
        vol (float): synths master output volume
    Methods:
        getToneData: get array data for a note(frequency)
        draw: plot the waveform of a note(frequency)
        play: play a note(frequency)
        release: release a note(frequency)
    """
    def __init__(self, oscCount=2):
        """
        Create a Synth object with oscCount Oscillators.
        Inputs:
            oscCount: number of Oscillator Object to create and use
        Returns:
            A Synth Object
        """
        self.sources = []
        for i in range(oscCount):
            self.sources.append(Oscillator())
        self.adsr = Envelope()
        self.ffilter = Filter()
        self.lfo = LFO()
        self.sustains = {}
        self.vol = 1

    def getToneData(self, freq):
        """
        Generates 3 periods worth of sound data from all the oscillators
        Combines the arrays and normalizes the output to 1 (not averaged)
        Then the output is passed through the synth's Filter object
        The output is then scaled once more by the synth's master volume (vol)
        Inputs:
            freq (float): frequencies (Hz) of the data to be generated
        Returns:
            tone (np.array): 3 periods of combine and filtered source data
        """
        tone = 0
        period = 1 / freq
        for osc in self.sources:
            tone += osc.getToneData(freq, period * 3)
        tone /= np.amax(abs(tone))
        tone = self.ffilter.run(tone)
        tone = self.vol * tone
        return tone

    def draw(self, freq, width, height, dpi=100):
        """
        Plot the tone data for the given frequency
        Inputs:
            freq (float): frequencies (Hz) of the data to be plotted
            width (int): width of the output image
            height (int): height of the output image
            dpi (int): resolution of the output data
        Returns:
            image (pygame.Surface): pygame image of the plot
        """

        # initialize the matplotlib figure for the final image
        plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)

        # get the amplitude and time data of the synth at the given frequency
        y = self.getToneData(freq)
        dur = y.size / sample_rate
        t = np.linspace(0, y.size / sample_rate, y.size)

        # plot the wave data of each oscillator for the same duration
        # then plot the synth data after the source data
        for source in self.sources:
            source.plot(freq, dur)
        plt.plot(t, y)

        plt.ylim(-1.2, 1.2)
        plt.xlim(0, dur)
        plt.title("Premixer Sound Wave")

        # convert the plot to an image
        image = plt2Img(width, height)
        return image

    def play(self, freq):
        """
        Plays the synth at the given frequency (note)
        The sound is triggered/started but not stopped
        The given frequency (note) will only play if it is not already playing
        Inputs:
            freq (float): frequencies (Hz) of the sound to generate and play
        Returns:
            sController (SoundController object): the SoundController that
            controls the volume/properties of the generated sound object as it
            plays.
        """
        # initialize the key for this freq if it doesnt exist in self.sustains
        if str(freq) not in self.sustains:
            self.sustains[str(freq)] = None

        # if this frequency is currently empty / not playing, then play it
        if self.sustains[str(freq)] is None:
            # get tone data of the Synth at this frequency
            tone = self.getToneData(freq)
            # play the data and get the sound object as it plays
            pySound, pyChannel = playArray(tone, True)
            # create a SoundController object for that sound
            # this object is needed for the adsr and lfo to work together
            # in realtime
            sController = SoundController(pySound)
            # start the adsr and lfo on the sController
            self.adsr.start(sController, "adsr")  # thread
            self.lfo.start(sController, "lfo")  # thread
            # refrence the controller in the synths sustain dictionary
            # so that the sound can be released later
            self.sustains[str(freq)] = sController
            return sController
        else:  # dont play the sound and print and error
            print("Frequency: " + str(freq) + " has not been released!")

    def release(self, freq):
        """
        releases the sound of the given frequency
        Inputs:
            freq (float): frequencies (Hz) of the sound to stop
        """

        # get the SoundController object for the given frequency from the
        # synths sustain dictionary
        sController = self.sustains[str(freq)]
        # the adsr will stop the controller (& sound) when release is done
        self.adsr.release(sController, "adsr")  # thread
        # derefrence the controller for garbage collection
        self.sustains[str(freq)] = None


class Filter:
    """
    A class for running low pass, high pass and band pass filters on np.arrays
    Properties:
        mode (string): The Filter type: can be "low", "high" or "band"
        cuttoff (float): cuttoff frequency in Hz
        width (float): Width of band, used only in band pass
        mix (float): mix ratio, how much of the filtered sound is returned
        1 means no input signal and 0 means no output signal
        repeats (int): Number of times the filter is run
        order of butterworth = 1 + repeats
        enable (bool): Whether the Filter is enabled or not
    Methods:
        draw: plot the graph of the filter
        run: runs the filter on a given array
        __createButter__: Returns the coeffiencts/parameters
        of the butterworth filter
    """

    def __init__(self, mode='high', cuttoff=1000, width=10, repeats=4, mix=1):
        """
        Create a Filter object with the given parameters.
        Inputs:
            mode: The mode/filter type
            cuttoff: The Cuttoff (Hz)
            width: The band width
            repeats: number of times the array is refiltered
            mix: mix ratio
        Returns:
            A Filter Object
        """
        self.mode = mode
        self.cuttoff = cuttoff
        self.width = width
        self.mix = mix
        self.enabled = False
        self.repeats = repeats

    def draw(self, width, height, dpi=100):
        """
        Plot the frequency/scale graph of the filter
        Inputs:
            width (int): width of the output image
            height (int): height of the output image
            dpi (int): resolution of the output data
        Returns:
            image (pygame.Surface): pygame image of the plot
        """
        plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)

        # get the filter coefficients
        b, a = self.__createButter__()
        # get the frequency response of the filter
        angularFreq, response = signal.freqz(b, a)
        # convert from angular frequency to Hz
        realFreq = sample_rate * angularFreq / (2 * np.pi)

        # plot the data
        plt.semilogx(realFreq, abs(response))
        ticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k"]
        plt.xticks(ticks, labels)
        plt.xlim([20, 20000])
        plt.title("Filter/Equalizer")

        image = plt2Img(width, height)
        return image

    def run(self,  inputSignal):
        """
        Filters the inputSignal array
        Inputs:
            inputSignal (array): input signal array to be filtered
        Returns:
            outputSignal (array): filtered output signal
        """
        # Filter only runs if it is enable
        if self.enabled:
            # length of input signal
            origLen = len(inputSignal)
            # get filter coefficients
            b, a = self.__createButter__()
            # in order to avoid bad filtering on edge cases
            # the input signal is padded with itself
            paddedSignal = np.concatenate(
                (inputSignal, inputSignal, inputSignal), axis=None)
            # run the filter on the padded signal (sound array)
            outputSignal = signal.filtfilt(b, a, paddedSignal)
            # remove the padding after it has been filtered
            outputSignal = outputSignal[origLen:2 * origLen]
            # mix the input and output signal using the self.mix ratio
            outputSignal = (
                self.mix * outputSignal + (1 - self.mix) * inputSignal)
            return outputSignal
        else:  # otherwise input signal is passed through
            return inputSignal

    def __createButter__(self):
        """
        Calculates the coeffiecients of a butterworth filter with the object's
        properties
        Returns:
            butter (tuple): Numerator and Denominator Coefficients
        References:
            https://dsp.stackexchange.com/questions/49460/apply-low-pass-butterworth-filter-in-python
            https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
        """
        # calculate coefficients for low pass or high pass
        if self.mode in ['low','high']:
            # Normalize the frequency
            normalizedCuttoff = self.cuttoff / (sample_rate / 2)
            butter = signal.butter(
                1 + self.repeats, normalizedCuttoff, btype=self.mode)
        # calculate coefficients for band pass
        elif self.mode == 'band':
            low = self.cuttoff / (sample_rate / 2)
            high = (self.cuttoff + self.width) / (sample_rate / 2)
            butter = signal.butter(
                1 + self.repeats, [low, high], btype=self.mode)
        return butter


class Envelope:
    """
    A Linear Attack Delay Sustain Envelope that runs parralel with a
    SoundController object
    Properties:
        Adur (float): Attack duration
        ADval (float): Volume after attack and before decay (0<ADval<1)
        Ddur (float): Decay duration
        Sval (float): Volume during sustain (0<Sval<1)
        Rdur (float): Release duration
        enable (bool): Whether the Envelope is enabled or not
    Methods:
        draw: plot the graph of the Envelope
        start: runs the __start__ method as a thread
        __start__: Controls a given sound or SoundController for
                    Attack Decay and Sustain
        release: runs the __release__ method as thread
        __release__: Contols a given sound or SoundController for Release
    """

    def __init__(self):
        """
        Create an Envelope object
        Returns:
            An Envelope Object
        """
        self.Adur = 0.1
        self.ADval = 1
        self.Ddur = 0.1
        self.Sval = 0.8
        self.Rdur = 0.3
        self.enabled = True

    def draw(self, width, height, dpi=100):
        """
        Plot the time/volume graph for this envelope
        Note: Sustain time is taken as 1 second
        Inputs:
            width (int): width of the output image
            height (int): height of the output image
            dpi (int): resolution of the output data
        Returns:
            image (pygame.Surface): pygame image of the plot
        """
        # initialize the matplotlib figure for the final image
        plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)

        # calculate the points from the Envelope properties
        y = [0, self.ADval, self.Sval, self.Sval, 0]
        ADdur = self.Adur + self.Ddur
        ADSdur = ADdur + 1
        t = [0, self.Adur, ADdur, ADSdur, ADSdur + self.Rdur]

        # plot the points and label the graph
        plt.plot(t, y)
        plt.title("ADSR")

        # get the image of the plot and return it
        image = plt2Img(width, height)
        return image

    def start(self, sController, key):
        """
        Controls the volume knob 'id' of a sController object for the duration
        of Attack, Decay and Sustain.
        This function calls the __start__ function as a thread
        Inputs:
            sController (SoundController): Controller to be enveloped
            key (string): The key/name of the knob to be controlled
        Refrences:
            http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
        """
        # start the thread only if the Envelope is enabled
        if self.enabled:
            thread = Thread(target=self.__start__, args=(sController, key))
            thread.daemon = True
            thread.start()

    def __start__(self, sController, key):
        """
        See Envelope.Start
        """
        # start the volume of the knob at 0
        sController.set_volume(0, key)

        # change the volume during Attack time
        start = time.time()
        elapsed = 0
        while elapsed < self.Adur:
            # set the volume at the sampling rate (to prevet the loop from
            # running too fast, and  reduce cpu usage)
            time.sleep(1 / sample_rate)
            elapsed = time.time() - start
            # calculate the volume at the current time (linearly) and set it
            currentVol = self.ADval * elapsed / self.Adur
            sController.set_volume(currentVol, key)

        # change the volume during Decay time
        start = time.time()
        elapsed = 0
        while elapsed < self.Ddur:
            # set the volume at the sampling rate
            time.sleep(1 / sample_rate)
            elapsed = time.time() - start
            # calculate the volume at the current time (linearly) and set it
            currentVol = (
                self.ADval + (self.Sval - self.ADval) * elapsed / self.Ddur)
            sController.set_volume(currentVol, key)

        # change the volume  to the Sustain Volume (Sval)
        sController.set_volume(self.Sval, key)

    def release(self, sController, key):
        """
        Controls the volume knob 'key' of a sController object for the duration
        of Release. Then it stops the sController and kills it.
        This function calls the __release__ function as a thread
        Inputs:
            sController (SoundController): Controller to be enveloped
            key (string): The key/name of the knob to be controlled
        """
        thread = Thread(target=self.__release__, args=(sController, key))
        thread.daemon = True
        thread.start()

    def __release__(self, sController, key):
        """
        See Envelope.Release
        """
        if self.enabled:
            # Change the volume during release time
            start = time.time()
            elapsed = 0
            while elapsed < self.Rdur:
                # set the volume at the sampling rate
                time.sleep(1 / sample_rate)
                elapsed = time.time() - start
                # calculate the volume at the current time (linearly) and set it
                currentVol = self.Sval - self.Sval * elapsed / self.Rdur
                sController.set_volume(currentVol, key)

        # Stop the sController Sound
        sController.stop()
        # kill the SController
        sController.alive = False


class LFO:
    """
    A volume controlling Low Frequency Objescillator that runs parralel with a
    SoundController object
    Properties:
        osc (Oscillator): the LFO's oscillator
        freq (float): frequency of the LFO
        time (float): time the LFO was created
        mix (float): ratio between original and LFO sound
            1 means the LFO controls the knob completely
            0 means the sound is unaffected
        sync (bool): This determines wether the Oscillator starts with the
        start method (false) or from the creation of the object (true)
        active (list): list of SoundController objects being controlled
        enabled (bool): Whether the LFO is enabled or not
    Methods:
        draw: plot the graph of the LFO
        start: runs the __start__ method as a thread
        __start__: Controls a given sound or SoundController untill the
        controller dies
    """

    def __init__(self, form=Wave.SINE, freq=0.8):
        """
        Create an LFO object
        Inputs:
            form (int): the LFO's wave shape
            freq (float): frequency of the LFO
        Returns:
            An LFO Object
        """
        self.osc = Oscillator()
        self.osc.form = form
        self.freq = freq
        self.enabled = False
        self.active = []
        self.time = time.time()
        self.sync = True
        self.mix = 0.2

    def draw(self, width, height, dpi=100):
        """
        Plot the time/volume graph for this LFO
        Inputs:
            width (int): width of the output image
            height (int): height of the output image
            dpi (int): resolution of the output data
        Returns:
            image (pygame.Surface): pygame image of the plot
        """

        # initialize the matplotlib figure for the final image
        plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)

        # plot the osc (2 periods)
        dur = 2 / self.freq
        self.osc.plot(self.freq, dur)
        plt.ylim(-1.2, 1.2)
        plt.xlim(0, dur)
        plt.title("LFO")

        # get the plot as an image
        image = plt2Img(width, height)
        return image

    def start(self, sController, key):
        """
        Controls the volume knob 'key' of a sController object while it is
        still alive
        This function calls the __start__ function as a thread
        Inputs:
            sController (SoundController): Controller to be enveloped
            key (string): The key/name of the knob to be controlled
        """
        if self.enabled:
            thread = Thread(target=self.__start__, args=(sController, key))
            thread.daemon = True
            thread.start()

    def __start__(self, sController, key):
        """
        See LFO.Start
        """
        # keep track of this controller
        self.active.append(sController)
        # determine the oscilators start time depending on the sync
        if self.sync:
            start = self.time
        else:
            start = time.time()
        while sController in self.active and sController.alive:
            # work at half the sample rate
            time.sleep(1 / sample_rate)
            # elapsed is time since start
            elapsed = time.time() - start
            # get the amplitude of the wave  'elapsed' time since start
            amplitude = self.osc.getToneData(self.freq, elapsed, singular=True)
            # normalize it:
            # ie. from (-1,1) --> (0,1)
            vol = (amplitude + 1) / 2
            # calculate the mixed volume
            mixVol = vol * (self.mix) + (1 - self.mix)
            sController.set_volume(mixVol, key)
        # derefrence the controller for garbage collection
        # once it has been killed
        self.active.remove(sController)


if __name__ == "__main__":
    # dummy data, if synthEngine is run instead of imported
    mySynth = Synth(2)
    mySynth.sources[0].form = Wave.SINE
    mySynth.sources[1].form = Wave.SQUARE

    mySynth.sources[0].scale = 0.5
    mySynth.sources[1].shift = 2 * np.pi/3

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

    def myK(mySynth, k):
        mySynth.play(midi(k))
        time.sleep(0.100)
        mySynth.release(midi(k))
        time.sleep(1.00)

    while True:
        myK(mySynth, 70)
