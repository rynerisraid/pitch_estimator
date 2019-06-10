import numpy as np
class Yin:
  def __init__(self, sample_rate, buff_size, over_lap, threshold):

    
    self.sample_rate = sample_rate
    self.buff_size = int(buff_size/2)
    self.over_lap = over_lap
    self.threshold = threshold



  def difference_function(self, x, frame_index):
    win = self.buff_size
    df = np.zeros(win+1)
    t = frame_index
    #print(t)
    for tau in range(1,win):
      for j in range(win):
        delta=x[t+j]-x[t+j+tau]
        df[tau]+= delta*delta

    return df
   
    
        
  def cumulative_mean_normalized_difference_function_frame(self, df):
    df[0]=1
    cmdf = np.ones(len(df))
    s = 0.0
    for tau in range(1,len(cmdf)-1):
      s+=df[tau]
      if s==0.0:
        cmdf[tau] =0.0
      cmdf[tau] = (tau)*df[tau]/s
      

    return cmdf

  def absolute_threshold(self, cmdf):
    tau_flag = len(cmdf)-1
    for tau in range(2, len(cmdf)-1):
      if cmdf[tau] > self.threshold:
        continue
      while tau+1<len(cmdf) and cmdf[tau]>cmdf[tau+1]:
        tau += 1
        tau_flag = tau-1
      break
    if tau_flag>len(cmdf)-2:
      tau_flag = np.argmin(cmdf[65:])+65
    #print(tau_flag)
    return tau_flag
  
  def parabolic_interpolation(self, cmdf, tau_estimate):

    if tau_estimate<1:
      x0 = tau_estimate
    else:
      x0 = tau_estimate-1
    
    if tau_estimate+1 < self.buff_size:
      x2 = tau_estimate+1
    else:
      x2 = tau_estimate-1
    
    if x0 == tau_estimate:
      if cmdf[tau_estimate] <=cmdf[x2]:
        better_tau = tau_estimate
      else:
        better_tau = x2
    elif x2 == tau_estimate:
      if cmdf[tau_estimate] <= cmdf[x0]:
        better_tau = tau_estimate
      else:
        better_tau = x0
    else:
      s0 = cmdf[x0]
      s1 = cmdf[tau_estimate]
      s2 = cmdf[x2]
      if 2*s1-s2-s0==0:
        better_tau = -1
      else:
        better_tau = tau_estimate+(s2-s0)/(2 * (2 * s1 - s2 - s0))
    
    return better_tau
          


  def get_pitch(self, x, index):
    df = self.difference_function(x,index)
    cmdf = self.cumulative_mean_normalized_difference_function_frame(df)
    tau_estimate  = self.absolute_threshold(cmdf)
    if tau_estimate!=-1:
      better_tau = self.parabolic_interpolation(cmdf,tau_estimate)
      if better_tau!=-1:
        freq = self.sample_rate/(better_tau)
      else:
        freq = -1
    else:
      freq = -1

    print(index/44100,freq)
    return freq

    
  def get_pitch_full(self,x):
    overlap = self.over_lap

    n_frames = int((len(x)) / overlap)

    x = np.pad(x,(0,n_frames*overlap+self.buff_size*2-len(x)),'constant',constant_values=0)

    freq = []
    for frame in range(n_frames):
      start = frame * overlap
      temp = self.get_pitch(x, start)
      freq.append(temp)

    return np.array(freq)
