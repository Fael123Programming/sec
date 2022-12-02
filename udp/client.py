import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 80
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("UDP DATA".encode(FORMAT), (HOST, PORT))

data, address = client.recvfrom(4096)

print(data.decode(FORMAT))
