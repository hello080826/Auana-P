# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave , sys , os, time
import numpy as np

_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

sys.path.append(os.path.dirname(_work_dir))

from auana import Auana

print " Mic Recognition Demo\n"

chunk = 1024
channels = 2
samplerate = 44100
format = paInt16

import matplotlib.pyplot as plt  
plt.title("Diagram")
plt.xlabel('Record Time (s)')
plt.ylabel('Search Time (s)')


pa = PyAudio()

Time = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40]
#NUM = int((samplerate*Time)/float(chunk))
b=[]
save_buffer = []
#open audio stream    
stream = pa.open(
            format   = format, 
            channels = channels, 
            rate     = samplerate, 
            input    = True,
            frames_per_buffer  = chunk
            )
#while ("" == raw_input("Continue ?")):
for i in Time:
    N = int((samplerate*i)/float(chunk))
    print "  Listening..."
    # wave_data = []
    while N:
        save_buffer.append(stream.read(chunk))
        N -= 1

    wave_data = np.fromstring("".join(save_buffer), dtype = np.short)
    wave_data.shape = -1,2
    wave_data = wave_data.T

    start = time.time()
    name, confidence, db, position= Auana().stereo(wave_data[0],wave_data[1],samplerate)
    end = time.time() - start

    if name is not None:
        print "  Now Playing is: %s Accuracy: %.2f Position: %d'%d "%(name.split(".")[0],confidence,position/60,position%60)
    else:
        print "  Not Found!"
    print "-------------------------------------"
    print "                    Time Cost: %.3f"%end
    print " \n"
    b.append(end)
    save_buffer = []

# for a in xrange(2):
#     print Time[a],b[a],Time[a+1],b[a+1]
#     plt.plot([Time[a],b[a]],[Time[a+1],b[a+1]])
plt.plot(Time,b)
plt.show()  
#stop stream
stream.stop_stream()
stream.close()
del save_buffer

