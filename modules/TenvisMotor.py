import urllib2
import time

class TenvisMotor():
     
    uri = "http://{0}/cgi-bin/hi3510/ptzctrl.cgi?-step=0&-act=%s&speed=100"

    def __init__(self, domain, user, pwd):
        self.uri = self.uri.format(domain)
        self.state = '00'
        self.auth_http(user,pwd)
        
    def auth_http(self,user, pwd):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager
        passman.add_password(None, self.uri, user, pwd)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # create the AuthHandler
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
    
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
    
    def _to_symbol(self, v):
        if v > 0:
            return '+'
        if v < 0:
            return '-'
        else:
            return '0'
    
    def send_command(self, cmdstr): 
        if cmdstr in self.MOVELIST.values():
            stream = urllib2.urlopen(self.uri % cmdstr)
            result = stream.read()
            assert "ok" in result
            stream.close()
        else:
            print('Movement not possible')
        
    def move(self, xy):
        move_symbol = self._to_symbol(xy[0]) + self._to_symbol(xy[1])
        cmdstr = TenvisMotor.MOVELIST[move_symbol]
        if cmdstr != self.state:
            self.send_command(cmdstr)
        self.state = cmdstr
    
    def nod_head(self,amount,repeat):
        self.send_command('up')
        time.sleep(amount)
        for i in range(1,repeat):
            self.send_command('down')
            time.sleep(amount*2)
            self.send_command('up')
            time.sleep(amount*2)
        self.send_command('down')
        time.sleep(amount)
        self.send_command('stop')
        
    def shake_head(self,amount,repeat):
        self.send_command('left')
        time.sleep(amount)
        for i in range(1,repeat):
            self.send_command('right')
            time.sleep(amount*2)
            self.send_command('left')
            time.sleep(amount*2)   
        self.send_command('right')
        time.sleep(amount)
        self.send_command('stop')
     
if __name__ == "__main__":
    import pygame
    import sys
    
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        exit()
    else:
        domain=sys.argv[1]
    
    pygame.init()
    screen = pygame.display.set_mode((320, 240))
    motor = TenvisMotor(domain,'admin','Penner12')
    
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
        
        
