from SPARQLWrapper import SPARQLWrapper, JSON
import sys


def InsertIndividual():
    sparql = SPARQLWrapper("http://eb4.cs.umbc.edu:3050/ds/update")
    sparql.setQuery("""\PREFIX knacc: <http://www.knacc.arya.umbc.edu/univ.owl#>
        INSERT
        {
          knacc:Flow_8 a knacc:Flow.
          knacc:Flow_8 knacc:hasMessage knacc:Msg_8.
          knacc:Msg_8 knacc:hasSourceIPAddress knacc:192.168.10.20.
          knacc:192.168.10.20 knacc:hasIPName "192.168.10.20".
          knacc:Msg_8 knacc:hasDestinationIPAddress knacc:20.20.20.20.
          knacc:20.20.20.20 knacc:hasIPName "20.20.20.20".
          knacc:Msg_8 knacc:hasProtocol knacc:HTTP.
        }
        WHERE
        {}"""
    )
    sparql.query()
    print ("Inserted")



def IPQuery(ip, bl_wh, ins_del, service):
    query = []
    query.append("PREFIX knacc: <http://www.knacc.arya.umbc.edu/univ.owl#> ")
    query.append(ins_del +"\n{")
    query.append("knacc:U_" + ip + " a knacc:" + bl_wh + ".")
    query.append("knacc:" + ip + " a knacc:IPAddress.")
    query.append("knacc:U_" + ip + " knacc:hasIPAddress knacc:" + ip + ".")
    query.append("knacc:" + ip + " knacc:hasIPName \"" + ip + "\".")
    if service == '1':
        query.append("knacc:U_" + ip + " knacc:hasService knacc:FileTransfer.")
        query.append("knacc:U_" + ip + " a knacc:WhiteListedEntity.")
    query.append("}\nWHERE\n{}")
    query_contents = '\n'.join(query)
    print (query_contents)
    return query_contents


def InsertIndividualIP(ip, bl_wh, ins_del, service):
    query = IPQuery(ip, bl_wh, ins_del, service)
    sparql = SPARQLWrapper("http://eb4.cs.umbc.edu:3050/ds/update")
    sparql.setQuery(query)
    sparql.query()
    print ("Updated the Individual")




InsertIndividualIP(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

