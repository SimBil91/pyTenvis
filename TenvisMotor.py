from base.TenvisOutput import TenvisOutput
import urllib2

class TenvisMotor(TenvisOutput):
    
    # This table converts a vector-style direction to its command
    MOVELIST = {
        "00": "stop", 
        "0+": "up",
        "0-": "down",
        "+0": "right",
        "-0": "left",
        "++": "upright",
        "+-": "downright",
        "-+": "upleft",
        "--": "downleft",
        "ph": "hscan",
        "pv": "vscan",
        "ho": "home"
    }
    
    URI = "http://{0}/cgi-bin/hi3510/ptzctrl.cgi?-step=0&-act=%s&speed=45"

    def __init__(self, domain, user="admin", pwd="Penner12"):
        TenvisOutput.__init__(
            self, 
            domain, 
            TenvisMotor.URI, 
            user, 
            pwd
        )
        
        self.state = '00'
        
    def _to_symbol(self, v):
        if v > 0:
            return '+'
        if v < 0:
            return '-'
        else:
            return '0'
    
    def send_command(self, cmdstr): 
        stream = urllib2.urlopen(self.uri % cmdstr)
        result = stream.read()
        assert "ok" in result
        stream.close()
        
    def move(self, xy):
        move_symbol = self._to_symbol(xy[0]) + self._to_symbol(xy[1])
        cmdstr = TenvisMotor.MOVELIST[move_symbol]
        if cmdstr != self.state:
            self.send_command(cmdstr)
        self.state = cmdstr
      
        
if __name__ == "__main__":
    import pygame
    import sys
    
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        sys.exit(-1)
    
    pygame.init()
    screen = pygame.display.set_mode((320, 240))
    
    motor = TenvisMotor(sys.argv[1])
    
    def checkKeys():
        keys = pygame.key.get_pressed()
        x = 0
        y = 0
        if keys [pygame.K_a]:
            x = -1
        if keys [pygame.K_s]:
            y = -1
        if keys [pygame.K_d]:
            x = 1
        if keys [pygame.K_w]:
            y = 1
            
        motor.move([x, y])
            
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit()
        checkKeys()
        
        
