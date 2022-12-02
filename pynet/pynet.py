import sys
import socket
import getopt
import threading
import subprocess

def is_valid_ip(ip):
    ip_octets = ip.split('.')
    if len(ip_octets) != 4:
        return False
    for ip_octet in ip_octets:
        try:
            ip_octet_int = int(ip_octet)
        except:
            return False
        else:
            if ip_octet_int < 2 or ip_octet_int > 254:
                return False
    return True

def is_valid_port(port):
    try:
        port = int(port)
    except:
        return False  # port is not an integer.
    else:
        return 0 < port < 65536  # Valid port numbers range from 1 to 65535.

def print_usage():
    print("Pynet Network Tool\n")
    print("Usage: pynet.py -t <target_host> -p <port>")
    print("-l --listen			- Listen on <target_host>:<port> for incoming connections")
    print("-e --execute=<file_to_run>	- Execute the give file upon receiving a connection")
    print("-c --command			- Initialize a command shell")
    print("-u --upload=<destination>	- Upon receiving a connection upload a file and write to <destination>\n")
    print("Examples: ")
    print("pynet.py -t 192.168.0.1 -p 5555 -l -c")
    print("pynet.py -t 192.168.0.1 -p 5555 -l -u=C:\\target.exe")
    print("pynet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'BlaBlaBla' | ./pynet.py -t 192.168.11.12 -p 135")
    sys.exit(0)
    
class Pynet:
    
    __slots__ = [
        '_listen', 
        '_command', 
        '_upload', 
        '_execute', 
        '_target', 
        '_upload_destination', 
        '_port',
        '_format'
    ]
    
    def __init__(self):
        self._listen = False
        self._command = False
        self._upload = False
        self._execute = ""
        self._target = ""
        self._upload_destination = ""
        self._port = 0
        self._format = 'utf-8'

    def _client_sender(self, buffer):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self._target, self._port))
            if len(buffer) > 0:
                client.send(buffer.encode(self._format))
            while True:
                recv_len = 1
                response = ''
                while recv_len > 0:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data.decode(self._format)
                    if recv_len < 4096:
                        break
                print(response, end='')
                buffer = input()
                buffer += '\n'
                client.send(buffer.encode(self._format))
        except:
            print(f'SOMETHING WENT WRONG!')
            client.close()

    def _server_loop(self):
        if len(self._target) == 0:
            self._target = '0.0.0.0'
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self._target, self._port))
        server.listen()
        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=self._client_handler, args=(client_socket, address,))
            client_thread.start()
            
    def _client_handler(self, client_socket, address):
        if len(self._upload_destination) > 0:
            file_buffer = b''
            while True:
                data = client_socket.recv(1024)
                if data is None:
                    break
                else:
                    file_buffer += data
            try:
                file_descriptor = open(self._upload_destination, 'wb')
                file_descriptor.write(file_buffer)
                file_descriptor.close()
                client_socket.send(f'Successfully saved file to {self._upload_destination}.\r\n'.encode(self._format))
            except:
                client_socket.send(f'Failed to save file to {self._upload_destination}.\r\n'.encode(self._format))
        if len(self._execute) > 0:
            output = self._run_command(self._execute)
            client_socket.send(output)
        if self._command:
            while True:
                client_socket.send(b'<pynet:#> ')
                cmd_buffer = ''
                while '\n' not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024).decode(self._format)
                response = self._run_command(cmd_buffer)
                client_socket.send(response)
            
    def _run_command(self, command):
        command = command.strip()
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = b'FAILED TO EXECUTE COMMAND.\r\n'
        return output
    
    def execute(self):
        if len(sys.argv[1:]) == 0:
            print_usage()
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "hle:t:p:cu",
                ['help', 'listen', 'execute', 'target', 'port', 'command', 'upload']
            )
        except getopt.GetoptError as error:
            print(error)
            print_usage()
        else:
            for option, value in opts:
                if option in ('-h', '--help'):
                    print_usage()
                elif option in ('-l', '--listen'):
                    self._listen = True
                elif option in ('-e', '--execute'):
                    self._execute = value
                elif option in ('-c', '--command'):
                    self._command = True
                elif option in ('-u', '--upload'):
                    self._upload_destination = value
                elif option in ('-t', '--target'):
                    self._target = value
                elif option in ('-p', '--port'):
                    self._port = int(value)
                # else:
                #     print('Unknown option:')
                #     print(f'Option={option}, value={value}')
                #     sys.exit(0)
            if not self._listen and len(self._target) > 0 and self._port > 0:
                buffer = sys.stdin.read()
                self._client_sender(buffer)
            if self._listen:
                self._server_loop()
            

if __name__ == '__main__':
    pynet = Pynet()
    pynet.execute()