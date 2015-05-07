from modules.TenvisAudio import TenvisAudio
from modules.TenvisVideo import TenvisVideo
from modules.TenvisMotor import TenvisMotor
import sys

class pyTenvis():
    def __init__(self,ip,usr,pwd):
        self.audio=TenvisAudio(ip)
        self.video=TenvisVideo(ip)
        self.motor=TenvisMotor(ip,usr,pwd)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: '+sys.argv[0]+' <ip_address> <user> <password>') 
        #exit()
        domain='192.168.178.49'
        usr='admin'
        pwd='Penner12'
    else:
        domain=sys.argv[1]
        usr=sys.argv[2]
        pwd=sys.argv[3]
    IPCAM=pyTenvis(domain,usr,pwd)
    #IPCAM.audio.play_audio()
    #IPCAM.video.show()
    IPCAM.motor.nod_head(0.3,2)
    IPCAM.motor.shake_head(0.4,2)