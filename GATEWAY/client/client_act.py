import csv
import socket
import sys
from ast import literal_eval as make_tuple

IP_address = "130.85.36.114"
byte_count = 100
filename = "key.csv"

def load_keyfile():
    data = []
    file = open(filename, 'r')    
    reader = csv.reader(file)
    for row in reader:
	# session_id, Key
 	data.append((row[0], row[1].strip()))		
    return data

def parse_key(data_from_gateway):
    data_tuple = make_tuple(data_from_gateway)
    for each in session_keys:
	if data_tuple[0] == each[0]:
	    return each[1]    



def recv_connection(sock):
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(byte_count)
            print >>sys.stderr, 'received "%s"' % data

            if data:
                return_key = parse_key(data)
                print >>sys.stderr, 'sending data back to gateway'
                connection.sendall(return_key)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()

def create_connection():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (IP_address, 10000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        recv_connection(sock)


session_keys = load_keyfile()
create_connection()
