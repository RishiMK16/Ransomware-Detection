import socketio
from scapy.all import sniff
import eventlet
import threading

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")  # Allow connections from any origin
app = socketio.WSGIApp(sio)  # Wrap the server in a WSGI app

# Function to capture and send packets
def packet_callback(packet):
    if packet.haslayer('TCP'):
        src_port = packet['TCP'].sport
        dst_port = packet['TCP'].dport


        payload = bytes(packet['TCP'].payload)
        payload_hex = payload.hex()

        #print(f"Source Port: {src_port}, Destination Port: {dst_port}")
        #print(f"Payload (Hex): {payload_hex}")

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



# Run the server
if __name__ == "__main__":
    

    # Run the sniffing function in a separate thread


    # Run the Socket.IO server
    print("Starting Socket.IO server...")
    eventlet.wsgi.server(eventlet.listen(("localhost", 3333)), app)
