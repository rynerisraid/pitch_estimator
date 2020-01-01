import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal





class Yin(object):
    def __init__(self):
        self.m_YINTHRESHOLD = 0.20


    def differenceFunction(self, wave, win, hop):
        '''

        :param wave: 音频幅值序列
        :param win: 窗长
        :param hop: 窗移
        :return: self.yin_buffer
        '''
        n_frames = int(len(wave)/hop)
        #填充序列
        pad_wave = np.pad(wave,(0,(n_frames+1)*hop+win+1-len(wave)),mode='constant',constant_values=0)
        yin_buffer = np.zeros((n_frames,win))
        print(yin_buffer.shape)
        for index in range(n_frames-1):
            t = index*hop  #帧数
            for tau in range(win):
                if tau ==0:
                    yin_buffer[index, tau]= 1
                else:
                    temp = pad_wave[t:t+win]-pad_wave[t+tau:t+win+tau]
                    yin_buffer[index, tau]= np.sum(temp*temp)
                    if yin_buffer[index,tau] <=0:
                        raise Exception("Error difference function")
        self.yin_buffer = yin_buffer
        self.n_frames = n_frames-1 #最后一帧不要了

    def cumulativeMeanNormalizedDifference(self):
        '''
        :param self.yin_buffer = yin_buffer
        :return: self.yin_buffer 累计均方误差和
        '''

        n_frames, buff_size = self.yin_buffer.shape
        '''running_sum = np.zeros((n_frames,))
        for tau in range(1, buff_size):
            running_sum += self.yin_buffer[:, tau]
            self.yin_buffer[:, tau] *= tau / running_sum
        '''
        for index in range(n_frames-1):
            running_sum = np.float(0.0)
            for tau in range(buff_size):
                running_sum+= self.yin_buffer[index,tau]
                if running_sum<= 0:
                    raise Exception("Error running sum, overflow at frame={}, tau={}".format(index,tau))
                self.yin_buffer[index,tau]*= tau/running_sum


    def estimatePitch(self,file_name, win, hop, tau_min=None, tau_max=None):
        sr, wave = wav.read(file_name)
        wave = np.array(wave,dtype=float)
        print('file name:{}, sample rate:{}'.format(file_name,sr))

        self.differenceFunction(wave, win, hop)
        self.cumulativeMeanNormalizedDifference()
        self.absoluteThreshold()



        freq = np.ones((self.n_frames,))
        for index in range(self.n_frames):
            if self.tauFrames[index] != -1:
                betterTau = self.parabolicInterpolation(self.yin_buffer[index,:],self.tauFrames[index])
                freq[index] = sr/betterTau
            else:
                freq[index] = -1

            '''
            if self.tauFrames[index] == -1:
                freq[index] = 0
            else:
                freq[index] = sr/self.tauFrames[index]
            '''
        self.freq = signal.medfilt(freq,5)

    def estimatePitchWave(self,wave, sr, win, hop, tau_min=None, tau_max=None):

        wave = np.array(wave,dtype=float)

        self.differenceFunction(wave, win, hop)
        self.cumulativeMeanNormalizedDifference()
        self.absoluteThreshold()



        freq = np.ones((self.n_frames,))
        for index in range(self.n_frames):
            if self.tauFrames[index] != -1:
                betterTau = self.parabolicInterpolation(self.yin_buffer[index,:],self.tauFrames[index])
                freq[index] = sr/betterTau
            else:
                freq[index] = -1

            '''
            if self.tauFrames[index] == -1:
                freq[index] = 0
            else:
                freq[index] = sr/self.tauFrames[index]
            '''
        self.freq = signal.medfilt(freq,5)

    def absoluteThreshold(self):
        n_frames, buff_size = self.yin_buffer.shape
        tauFrames = np.ones((n_frames,))
        for index in range(n_frames):

            for tau in range(20, buff_size):
                if self.yin_buffer[index,tau]<self.m_YINTHRESHOLD:
                    while tau+1 < buff_size and self.yin_buffer[index, tau+1] <self.yin_buffer[index, tau]:
                        tau+=1
                    break
            #print(index,tau)
            if tau == buff_size or self.yin_buffer[index,tau] >= self.m_YINTHRESHOLD:
                tauFrames[index]  = -1
            else:
                tauFrames[index] = tau

        self.tauFrames = tauFrames

    def parabolicInterpolation(self, yin_buffer, tauEstimate):
        #print(yin_buffer.shape)
        x0, x1, x2 = 0, 0, 0
        betterTau = 0
        if tauEstimate < 1:
            x0 = tauEstimate
        else:
            x0 = tauEstimate-1

        if tauEstimate+1 < yin_buffer.shape[0]:
            x2 = tauEstimate + 1
        else:
            x2 = tauEstimate

        if x0 ==tauEstimate:
            if yin_buffer[tauEstimate] <=yin_buffer[x2]:
                betterTau = tauEstimate
            else:
                betterTau = x2
        elif x2==tauEstimate:
            if yin_buffer[tauEstimate]<=yin_buffer[x0]:
                betterTau = tauEstimate
            else:
                betterTau = x0
        else:

            s0 = yin_buffer[int(x0)]
            s1 = yin_buffer[int(tauEstimate)]
            s2 = yin_buffer[int(x2)]
            if 2*s1-s2-s0 ==0:
                betterTau = -1
            else:
                betterTau = tauEstimate + (s2-s0)/(2*(2*s1-s2-s0))

        return betterTau




if __name__ == '__main__':
    proc = Yin()
    proc.estimatePitch('q1.wav',1024,441)
    import matplotlib.pyplot as plt
    plt.plot(proc.freq)
    plt.show()