import csv
import socket
import sys
from ast import literal_eval as make_tuple

IP_address = "10.0.2.15"
byte_count = 1024


def send_key_optional(conn, random, destIP):
    print ("\n\nYou have made a connection to "+ destIP )
    inp = input("Proceed with inspecting the connection? (Y/N):  ")    
    if inp.upper() == 'Y':
        send_key(conn, random)
    elif inp.upper() == 'N':
        conn.sendall(bytes("\00", 'ascii'))


    
def send_key_mandatory(conn, random):
    send_key(conn, random)


def send_key(conn, random):
    filename = 'sslkeylogfile.log'
    f = open(filename,'r')

    for line in f:
        if random in line:
            conn.send(line.encode('ascii'))
            print('Sent ',repr(line))

    f.close()
    print ('Done sending')



def recv_connection(sock):
    # Wait for a connection
    print ( 'Waiting for a connection')
    conn, client_address = sock.accept()

    print ( 'Got connection from ' , client_address)

    # Receive the data in small chunks and retransmit it
    data = conn.recv(byte_count)
    print('Data received', repr(data))
    data1 = data.decode('ascii').split(",")
    
    destIP = data1[1]
    access_decision = data1[2]
    random = data1[3]

    if access_decision == 'MAND':
        send_key_mandatory(conn, random)
    elif access_decision == 'OPTL':
        send_key_optional(conn, random, destIP)

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
 
