import client
import config
import time

def is_invalid_ip(ip):
    ip_octets = ip.split('.')
    if len(ip_octets) != 4:
        return True
    for ip_octet in ip_octets:
        try:
            ip_octet_int = int(ip_octet)
        except:
            return True
        else:
            if ip_octet_int < 2 or ip_octet_int > 254:
                return True
    return False
        
def is_invalid_port(port):
    try:
        port = int(port)
    except:
        return True  # port is not an integer.
    else:
        return port < 1 or port > 65535  # Valid port numbers range from 1 to 65535.

if __name__ == '__main__':
    print('-'*50)
    print('WELCOME TO SERVER TALK'.center(50))
    print('-'*50)
    server_ip = input('Enter the formatted server\'s ip address: ')
    while is_invalid_ip(server_ip):
        print('INVALID IP. RECHECK IT AND TYPE AGAIN!')
        time.sleep(1)
        server_ip = input('Enter the formatted server\'s ip address: ')
    server_port = input('Enter server\'s port: ')
    while is_invalid_port(server_port):
        print('INVALID PORT. RECHECK IT AND TYPE AGAING!')
        time.sleep(1)
        server_port = input('Enter server\'s port: ')            
    client = client.Client(
        server_ip=server_ip, 
        server_port=int(server_port)
    )
    print(f'CONNECTED TO SERVER AT ({server_ip}:{server_port}).')
    message = input(f'Message to send [\'{config.DISCONNECT_MESSAGE}\' to end connection]: ')
    while message.upper() != config.DISCONNECT_MESSAGE:
        client.send_message(message)
        print('SENT!')
        message = input(f'Message to send [\'{config.DISCONNECT_MESSAGE}\' to end connection]: ')
    client.send_message(config.DISCONNECT_MESSAGE)  # When the server receives this message it'll close the connection.
    