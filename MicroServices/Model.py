import socketio
import cv2
import numpy as np
import time

l=[]
sio=socketio.Client()

@sio.event
def connect():
    print("connected to preproccessor")

@sio.event
def disconnect():
    print("disconnected from preprocessor")

@sio.on('image_array')
def image_array(packet):
    global l
    c=packet
    x=np.array(c)
    x=x.astype('float32')
    if(len(l)<10):
        l.append(x)
    else:
        sio.emit('AI_response','currently processing')
        time.sleep(2)
        sio.emit('prediction','true')
        l=[]


sio.connect('http://localhost:3334')
sio.wait()