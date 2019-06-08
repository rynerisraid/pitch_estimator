import scipy.signal as signal
import numpy as np
def generate_frame_data(y, sr, win=1024, hop=441):
    n_frames = 1 + int(len(y)//hop)
    y_frame = np.zeros((win,n_frames))
    for index in range(n_frames):
        temp = y[index*hop:index*hop+win]
        y_frame[:,index] = np.pad(temp,(0,win-len(temp)),'constant',constant_values=0)
    x_frame = np.arange(0, len(y)/sr, hop/sr)
    return y_frame,x_frame

def autocorrelation_function(x):
    win_len = len(x)
    acf = [np.dot(x[0:win_len-w],x[w:win_len])*(1-w/win_len) for w in range(win_len)]
    return acf
def autocorrelation_function_seq(y_frame):
    n_win, n_frames = np.shape(y_frame) 
    T = []
    for index in range(n_frames):
        acf = autocorrelation_function(y_frame[:,index])
        argmax = np.argmax(acf[40:])+41
        T.append(argmax)
    return T
  
def acf_pitch_estimator(wave,sr, is_median_filter=False, order=9):
  y_frame, x_frame = generate_frame_data(wave,sr)
  T = autocorrelation_function_seq(y_frame)
  freq = [sr/item for item in T]
  if is_median_filter:
    freq = signal.medfilt(freq,order)
  return x_frame,freq