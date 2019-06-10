# pitch_estimator
F0 estimation for signal, and it could be used in music and audio signal processing. In singing voice, the F0 is related to musicial pitch, while other formants have bad effects. 
## autocorrealtion function

## Yin algorithm

wave, sr = librosa.load('q1.wav',sr=44100)</br>
x, freq = acf_pitch_estimator(wave,sr, is_median_filter=True, order=13)</br>
x, freq = acf_pitch_estimator(wave,sr, is_median_filter=False, order=13)</br>

## pYin
