import socket
import sys
import csv
import datetime
import time

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
    print ( 'sending message')
    sock.send(b'hello')

   
def recv_response(sock, DestIP, outfile):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    filename = 'output_folder/received_file_' + DestIP + st
    f = None
    #f = open(outfile, 'ab')
    print ("file opened")
    first = True
    ret_val = False
    while True:
        print('receiving data...')
        data = sock.recv(1024)
        #print('data=%s', (data))
        if not data:
            break
        if first:
          first = False
          k = str(b'\x00')
          kk = str(data)
          #if k == kk: 
          print ("if k (" + k + ") = kk (" + kk + ")")
          if k == kk:
          #if str(data) == str('\x00'):

            print ("FOUND NOTNOTNOTNOTNONTONTONTONTONTONTONOTNOTNOT")
            ret_val = False
            break
          else:
            f = open(outfile, 'ab')
            ret_val = True

        # write data to a file
        f.write(data)
        print (data)
    if f:
      f.close()
      print('Successfully get the file')
    return ret_val


def create_connection(ip_address, DestIP, accessDecision, random, outfile, monitoring_conns, curr_key):
    sock = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip_address, 10000)
    print ( 'connecting to %s port %s' % server_address)
    sock.connect(server_address)

    print ( 'sending message')
    hello_msg = "hello," + DestIP + "," + accessDecision + "," + random
    print (hello_msg.encode('ascii'))
    sock.send(hello_msg.encode('ascii'))
    
    ret_response = recv_response(sock, DestIP, outfile)
    if accessDecision == 'OPTL':
      if  not ret_response:
        monitoring_conns[curr_key]['OPTLResultSet'] = True
        monitoring_conns[curr_key]['OPTLResult'] = False
        print ("ret_response: User asked NOT to monitor")
      else: 
        monitoring_conns[curr_key]['OPTLResultSet'] = True
        monitoring_conns[curr_key]['OPTLResult'] = True
        print ("ret_response: User asked to monitor")
    
      
		
    print ("closing socket")
    sock.close()	
		

#key = create_connection()
#print key
#create_connection('10.0.2.15')
