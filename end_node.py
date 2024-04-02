import socket
import struct

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Specify the multicast group address and port
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    data, address = sock.recvfrom(1024)
    print(f'Received {len(data)} bytes from {address}: {data.decode()}')