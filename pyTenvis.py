from modules.TenvisAudio import TenvisAudio
from modules.TenvisVideo import TenvisVideo
from modules.TenvisMotor import TenvisMotor
import sys
from threading import Thread

__version__=0.1

class pyTenvis():
    def __init__(self,ip,usr,pwd):
        self.audio=TenvisAudio(ip)
        self.video=TenvisVideo(ip)
        self.motor=TenvisMotor(ip,usr,pwd)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: '+sys.argv[0]+' <ip_address> <user> <password>') 
        exit()
    else:
        domain=sys.argv[1]
        usr=sys.argv[2]
        pwd=sys.argv[3]
    IPCAM=pyTenvis(domain,usr,pwd)
    #IPCAM.audio.play_audio()
    t1 = Thread(target=IPCAM.video.pull_frames, args=())
    t2 = Thread(target=IPCAM.video.follow, args=(False,))
    t1.start()
    t2.start()
    t2.join()
    IPCAM.motor.nod_head(0.3,2)
    IPCAM.motor.shake_head(0.4,2)