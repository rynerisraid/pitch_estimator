# pitch_estimator
基频估计基本复现，自相关函数法，Yin算法
## autocorrealtion function
wave, sr = librosa.load('q1.wav',sr=44100)</br>
x, freq = acf_pitch_estimator(wave,sr, is_median_filter=True, order=13)</br>
x, freq = acf_pitch_estimator(wave,sr, is_median_filter=False, order=13)</br>


## Yin algorithm

from scipy.io import wavfile</br>
import numpy as np</br>
from pyYin import *</br>

fs, data = wavfile.read('q1.wav')</br>
data =data/32767</br>
processor = Yin(sample_rate=44100, buff_size=1024, over_lap=441, threshold=0.2)</br>
freq = processor.get_pitch_full(data)</br>



