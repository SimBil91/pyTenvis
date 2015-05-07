import subprocess
import pyaudio
import os

class TenvisAudio():
    def __init__(self,ip):
        self.command=['avconv','-i','rtsp://'+ip+'/11','-ar', '16000','-vn','-f','wav', 'pipe:1']
        self.FNULL = open(os.devnull, 'w')
        self.start_stream()
    def start_stream(self):
        self.pipe = subprocess.Popen(self.command, stdout = subprocess.PIPE, stderr=self.FNULL) 
    def stop_stream(self):
        self.pipe.terminate()
    def play_audio(self):
        # read data
        p = pyaudio.PyAudio() 
        self.stream = p.open(
                format = pyaudio.paInt16, 
                channels = 1, 
                rate = 16000,
                output = True, 
                frames_per_buffer = 1000) 
        data = self.pipe.stdout.read(100)
        # play stream 
        while data != '':
            self.stream.write(data)
            data = self.pipe.stdout.read(100)
            #self.pipe.stdout.flush()
    
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        exit()
    else:
        domain=sys.argv[1]
    taudio=TenvisAudio(domain)
    taudio.play_audio()