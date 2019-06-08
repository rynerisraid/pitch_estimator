
import librosa
import numpy as np

'''
读取基频文件

'''
def read_pitch_file(filename):
  file = open(filename,mode='r',encoding='utf-8')
  content = file.readlines()
  freq = [float(line) for line in content]
  return freq

'''
读取标注文件

'''
def read_ground_truth(filename):
    file = open(filename,mode='r',encoding='utf-8')
    onset= []
    offset = []
    pitch = []
    lines = file.readlines()
    for index in range(len(lines)):
        if index%3==0:
            onset.append(float(lines[index]))
        elif index%3==1:
            offset.append(float(lines[index]))
        else:
            pitch.append(float(lines[index]))
    return onset,offset,pitch


'''
评估算法性能
'''
def compute_raw_pitch_accuracy(pitch_file, ground_file):
    onset, offset, pitch_label = read_ground_truth(ground_file)
    pitch = read_pitch_file(pitch_file)
    
    counter = 0
    sum_counter = 0
    
    for index in range(len(onset)):
        start = int(onset[index]*100)
        end = int(offset[index]*100)
        for p in range(len(pitch[start:end])):
            sum_counter+=1
            if np.abs(pitch_label[index]-pitch[start+p])<=0.5:
                counter+=1

    return counter/sum_counter