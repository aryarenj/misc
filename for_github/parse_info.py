from mitmproxy import io, http
#from mitmproxy.io import FlowReader
from mitmproxy.exceptions import FlowReadException


fileout = open("out.txt", 'w' )

def get_info(flow):

        fileout.write(flow.server_conn.ip_address + "\n")
        fileout.write(flow.server_conn.sni + "\n")
        fileout.write(flow.server_conn.id + "\n")
        fileout.write(flow.server_conn.address + "\n")
        fileout.write(flow.server_conn.source_address + "\n")
        fileout.write(flow.server_conn.tls_version + "\n") 
        fileout.write(flow.client_conn.address + "\n")
        fileout.write(flow.client_conn.id + "\n")
        fileout.write(flow.client_conn.sni + "\n") 
        fileout.write(flow.client_conn.tls_version + "\n") 
        fileout.write(flow.client_conn.cipher_name + "\n") 
        fileout.write(flow.client_conn.clientcert + "\n")
        fileout.write (dir(flow.client_conn + "\n") + "\n")
        
        fileout.write (dir(flow.server_conn + "\n") + "\n")



