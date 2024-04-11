import socket
import struct
import select
import argparse
import threading
import netifaces as ni 

def get_container_ip():
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # Connect to a known external server (Google DNS)
    container_ip = s.getsockname()[0]  # Get the local IP address assigned by Docker
    s.close()
    return container_ip

# Obtain container IP dynamically
# Might need to change interface name depending on the system
container_ip = get_container_ip()
container_port = 10000
print("Container IP address: " + container_ip + "\n")

# Multicast group information
multicast_group = '224.3.29.71'
multicast_port = 10000

# Create a UDP socket for multicast reception
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multicast_socket.bind((multicast_group, multicast_port))
multicast_socket.setblocking(0)

# Join the multicast group
mreq = struct.pack('4sL', socket.inet_aton(multicast_group), socket.INADDR_ANY)
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Create a UDP socket for unicast reception
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((container_ip, container_port))
client_socket.setblocking(0)

# Function to send unicast message
def send_message(destination_ip, message, port):
    # Create a UDP socket
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send the message to the destination IP address and port
        sender_socket.sendto(message.encode(), (destination_ip, port))
        print("Message sent successfully.")
    finally:
        # Close the socket
        sender_socket.close()

def receive_messages():
    while True:
        readable, _, _ = select.select([multicast_socket, client_socket], [], [])

        for sock in readable:
            if sock is multicast_socket:
                multicast_data, multicast_addr = multicast_socket.recvfrom(1024)
                print(f'Received multicast message from {multicast_addr}: {multicast_data.decode()}')
            elif sock is client_socket:
                unicast_data, unicast_addr = client_socket.recvfrom(1024)
                print(f'Received unicast message from {unicast_addr}: {unicast_data.decode()}')

# CLI setup
def main():
    parser = argparse.ArgumentParser(description='Send or listen for messages.')
    parser.add_argument('--send', action='store_true', help='Send a unicast message')
    parser.add_argument('--dest_ip', help='Destination IP address (required if --send is used)')
    parser.add_argument('--msg', help='Message to send (required if --send is used)')
    parser.add_argument('--port', default=10000, type=int, help='Destination port (default: 10000)')
    parser.add_argument('--listen', action='store_true', help='Start listening for messages')
    args = parser.parse_args()

    if args.listen:
        print("Node listening for messages...\n")
        receive_messages()
    elif args.send:
        if not args.dest_ip or not args.msg:
            parser.error("--send requires --dest_ip and --msg.")
        else:
            send_message(args.dest_ip, args.msg, args.port)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
