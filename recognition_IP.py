#!/usr/bin/env python
# author: Simon Bilgeri, Munich, Germany
# date: March 2015
# This node uses Pyaudio, the speech recognition library (uses google speech api)
# currently: no own key used
# private key: AIzaSyD_RN5bb7QvX5YEHg5nWT2Q2D3PWA9dWwE
import speech_recognition as sr
import rospy
from std_msgs.msg import String
import TenvisAudio
import io
# Edit parameters
#r = sr.Recognizer(language = "en-US", key = "AIzaSyD_RN5bb7QvX5YEHg5nWT2Q2D3PWA9dWwE")
#r.pause_threshold = 0.8
#r.record(source, duration = None)
#r.listen(source, timeout = None)
#r.recognize(audio_data, show_all = False)
from std_srvs.srv import Empty
rec_state=0

def enable_recognition(state):
    global rec_state
    rec_state=1
    return []

def disable_recognition(state):
    global rec_state
    rec_state=0
    return []

class PipeStream(sr.AudioSource):
    def __init__(self, taudio):
        self.stream = None
        #taudio.start_stream()
        self.pipe=taudio.pipe

    def __enter__(self):
        self.SAMPLE_WIDTH = 2
        self.RATE = 16000 # sampling rate in Hertz
        self.CHANNELS = 1 # mono audio
        self.CHUNK = 1024 # number of frames s
        self.stream = self.pipe.stdout
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        #self.stream = None
        self.pipe.stdout.flush()
        
        
def callback(recognizer, audio):                          # this is called from the background thread
    global rec_state
    try:
            # listen for the first phrase and extract it into audio data
        if rec_state==0:
            result = recognizer.recognize(audio, True)
            pub.publish(str(result[0]))
            rospy.loginfo(result) 
        else:
            print('Reconition disabled')
    except:
        rospy.loginfo("Could not understand sentence!") 
        
if __name__ == '__main__':
    # Init node
    rospy.init_node('recognition_IP')
    # Init IP audio
    taudio=TenvisAudio.TenvisAudio('192.168.178.49')
    
    # init Publisher
    pub = rospy.Publisher('speech', String)
    # init Service
    s_en = rospy.Service('enable_recognition', Empty, enable_recognition)
    s_dis = rospy.Service('disable_recognition', Empty, disable_recognition)
    r = sr.Recognizer()
    r.energy_threshold = 1200 # microphone dependent
    r.pause_threshold = 1.2
    r.quiet_duration =0.8
    r.dynamic_energy_threshold = False
    # perform listining and recognizing
    while 1:
        with PipeStream(taudio) as source:                # use the default microphone as the audio source
            audio = r.listen(source) 
            print(r.energy_threshold)                  # listen for the first phrase and extract it into audio data
        try:
            # listen for the first phrase and extract it into audio data
            if rec_state==1:
                result = r.recognize(audio, True)
                pub.publish(str(result[0]))
                rospy.loginfo(result) 
               
            else:
                print('Recognition disabled')
        except:
            rospy.loginfo("Could not understand sentence!") 


