'''
CS 591 Computational Audio Spring 2014
Author: Edwin Ko
Final Project: Prosodic Analysis
File: wordBoundary.py
Purpose: To detect and segment word boundaries
using simple and original techniques.
'''

import cmath
import array
import contextlib
import wave
from math import sin, cos, pi, log, sqrt

# reads in a wave file
def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params

# writes out a wave file
def writewav(fname, data, params):
    with contextlib.closing(wave.open(fname, "w")) as f:
        f.setparams(params)
        f.writeframes(data.tostring())
    print(fname + " written.")


def detectSilence(x, w, sr):
    """Detects the silences within a given sound file.

    Args:
      x: a list of data from the sound file.
      w: window size.
      sr: sample rate of sound file.

    Returns:
      silence: [[start, end]]
       That is, start refers to the start time of the silence interval
       and end refers to the end time of the same interval. This is a list
       of lists, where the inner lists refer to to the silence intervals.
       The length of the outer list is the number of silence intervals.
    """
    isSilence = False
    mean = averageAbsolute(x)
    sd = 3.0*standard_deviation(x)
    t = mean - sd
    silence = []
    length = len(x)/float(sr)

    window = w
    slide = window
    start = 0
    count = 0

    while (window < len(x)):
        
        windowMean = averageAbsolute(x[start:start + slide])

        if (windowMean < t) and (isSilence == False):
            silence.append([(start/float(sr))])
            isSilence = True
        elif (windowMean >= t) and (isSilence == True):
            silence[count].append((start/float(sr)))
            isSilence = False
            count += 1
        
        window += slide
        start += slide

    if len(silence[-1]) == 1:
        silence[-1].append(length)
    
    return silence


def locateWords(x, length):
    """Locates the words within a given sound file.

    Args:
      x: a list of data from the sound file.
      length: the length of the sound file in seconds.

    Returns:
      words: [[start, end]] 
       That is, start refers to the start time of the word interval
       and end refers to the end time of the same interval. Start and
       end are essentially considered word boundaries. This is a list
       of lists, where the inner lists refer to to the word intervals.
       The length of the outer list is the number of words.
    """
    
    words = []
    
    for i in range(len(x)-1):
        words.append([x[i][1], x[i+1][0]])
        
    if x[-1][1] != length:
        words.append([x[-1][1], length])
        
    if length > 2:
        for x, y in words:
            if (y-x) < 0.1:
                words.remove([x, y])
    else:
        for x, y in words:
            if (y-x) < 0.03:
                words.remove([x, y])
                
    print "There are roughly", len(words), "words in the file."
    
    return words

# this does not work
def detectStress(data, words, avg, sr):
    """Detects the stress in each word interval.

    Args:
      data: a list of data from the wave file.
      words: list of lists, inner lists are word intervals.
      avg: average amplitude of just the data within the word intervals.
      sr: sample rate of sound file.

    Returns:
      None: not yet implemented.
    """    
    current = 0
    word_interval = []
    
    for x, y in words:
        start = int(x*sr)
        end = int(y*sr)
        isStress = False 
        word_interval.append([])
        window = 700
        n = start+window
        
        while (n < end):
           
            windowMean = averageAbsolute(data[start:start+window])
            
            if (windowMean > avg) and (isStress == False):
                word_interval[-1].append(start/float(sr))
                isStress = True
            elif (windowMean <= avg) and (isStress == True):
                word_interval[-1].append(start/float(sr))
                isStress = False
                
            n += window
            start += window
            
    return None

def remove_sound(input, sounds, sr):
    """Removes the predicted words/silences from the sound file.

    Args:
      input: a list of data from the wave file.
      sounds: list of lists, word/silence boundaries.
        - if word intervals passed in, removes silences.
        - if silence intervals passed in, removes words.
      sr: sample rate of sound file.

    Returns:
      output: a list of data with corresponding sound intervals removed .
    """
    
    output = array.array("h")
    for x, y in sounds:
        start = int(x*sr)
        end = int(y*sr)
        for i in range(start, end):
            output.append(input[i])
    return output

# returns the maximum absolute value in window
def maximum(window):
    max = 0.0
    for i in range(len(window)):
       if abs(window[i]) > max:
          max = abs(window[i])
    return max

# returns the mean of the absolute values in window
def averageAbsolute(window):
    sum = 0.0
    for i in range(len(window)):
        sum += abs(window[i])
    average = sum/len(window)
    return average

# returns standard deviation of absolute values in window
def standard_deviation(window):
    sum = 0.0
    avg = averageAbsolute(window)
    for i in range(len(window)):
        sum = (abs(window[i]) - avg)**2
    return round(sqrt((sum/(len(window)-1))), 2)

# returns count the values cross zero in window
def zero_cross(window):
    cross = 0
    prev_val = 0
    for i in range(len(window)):
        if (prev_val < 0 and window[i] < 0) or (prev_val >= 0 and window[i] >= 0) or i == 0:
            prev_val = window[i]
            continue
        else:
            prev_val = window[i]
            count += 1
    return count

def main():
    print "This is a simple script that computes a spectrogram."
    infileName = raw_input("Enter the name of the input .wav file: ")
    print "For best word count estimation:"
    print "    < 10 sec, use window size 700."
    print "    > 10 sec, use window size 300."
    answer = raw_input("Keep window size of 700? [Y/N] ")
    isAnswer = False
    if answer != ('Y' or 'N'):
        while(not(isAnswer)):
            answer = raw_input("Try again. Keep window size of 700? [Y/N]: ")
            if answer == ('Y' or 'N'):
                isAnswer = True
    if answer == 'N':
        window = eval(raw_input("Enter the window size: "))
    else:
        window = 700

    data, params = readwav(infileName)
    length = len(data)/float(params[2])
    sample_rate = params[2]
    
    silences = detectSilence(data, window, sample_rate)
    words = locateWords(silences, length)
    
    word_data = remove_sound(data, words, sample_rate)
    ofilename = infileName[:-4] + "_" + str(window) +"_words.wav"
    outfile = open(ofilename, 'w')
    writewav(ofilename, word_data, params)
    outfile.close()
    
    silence_data = remove_sound(data, silences, sample_rate)
    ofilename = infileName[:-4] + "_" + str(window) +"_silence.wav"
    outfile = open(ofilename, 'w')
    writewav(ofilename, silence_data, params)
    outfile.close()
    
    
main() 

