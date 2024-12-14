from scapy.all import sniff
import socket

s=socket.socket()
print("socket created")
s.bind(('localhost',3333))

s.listen(1)
print("waiting for connections")

while True:
    c,addr=s.accept()
    print("connected with ",addr)
    
    def packet_callback(packet):
        if packet.haslayer('TCP'):
            src_port = packet['TCP'].sport
            dst_port = packet['TCP'].dport
            
            payload = bytes(packet['TCP'].payload)
            payload_hex = payload.hex()

            #print(f"Source Port: {src_port}, Destination Port: {dst_port}")
            #print(f"Payload (Hex): {payload_hex}")
            #print("-" * 40)
            c.send(payload_hex.encode())

    sniff(iface='Wi-Fi', prn=packet_callback, store=0, count=0)
    c.close()
