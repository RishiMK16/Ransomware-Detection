import socketio
from scapy.all import sniff
import threading
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
 
# Create a Socket.IO server with gevent as the async mode
sio = socketio.Server(async_mode="gevent", cors_allowed_origins="*")  # Allow connections from any origin
app = socketio.WSGIApp(sio)  # Wrap the server in a WSGI app

# Function to capture and send packets
def packet_callback(packet):
    if packet.haslayer('TCP') and packet['TCP'].payload:
        src_port = packet['TCP'].sport
        dst_port = packet['TCP'].dport
        payload = bytes(packet['TCP'].payload)
        payload_hex = payload.hex()
        print(f"Emitting packet data: src_port={src_port}, dst_port={dst_port}, payload={payload_hex}")
        # Broadcast packet payload to all connected clients
        sio.emit("packet_data", {"src_port": src_port, "dst_port": dst_port, "payload": payload_hex})

# Start sniffing packets on the specified interface
def start_sniffing():
    print("Starting packet sniffing...")
    sniff(iface="Wi-Fi", prn=packet_callback, store=0, count=0)

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")
    sniffing_thread = threading.Thread(target=start_sniffing)
    sniffing_thread.daemon = True
    sniffing_thread.start()

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on("block")
def block(booleanval):
    if(booleanval==True):
        print("blocked")
# Run the server
if __name__ == "__main__":
    print("Starting Socket.IO server...")
    pywsgi.WSGIServer(("localhost", 3333), app, handler_class=WebSocketHandler).serve_forever()
