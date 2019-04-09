from query_sparql import *
from sparql import *

def response(flow):
    print ("Arya Hello")

    sni = flow.server_conn.sni 
    SourceIP = flow.server_conn.ip_address[0]
    DestIP = flow.server_conn.source_address[0])
 
    inp = {"Flow":"Flow002", "Message":"Message002", "SourceIP":SourceIP, "DestIP":DestIP, "Protocol":"HTTP"}

    query = GenerateQuery(1, inp)
    print (query)
    InsertIndividualVariable(query)

    Query(inp["Flow"])


