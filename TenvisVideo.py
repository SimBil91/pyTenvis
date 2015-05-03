from base.TenvisInput import TenvisInput
import cv2
import sys

class TenvisVideo(TenvisInput):
    uri = "rtsp://{0}:{1}@{2}:554/12"
    def __init__(self, domain, user="admin", pwd="Penner12"):
        TenvisInput.__init__(
            self, 
            domain, 
            TenvisVideo.uri, 
            user, 
            pwd
        )
        self.vcap = cv2.VideoCapture(self.uri)
        self.faceCascade = cv2.CascadeClassifier('face_default.xml')
    def detect_faces(self,frame):
        frame = cv2.resize(frame, (160, 120)) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame = cv2.resize(frame, (640, 480)) 
        return frame
            
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        domain='192.168.178.49'
        #print "Usage: %s <ip_address>" % sys.argv[0]
    else:
        domain=sys.argv[1]
    video=TenvisVideo(domain)
    key=0
    while(key!=1048689):
        ret, frame = video.vcap.read()
        #frame2=video.detect_faces(frame)

        cv2.imshow('FlatBuddy', frame)
        key=cv2.waitKey(25)

