from SPARQLWrapper import SPARQLWrapper, JSON


def Query(flowid) :
    sparql = SPARQLWrapper("http://eb4.cs.umbc.edu:3050/ds/query")
    #sparql.setQuery("""
    query = 'PREFIX knacc: <http://www.knacc.arya.umbc.edu/univ.owl#> \n'
    query += 'SELECT ?flow ?accessDecision \n'
    query += '    WHERE {\n'
    query += '     ?flow a knacc:Flow. \n'
    query += '      ?flow knacc:hasFlowID knacc:' 
    query +=  str(flowid) + '. \n'
    query += '     ?accessDecision a knacc:AccessDecision. \n'
    query += '     ?flow knacc:hasAccessDecision ?accessDecision. \n'
    query += '   }'
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print( results)

    for result in results["results"]["bindings"]:
        print(result["flow"]["value"].split('#')[1] + " : ",)
        print(result["accessDecision"]["value"].split('#')[1])


