import socket
import sys
import csv


def parse_info(filename):
    data = []
    file = open(filename, 'r')    
    reader = csv.reader(file)
    for row in reader:
	    # session_id, IP_address, 0/1(enforce/request)
 	    data.append((row[0], row[1], row[2]))		
    return data[1]

	
def send_data(sock, data):
    # Send data
    message = str((data[0], data[2]))
    print message
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

   
def recv_response(sock):
    # Look for the response
    amount_received = 0
    amount_expected = 20
    byte_count = 20
	
    while amount_received < amount_expected:
        data = sock.recv(byte_count)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data    
	return data

def create_connection():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = parse_info(sys.argv[1])
    ip_address = data[1]
    print ip_address
    # Connect the socket to the port where the server is listening
    server_address = (ip_address, 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        send_data(sock, data)
        key = recv_response(sock)		
		
    finally:
		print >>sys.stderr, 'closing socket'
		sock.close()	
		
    return key

key = create_connection()
print key
