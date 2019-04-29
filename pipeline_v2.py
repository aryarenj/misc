from query_sparql import *
from gateway_keyRequest import *
from sparql import *
import time
import datetime
count = 0
import os
import json
from mitmproxy import http

#data_dict = {}
count = 1
monitoring_conns = {}

def inspection(DestIP, monitoring_conns, curr_key, SourceIP, acc):
   global count
   print ("#####################################" + str(count))
   count += 1
   filter_cmd = "tcpdump -r test.pcap -w outTemp_"+ DestIP + ".pcap host " + DestIP
   print (filter_cmd)
   os.system(filter_cmd)
   time.sleep(3)
   create_json_cmd = "tshark -r outTemp_" + DestIP + ".pcap -T json > outTemp_" + DestIP + ".json"
   os.system(create_json_cmd)
   time.sleep(3)
   print ("STAT: Reading JSON")
   with open ("outTemp_" + DestIP + ".json" ) as json_file:
      data = json.load(json_file)
     
      for each_packet in data:
         print (each_packet)
         try:
           random_str = each_packet["_source"]["layers"]["ssl"]["ssl.record"]["ssl.handshake"]["ssl.handshake.random"]
           print ("++++++++++++++++++++++++++++++++++")
           packet_dest = each_packet["_source"]['layers']['ip']['ip.dst']
           print ("-----------------------------------")
           if packet_dest == DestIP:
              crandom = random_str.replace(":", "")
              print ("STAT: " + str(crandom))
              if not (crandom in monitoring_conns[curr_key]['ClientRandom']):
                 outfil = "output_folder/" + curr_key + ".ssl"
                 if not monitoring_conns[curr_key]['IsFirst']: 
                   create_connection(SourceIP, DestIP, 'MAND', crandom, outfil, monitoring_conns, curr_key)
                 else:
                   create_connection(SourceIP, DestIP, acc, crandom, outfil, monitoring_conns, curr_key)      #acc = 'MAND' for mandatoryinspection ; OPTL for optional
                   monitoring_conns[curr_key]['IsFirst'] = False
                 monitoring_conns[curr_key]['ClientRandom'].append(crandom)
              else:
                 print ("outside")

         except:
           continue


def request(flow: http.HTTPFlow):
  #print (dir(flow))
  #print (dir(flow.client_conn.connection.client_random))#.source_address[0])
  cr = flow.client_conn.connection.client_random()
  print (cr.hex()) #encode('ascii'))
  crandom = str(cr.hex())
  # print (flow.client_conn.ip_address)
  #ipp = flow.client_conn.ip_address[0]
  #ipss = ipp.split(":")
  #fin = ipss[len(ipss) - 1]
  #print (fin)
  #return
  ts= time.time()
  ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
  sni = flow.server_conn.sni
  DestIP = flow.server_conn.ip_address[0]
  ipv6src = flow.client_conn.ip_address[0]
  ipv6src_s = ipv6src.split(":")
  SourceIP = ipv6src_s[len(ipv6src_s) - 1] #flow.server_conn.source_address[0]
  Flowid = "Flowgit" + ts_str
  Message = "Message" + ts_str
  protocol = "HTTP"
  inp = {"Flow":Flowid, "Message":Message, "SourceIP":SourceIP, "DestIP":DestIP, "Protocol":protocol}
  print (inp)
  curr_key = SourceIP + "_"+ DestIP + "_" + protocol
  outfil = "output_folder/" + curr_key + ".ssl"

  #print (data_dict)
  curr_access_decision = ''

  # Getting Access Decision
  if True:
    all_mon_conns = monitoring_conns.keys()
    if curr_key in all_mon_conns:
      # If the key is found in the monitoring set
      curr_acccess_decision = monitoring_conns[curr_key]['AccessDecision']
     
    else:
      # Starting to see if we need to monitor new connection
      query = GenerateQuery(1, inp)
      InsertIndividualVariable(query)
      curr_access_decision = Query(Flowid)
      if curr_access_decision:
        print ("Current Access Decision is " + curr_access_decision)
      else:
        print ("Current Access Decision is None")
      monitoring_conns[curr_key] = {}
      #curr_access_decision = 'AllowConnection'
      monitoring_conns[curr_key]['AccessDecision'] = curr_access_decision
      monitoring_conns[curr_key]['ClientRandom'] = []
      monitoring_conns[curr_key]['IsFirst'] = True
      monitoring_conns[curr_key]['OPTLResult'] = False
      monitoring_conns[curr_key]['OPTLResultSet'] = False

  # Depending on access decision we will decide to monitor or not 

  if curr_access_decision == "MandatoryInspection":
     print ("Got Mandatory Inspection")
     if not (crandom in monitoring_conns[curr_key]['ClientRandom']):
       create_connection(SourceIP, DestIP, 'MAND', crandom, outfil, monitoring_conns, curr_key)
       monitoring_conns[curr_key]['ClientRandom'].append(crandom)
     else:
       print ("Session Key already Exist")
     #inspection(DestIP, monitoring_conns, curr_key, SourceIP, "MAND")


  if curr_access_decision == "BlockConnection":
     #flow.request.host = "mitmproxy.org"
     flow.response = http.HTTPResponse.make(418, b"The current action you have done is against the organizational policies. Please review it!. ",)


  if curr_access_decision == "OptionalInspection":
     print ("Got Optional Inspection")
     if monitoring_conns[curr_key]['OPTLResultSet']:
       if monitoring_conns[curr_key]['OPTLResult']:
         if not (crandom in monitoring_conns[curr_key]['ClientRandom']):
           create_connection(SourceIP, DestIP, 'MAND', crandom, outfil, monitoring_conns, curr_key)
           monitoring_conns[curr_key]['ClientRandom'].append(crandom)
           # If it is a new random and the user already said monitor
         else:
           print ("Optional but key exist")
       else:
         print ("Optional but user said no")
     else:
       print ("Optional but need to ask user")
       create_connection(SourceIP, DestIP, 'OPTL', crandom, outfil, monitoring_conns, curr_key)
       if monitoring_conns[curr_key]['OPTLResult']:
         print ("abc.py: User asked to monitor")
       else:
         print ("abc.py: User asked NOT to monitor")
     
     #inspection(DestIP, monitoring_conns, curr_key, SourceIP, "OPTL")


  if curr_access_decision == "AllowConnection":
     print ("Got AllowConnection")
