import socket
import config

class Client(socket.socket):
    
    __slots__ = ['_server_ip', '_server_port']
    
    def __init__(self, *, server_ip, server_port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self._server_ip = server_ip
        self._server_port = server_port
        self.connect((self._server_ip, self._server_port))
        
    def send_message(self, msg):
        encoded_message = msg.encode(config.ENCODE_DECODE_FORMAT)
        message_length = self._get_message_length(encoded_message)
        self.send(message_length)
        self.send(encoded_message)
        
    def _get_message_length(self, encoded_message):
        encoded_message_length = len(encoded_message)
        encoded_message_length_encoded = str(encoded_message_length).encode(config.ENCODE_DECODE_FORMAT)
        # Add padding of blank spaces until reach the size of config.HEADER_LENGTH.
        encoded_message_length_encoded_padded = encoded_message_length_encoded + b' ' * (config.HEADER_LENGTH - len(encoded_message_length_encoded))
        return encoded_message_length_encoded_padded
    