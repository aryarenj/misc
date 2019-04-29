import csv
import socket
import sys
from ast import literal_eval as make_tuple

IP_address = "10.0.2.15"
byte_count = 1024


'''
def parse_key(data_from_gateway):
    data_tuple = make_tuple(data_from_gateway)
    for each in session_keys:
	if data_tuple[0] == each[0]:
	    return each[1]    

'''

#def getRequiredKey(random):
    

def recv_connection(sock):
    # Wait for a connection
    print ( 'waiting for a connection')
    conn, client_address = sock.accept()

    print ( 'Got connection from ' , client_address)

    # Receive the data in small chunks and retransmit it
    data = conn.recv(byte_count)
    print('Server received', repr(data))
    data1 = data.decode('ascii').split(",")
    
    DestIP = data1[1]
    AccessDecision = data1[2]
    random = data1[3]
    #command = "grep " + random + " sslkeylogfile.log "
    #k = os.system(command)
    filename = 'sslkeylogfile.log'
    f = open(filename,'r')
    ''''
    l = f.read(1024)
    while (l):
            conn.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
    f.close()
    '''
     
    for l in f:
        if random in l:
            conn.send(l.encode('ascii'))
            print('Sent ',repr(l))
    
    f.close()
    print ('Done sending')
    conn.close()


def create_connection():
    # Create a TCP/IP socket
    sock = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (IP_address, 10000)
    print ( 'starting up on %s port %s' %server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)

    while True:
        recv_connection(sock)


create_connection()

