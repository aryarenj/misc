from SPARQLWrapper import SPARQLWrapper, JSON


def Query() :
    sparql = SPARQLWrapper("http://eb4.cs.umbc.edu:3050/ds/query")
    sparql.setQuery("""
	PREFIX knacc: <http://www.knacc.arya.umbc.edu/univ.owl#>
	SELECT ?flow ?accessDecision
	WHERE {
	  ?flow a knacc:Flow.
	  ?accessDecision a knacc:AccessDecision.
	  ?flow knacc:hasAccessDecision ?accessDecision
	}"""
    )

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print( results)

    for result in results["results"]["bindings"]:
        print(result["flow"]["value"].split('#')[1] + " : ",  end='')
        print(result["accessDecision"]["value"].split('#')[1])


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


def InsertIndividualVariable(string):
    sparql = SPARQLWrapper("http://eb4.cs.umbc.edu:3050/ds/update")
    sparql.setQuery(string)
    sparql.query()
    print ("Inserted the variable Individual")



def CreateString():
    string = "\"\"\"PREFIX knacc: <http://www.knacc.arya.umbc.edu/univ.owl#>        INSERT        {           knacc:Flow_8 a knacc:Flow.           knacc:Flow_8 knacc:hasMessage knacc:Msg_8.           knacc:Msg_8 knacc:hasSourceIPAddress knacc:192.168.10.20.           knacc:192.168.10.20 knacc:hasIPName \"192.168.10.20\".           knacc:Msg_8 knacc:hasDestinationIPAddress knacc:20.20.20.20.           knacc:20.20.20.20 knacc:hasIPName \"20.20.20.20\".           knacc:Msg_8 knacc:hasProtocol knacc:HTTP.         }         WHERE         {}\"\"\""
    print (string)
    return string  

 

string = CreateString()
InsertIndividualVariable(string)

#InsertIndividual()
#Query()
