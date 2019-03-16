import sys

import os
import json
import read_json


def get_arr_ele(ret, st):
    br_cnt = 1;
    if st >= len(ret):
      return False, -1, -1
    while (ret[st] != '{'):
        st += 1
        if st >= len(ret):
            return False, -1, -1
    st += 1
    ret_st = st - 1
    while br_cnt > 0:
        if ret[st] == '{':
            br_cnt += 1
        elif ret[st] == '}':
            br_cnt -= 1
        st += 1 
        if st >= len(ret):
          return False, -1, -1
    ret_en = st - 1
    return True, ret_st, ret_en
 
def check_dupl(pair):
    out = {}
    for k, v in pair:
        if k in out:
            print k
        else:
            out[k] = v
    return out

def read_json_file(filname):
    fil = open(filname, 'r')
    ret = ''
    for i in fil:
        ret += (i.strip('\n') + ' ')
    fil.close()
    end = len(ret) - 1
    while (ret[end] == '\t' or ret[end] == ' ' or ret[end] == '\n'):
        end -= 1
    if ret[end] == ',':
        ret[end] = ']'
    elif ret[end] == ']':
        nop = 1
    else:
        ret += ']'
    con_arr = []
    cont_loop = True
    st = 0
    while (cont_loop):
        cont_loop, st, en = get_arr_ele(ret, st)
        #print st, " : " , en, " ", en - st
        curr_json = ret[st:en + 1]
        #con_arr.append(curr_json)
        if not cont_loop:
            break
        if st == -1 and en == -1:
            break
        curr_obj = read_json.dumps(curr_json)
        con_arr.append(curr_obj)
        #print curr_obj.keys()
        #kk = curr_obj["_source"]["layers"].keys()
        #for kki in kk:
        #  if kki.startswith("ssl"):
        #    print curr_obj["_source"]["layers"][kki]
        
        #print "------"
        #print len(curr_obj['"_source"'])
        #print "-----"
        #exit(0)
        st = en + 1
        #st = en + 1
        #exit(0)
    #print json.dumps(json.loads(ret[st:en + 1]), sort_keys=True,
    #                                       indent=4, separators=(',', ': '))
    print "Number of Rows: ", len(con_arr)
    
    #for i in con_arr:
    fil = open(filname + "_filt.json", "w")
    json.dump(con_arr, fil, sort_keys=True,
                   indent=4, separators=(',', ': ')) 
    fil.close()


    # Parse Each JSON Obj
    #for cobj in con_arr:
    #    parse_jobj(cobj)
    #con = json.loads(ret, object_pairs_hook=check_dupl)
    return con_arr

def filter_tls_json(jobj):
    for jpkt in jobj:
        layers = jpkt['_source']['layers']
        print json.dumps(layers,
                         sort_keys=True,
                         indent=4, separators=(',', ': '))

'''
        if 'ssl' in layers.keys():
                # if layers['ssl']['ssl.record']['ssl.record.content_type'] == '22':
                if 'ipv6' in layers.keys():
                    print layers['ipv6']['ipv6.src'] + ' ----> ' + layers['ipv6']['ipv6.dst']
                elif 'ip' in layers.keys():
                    print layers['ip']['ip.src'] + ' ----> ' + layers['ip']['ip.dst']
                else:
                    print "df" + layers.keys()
                print json.dumps(jpkt['_source']['layers'], #['ssl'],
                                           sort_keys=True,
                                           indent=4, separators=(',', ': '))
                print json.dumps(jpkt['_source']['layers']['ssl'], 
                                           sort_keys=True,
                                           indent=4, separators=(',', ': ')) 
                print "\n\n"
'''       

def filter_tls(filname):
    jobj = read_json_file(filname)
    #filter_tls_json(jobj)
    return jobj

def get_all_type_from_folder(curr_dir, types):
    all_files = os.listdir(curr_dir)
    ret = []
    for i in all_files:
        if i.endswith(types):
            ret.append(i)
    return ret

def create_ssl_json_from_pcap(inp_fil):
    output_fil = inp_fil + '.json'
    os.system("tshark -r " + inp_fil + " -T json -Y \"ssl\" > " + output_fil)
    
def main(curr_folder):
    pcaps = get_all_type_from_folder(curr_folder, ".pcap")
    for i in pcaps:
        create_ssl_json_from_pcap(curr_folder + '/' + i)

def main_create_fil(curr_folder):
    pcaps = get_all_type_from_folder(curr_folder, ".json")
    for i in pcaps:
      filter_tls(curr_folder + '/' + i)

def main_report(curr_folder):
    pcaps = get_all_type_from_folder(curr_folder, "_filt.json")
    out = []
    print pcaps
    for i in pcaps:
      out = []
      jo = read_jobjs(curr_folder + '/' + i)
      out = get_part_of_json(jo, out)
      js = json.dumps(out, sort_keys=True,
                       indent=4, separators=(',', ': '))

      fil = open(curr_folder + '/' + i + "_state.json", "w")
      fil.write(js) 
      #for j in out:
      #  fil.write(j + "\n")
      fil.close()
   
def create_json_newtype(tls_jobj, src, dest):
    curr = {}
    curr["tls_json"] = tls_jobj
    curr["src"] = src
    curr["dest"] = dest
    return curr
 
def get_part_of_json(jobj, out):
  #out = []
  for i in jobj:
    lay = i["_source"]["layers"]

    keys = lay.keys()
    if "ssl" in keys:
      json_to_print = {}
      if "ipv6" in keys:
        print(lay["ipv6"]["ipv6.src"] + " --------CISCOCISCO--------------> " + lay["ipv6"]["ipv6.dst"])
        
      else:
        #continue
        out.append(lay["ip"]["ip.src"] + " ----------------------> " + lay["ip"]["ip.dst"])
      for j in keys:
        if j.startswith("ssl"):
           if "ipv6" in lay.keys():
             tout_obj = create_json_newtype(lay[j], lay["ipv6"]["ipv6.src"], lay["ipv6"]["ipv6.dst"])
           elif "ip" in lay.keys():
             tout_obj = create_json_newtype(lay[j], lay["ip"]["ip.src"], lay["ip"]["ip.dst"])
           else:
             print ("No field found! \n Exiting")
             exit(0)
           #js = json.dumps(tout_obj, sort_keys=True,
           #                    indent=4, separators=(',', ': ')) 
           #out.append(js + "\n\n")
           out.append(tout_obj)
  return out


def read_jobjs(filname):
  fil = open(filname, 'r')
  jobj = json.load(fil)
  fil.close()
  return jobj


pcap_folder = sys.argv[1]
main(pcap_folder)
main_create_fil(pcap_folder)
main_report(pcap_folder)
#json_obj = filter_tls(pcap_folder)
#main(pcap_folder)
#print get_all_pcap_from_folder(sys.argv[1])
