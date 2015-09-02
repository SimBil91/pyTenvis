import cv2
import cv
import sys
import numpy 
from modules.TenvisMotor import TenvisMotor
from threading import Thread, Lock
import time
class TenvisVideo():
    uri = "rtsp://{0}:554/12"
    def __init__(self, domain):
        self.uri = self.uri.format(domain)
        self.vcap = cv2.VideoCapture(self.uri)
        self.faceCascade = cv2.CascadeClassifier('face_default.xml')
        self.hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
        self.face_detected=-1
        self.motor=TenvisMotor(domain,'admin','Penner12')
        self.frame=None
        self.mutex=Lock()
        self.stop=False
        
    def calc_histogramm(self,ROI,frame):
        self.extract_hue(frame)
        sel = cv.GetSubRect(self.hue, tuple(ROI))
        cv.CalcArrHist( [sel], self.hist, 0)
        (_, max_val, _, _) = cv.GetMinMaxHistValue( self.hist)
        if max_val != 0:
            cv.ConvertScale(self.hist.bins, self.hist.bins, 255. / max_val)
        self.track_window=tuple(ROI)
            
    def extract_hue(self,frame):
        # Convert to HSV and keep the hue
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        self.hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.Split(hsv, self.hue, None, None, None)
        
    def track_object(self,frame):
        center_point=[0,0]
        self.extract_hue(frame)
        # Compute back projection
        backproject = cv.CreateImage(cv.GetSize(frame), 8, 1)
        # Run the cam-shift
        cv.CalcArrBackProject( [self.hue], backproject, self.hist )
        crit = ( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 100, 0.01)
        try:
            (iters, (area, value, rect), track_box) = cv.CamShift(backproject, self.track_window, crit)
            self.track_window = rect
            center_point=[self.track_window[0]+self.track_window[2]*0.5,self.track_window[1]+self.track_window[3]*0.5]
        except:
            print('error')

        try:
            cv.EllipseBox( frame, track_box, cv.CV_RGB(255,0,0), 3, cv.CV_AA, 0 )
        except:
            print('ellipse error')
        return frame,center_point
            
    def detect_faces(self,frame):
        #frame = cv2.resize(frame, (640, 360)) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        # Draw a rectangle around the faces
        for i in range(0,len(faces)):
        #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            faces[i][0]=faces[i][0]
            faces[i][1]=faces[i][1]
            faces[i][2]=faces[i][2]
            faces[i][3]=faces[i][3]
            faces[i][1]=faces[i][1]+int(0.2*faces[i][3])
            faces[i][3]=0.6*faces[i][3]
            faces[i][0]=faces[i][0]+int(0.2*faces[i][2])
            faces[i][2]=0.6*faces[i][2]
            
        return faces
    
    def pull_frames(self):
        while 1:
            self.mutex.acquire()
            ret,self.frame=self.vcap.read()
            self.mutex.release()
            time.sleep(0.0001)
        
    def follow(self,show):
        key=0
        framecount=0
        offset=80
        while(chr(key & 255)!='q' and self.stop!=True):
            if self.frame!=None:
                self.mutex.acquire()
                frame=self.frame
                self.mutex.release()
                if chr(key & 255)=='d':
                    self.face_detected=0
                if framecount%2==0:
                    faces=self.detect_faces(frame)
                    if faces!=():
                        self.calc_histogramm(faces[0],cv.fromarray(frame))
                        self.face_detected=1
                        center_point=(faces[0][0]+faces[0][2]/2,faces[0][1]+faces[0][3]/2)
                        if show:
                            for x,y,w,h in faces:
                                cv2.rectangle(numpy.asarray(frame), (x, y), (x+w, y+h), (0, 255, 0), 2)
                                cv2.circle(numpy.asarray(frame), tuple(map(int,center_point)), 1, (0, 255, 0))
                                cv2.circle(numpy.asarray(frame), (320,180), offset, (0, 0, 255))
                    elif self.face_detected==1:
                        self.face_detected=0
                if (self.face_detected==0):
                    frame,center_point=self.track_object(cv.fromarray(frame))
                    
                if framecount%1==0 and 'center_point' in locals():
                    self.motor.move_to_pos(center_point,[320,180],offset,[2,2])
                if show:
                    cv2.imshow('FlatBuddy', numpy.asarray(frame))
                framecount=framecount+1
                key=cv2.waitKey(10)
                    
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        exit()
    else:
        domain=sys.argv[1]
    video=TenvisVideo(domain)
    video.show()

