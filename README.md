# pitch_estimator
F0 estimation for signal, and it could be used in music and audio signal processing. In singing voice, the F0 is related to musicial pitch, while other formants have bad effects. 
# autocorrealtion function

# Yin algorithm
'''
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
from pyYin import *

fs, data = wavfile.read("./wave_data/q1.wav")
data =data/32767 
processor = Yin(sample_rate=44100, buff_size=1024, over_lap=441, threshold=0.2)

freq = processor.get_pitch_full(data)
plt.plot(freq)
'''

# pYin
