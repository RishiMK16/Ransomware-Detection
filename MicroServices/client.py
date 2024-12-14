import socket

c=socket.socket()
c.connect(('localhost',3333))
while True:
    data = c.recv(1024)  # Adjust buffer size if needed
    if not data:
        break  # Exit if the connection is closed
    print(data.decode())