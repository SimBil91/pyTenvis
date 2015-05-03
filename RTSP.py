import socket
import base64

ip='wowzaec2demo.streamlock.net'
adr='rtsp://'+ip+'/vod/mp4:BigBuckBunny_115k.mov'
clientports=[4588,4589 ] # the client ports we are going to use for receiving video
auth=base64.b64encode('admin:Penner12')
# Create an TCP socket for RTSP communication
# further reading: 
# https://docs.python.org/2.7/howto/sockets.html
dest="DESCRIBE "+adr+" RTSP/1.0\r\nRequire: funky\r\nCSeq: 2\r\nUser-Agent: ONVIF Rtsp client\r\nAccept: application/sdp\r\nAuthorization: Basic "+auth+"\r\n\r\n"
opt="OPTION "+adr+" RTSP/1.0\r\nCSeq: 2\r\nUser-Agent: ONVIF Rtsp client\r\nAccept: application/sdp\r\nRequire: funky\r\nAuthorization: Basic "+auth+"\r\n\r\n"
setu="SETUP "+adr+"/trackID=1 RTSP/1.0\r\nCSeq: 3\r\nUser-Agent: ONVIF Rtsp client\r\nTransport: RTP/AVP;unicast;client_port="+str(clientports[0])+"-"+str(clientports[1])+"\r\nAuthorization: Basic "+auth+"\r\n\r\n"
play="PLAY "+adr+" RTSP/1.0\r\nCSeq: 5\r\nUser-Agent: python\r\nSession: SESID\r\nRange: npt=0.000-\r\n\r\n"

def sessionid(recst):
  """ Search session id from rtsp strings
  """
  recs=recst.split('\r\n')
  for rec in recs:
    ss=rec.split()
    # print ">",ss
    if (ss[0].strip()=="Session:"):
      return int(ss[1].split(";")[0].strip())


def printrec(recst):
  """ Pretty-printing rtsp strings
  """
  recs=recst.split('\r\n')
  for rec in recs:
    print rec


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip,554)) # RTSP should peek out from port 554



print
print "*** SENDING DESCRIBE ***"
print
printrec(dest)
s.send(dest)
recst=s.recv(4096)
print
print "*** GOT ****"
print
printrec(recst)
print
print "*** SENDING SETUP ***"
print
s.send(setu)
printrec(setu)
recst=s.recv(4096)
print
print "*** GOT ****"
print
printrec(recst)
idn=sessionid(recst)

serverports=getPorts("server_port",recst)
clientports=getPorts("client_port",recst)
print "****"
print "ip,serverports",ip,serverports
print "****"

s1=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind(("", clientports[0])) # we open a port that is visible to the whole internet (the empty string "" takes care of that)
s1.settimeout(5) # if the socket is dead for 5 s., its thrown into trash
# further reading:
# https://wiki.python.org/moin/UdpCommunication

# Now our port is open for receiving shitloads of videodata.  Give the camera the PLAY command..
print
print "*** SENDING PLAY ***"
print
play=setsesid(play,idn)
s.send(play)
recst=s.recv(4096)
print
print "*** GOT ****"
print
printrec(recst)
print
print