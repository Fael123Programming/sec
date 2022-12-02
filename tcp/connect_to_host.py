import socket

PORT = 80
FORMAT = 'utf-8'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    print(f'----- CONNECT TO A REMOTE HOST')
    host_name = input('Host name: ')
    host_ip = socket.gethostbyname(host_name)
    client.connect((host_ip, PORT))
    print(f'----- Connected to host: ({host_name}) at ({host_ip}:{PORT})')
    client.sendall("GET / HTTP/1.1\r\n\r\n".encode(FORMAT))
    print(f'----- Request sent to server...')
    response = client.recv(4096)
    print(f'----- Response received from the server:\n', response)