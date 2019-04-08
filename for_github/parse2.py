from mitmproxy import io
#from mitmproxy.io import FlowReader
from mitmproxy.exceptions import FlowReadException

filename = 'out.txt'

with open(filename, 'rb') as fp:
    reader = io.FlowReader(fp)
    #while(1):

    for flow in reader.stream():
        print(flow.server_conn.ip_address)
        print(flow.server_conn.sni)
        #print(flow.server_conn.id)
        print(flow.server_conn.address)
        print(flow.server_conn.source_address)
        print(flow.server_conn.tls_version) 
        print(flow.client_conn.address)
        print(flow.client_conn.id)
        print(flow.client_conn.sni) 
        print(flow.client_conn.tls_version) 
        print(flow.client_conn.cipher_name) 
        print ("\n")       
        
        
        



