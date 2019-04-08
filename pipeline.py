from query_sparql import *
from sparql import *

inp = {"Flow":"Flow002", "Message":"Message002", "SourceIP":"192.168.10.3", "DestIP":"192.168.10.11", "Protocol":"HTTP"}

query = GenerateQuery(1, inp)
print (query)
InsertIndividualVariable(query)

Query(inp["Flow"])

#Query("Flow7")

