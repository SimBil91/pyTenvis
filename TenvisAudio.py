import subprocess
import pyaudio
import os

ip='192.168.178.48'
CHUNK = 1024
command=['avconv','-i', 'rtsp://'+ip+'/11','-vn','-f','wav','-max_delay','0', 'pipe:1']
FNULL = open(os.devnull, 'w')
pipe = subprocess.Popen(command, stdout = subprocess.PIPE, stderr=FNULL) 
#wf=wave.open(pipe.stdout.read())
p = pyaudio.PyAudio() 
stream = p.open(
                format = pyaudio.paInt16, 
                channels = 1, 
                rate = 8000, 
                output = True, 
                frames_per_buffer = 10000) 
# read data
data = pipe.stdout.read(1000)

# play stream (3)
while data != '':
    stream.write(data)
    data = pipe.stdout.read(1000)
    pipe.stdout.flush()
