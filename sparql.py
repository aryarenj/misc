from SPARQLWrapper import SPARQLWrapper, JSON

inp = {"Flow":"Flow002", "Message":"Message002", "SourceIP":"192.168.10.20", "DestIP":"20.20.20.20", "Protocol":"HTTP"}



def createQuery(inp):
    query = []
    query.append("knacc:" + inp["Flow"] + " a knacc:Flow.")
    query.append("knacc:" + inp["Flow"] + " knacc:hasFlowID knacc:" + inp["Flow"] + ".")
    query.append("knacc:" + inp["Message"] + " a knacc:Message.")
    query.append("knacc:" + inp["Flow"] + " knacc:hasMessage knacc:" + inp["Message"] + ".")
    query.append("knacc:" + inp["Message"] + " knacc:hasSourceIPAddress knacc:" + inp["SourceIP"] + ".")
    query.append("knacc:" + inp["Message"] + " knacc:hasDestinationIPAddress knacc:" + inp["DestIP"] + ".")
    query.append("knacc:" + inp["Message"] + " knacc:hasProtocol knacc:" + inp["Protocol"] + ".")
    query_contents = '\n'.join(query)
    return query_contents



def GenerateQuery(InsertDelete, inp):
    query_contents = createQuery(inp)
    query = []
    query.append("PREFIX knacc: <http://www.knacc.arya.umbc.edu/univ.owl#>")
    if InsertDelete == 1 :		#insert
        query.append("INSERT\n{")  
    elif InsertDelete == 0: 		#delete
        query.append("DELETE\n{")
    else:
        print("Invalid choice for Insert/Delete")
    query.append(query_contents)
    query.append("}\nWHERE\n{}")
    complete_query = '\n'.join(query)
    return complete_query


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


def InsertIndividualVariable(query):
    sparql = SPARQLWrapper("http://eb4.cs.umbc.edu:3050/ds/update")
    sparql.setQuery(query)
    sparql.query()
    print ("Updated the Individual")




#query = GenerateQuery(1, inp)
#print (query)
#InsertIndividualVariable(query)

#InsertIndividual()
