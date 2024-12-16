import socketio

sio=socketio.Client()

@sio.event
def connect():
    print("connected to preproccessor")

@sio.event
def disconnect():
    print("disconnected from preprocessor")

@sio.on('image_array')
def image_array(packet):
    print(packet)

sio.connect('http://localhost:3334')
sio.wait()