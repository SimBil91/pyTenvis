import cv2
import sys

class TenvisVideo():
    uri = "rtsp://{0}:554/11"
    def __init__(self, domain):
        self.uri = self.uri.format(domain)
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
        frame = opencvcv2.resize(frame, (640, 480)) 
        try:
            print(x,y)
        except:
            pass
        return frame
    def show(self):
        key=0
        while(chr(key & 255)!='q'):
            ret, frame = self.vcap.read()
            #frame=video.detect_faces(frame)
            cv2.imshow('FlatBuddy', frame)
            key=cv2.waitKey(25)
            
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        exit()
    else:
        domain=sys.argv[1]
    video=TenvisVideo(domain)
    video.show()

