import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa
import time
import pyaudio

A_freq = 440

sample_rate = 44100
T = 1
t = np.linspace(0, T, T * sample_rate, False)

audio = np.sin(A_freq * 2 * np.pi * t)


audio *= 32767 / np.max(np.abs(audio))
# convert to 16-bit data
audio = audio.astype(np.int16)

# zoom = round(sample_rate/A_freq)

# bytestream = audio.tobytes()
# pya = pyaudio.PyAudio()
# stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=sample_rate, output=True)
# while True:
#     stream.write(bytestream)
# stream.stop_stream()
# stream.close()
#
# pya.terminate()


plt.plot(t, audio, 'x')
plt.show()

wave = sa.WaveObject(audio, 1, 2, sample_rate)
while True:
    playObj = wave.play()
    playObj.wait_done()
