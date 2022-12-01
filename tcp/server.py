import socket
import threading
import config

class Server(socket.socket):
    
    __slots__ = ['_ip', '_port']
    
    def __init__(self, ip=socket.gethostbyname(socket.gethostname()), port=5050):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((ip, port))
        self._ip = ip
        self._port = port
        
    def start(self):
        print(f'SERVER RUNNING ON {self}.')
        self.listen()
        while True:
            try:
                client_socket, client_ip = self.accept()
                thread = threading.Thread(target=self._handle_client, args=(client_socket, client_ip))
                thread.start()
                print(f'ACTIVE CONNECTIONS => {threading.active_count() - 1}')
            except KeyboardInterrupt:
                self.close()
                print(f'\nSERVER AT {self} CLOSED.')
                break
                
    def _handle_client(self, client_socket, client_ip):
        client_address = f'{client_ip[0]}:{client_ip[1]}'  # ip:port
        print(f'({client_address}) CONNECTED.')
        while True:
            msg_length = int(client_socket.recv(config.HEADER_LENGTH).decode(config.ENCODE_DECODE_FORMAT))
            if msg_length is None:
                continue
            msg = client_socket.recv(msg_length).decode(config.ENCODE_DECODE_FORMAT)
            if msg.upper() == config.DISCONNECT_MESSAGE:
                print(f'({client_address}) HAS DISCONNECTED.')
                client_socket.close() 
                break
            else:
                print(f'({client_address}) SAYS => [{msg}]')
    
    @property
    def ip(self):
        return self._ip
    
    @property
    def port(self):
        return self._port
    
    def __str__(self):
        return f'({self._ip}:{self._port})'
