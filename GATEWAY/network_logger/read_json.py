

def get_curr_json(inp, st) :
  #print "Getting json from " + inp[st:]
  stack = []
  while st < len(inp) and inp[st] != '{':
    st += 1
  if st >= len(inp):
    return False, -1, -1
  stack.append('{')
  st += 1
  ret_st = st - 1
  while len(stack) > 0:
    #print inp[st]
    if st >= len(inp):
      return False, -1, -1
    if inp[st] == '{':
      stack.append('{')
    elif inp[st] == '}':
      stack.pop()
    st += 1
  #print "End is " + str(st - 1)
  ret_en = st - 1
  #print "JSON is " + inp[ret_st + 1: ret_en]
  return True, ret_st, ret_en

def get_key(inp, st):
  en = st
  while inp[en] != '"':
    en += 1
    if en == len(inp):
      return False, "", -1
  st = en
  en += 1
  while en < len(inp) :
    if inp[en] == '"' and inp[en - 1] != '\\':
      # Found end of key
      break
    else:
      en += 1
      if en == len(inp):
        return False, "", -1
  curr_key = inp[st:en + 1]
  en += 1
  if en == len(inp):
    return False, "", -1
  while en < len(inp) and inp[en] != ':':
    en += 1
  if en == len(inp):
    return False, "", -1
  else:
    return True, curr_key, en + 1
  '''
  while en < len(inp):
    if started:
  for i in range(st, len(inp)):
    
    if inp[i] == ':':
      curr_key = inp[st:i]
      curr_key = curr_key.strip()
      if len(curr_key) == 0:
        return False, "", -1
      next_ind = i + 1
      if curr_key [0] == '"': 
        curr_key = curr_key[1:]
      if curr_key[len(curr_key) - 1] == '"':
        curr_key = curr_key[:len(curr_key) - 1]
      curr_key = curr_key.replace(" ", '_')
      return True, curr_key, next_ind
  return False, "", -1
  '''

def get_value(inp, st):
  #print "get value from : " + str(inp[st:])
  while inp[st] == ' ' or inp[st] == '\t' or inp[st] == '\n':
    st += 1
  if inp[st] == '{':
    #print "Found JSON in Value"
    found_json, cst, cen = get_curr_json(inp, st)
    if found_json:
      curr_new_json = inp[cst + 1: cen]
      val = parse_jobj(curr_new_json)
      if cen == len(inp) - 1:
        return -1, val    
      else:
        while inp[cen] != ',':
          if cen == len(inp) - 1:
            return -1, val
          cen += 1
         
        return cen + 1, val
  elif inp[st] == '"':
    out = ''
    st += 1
    while st < len(inp) and inp[st] != '"': # or (st > 0 and inp[st - 1] != '\\' and inp[st] == '"') :
      out += inp[st]
      st += 1
    #print out  
    st += 1
    while st < len(inp) and inp[st] != ',':
      st += 1
    #print out
    if st < len(inp) and inp[st] == ',':
      next_ind = st + 1
      #print "found ,"
    else:
      next_ind = -1
      #print "found end"
    return next_ind, out
  else:
    out = ''
    while st < len(inp) and inp[st] != ',':
      out += inp[st]
      st += 1
      if st == len(inp):
        return -1, out
    if inp[st] == ',':
      next_ind = st + 1
    else:
      next_ind = -1
    return next_ind, out

    
    

def parse_jobj(inp): 
  #print "Parsing JSON Obj: " + inp
  fin_json = {}
  st = 0
  while True:
    found_key, curr_key, next_ind = get_key(inp, st)
    if not found_key:
      print "Error Parsing"
      return None
    curr_key = curr_key.strip('"')
    # print "Key: " + curr_key 
    #print inp[next_ind:]
    next_ind, val = get_value(inp, next_ind)
    #print "Value: " + str(val)
    ind = 1
    if curr_key in fin_json.keys():
      tmp_arr = []
      if type(fin_json[curr_key]) == type(tmp_arr):
        fin_json[curr_key].append(val)
      else:
        tmp_val = fin_json[curr_key]
        tmp_arr.append(tmp_val)
        tmp_arr.append(val)
        fin_json[curr_key] = tmp_arr
      '''
      t_curr_key = curr_key
      while t_curr_key in fin_json.keys():
      t_curr_key = curr_key.strip('"') + '_' + str(ind)
      #t_curr_key = '"' + t_curr_key + '"'
      print curr_key 
      print t_curr_key
      print '-----'
      ind += 1
      int '----'
      '''
    else:
      fin_json[curr_key] = val
    if next_ind == -1:
      return fin_json
    st = next_ind

def dumps(inp):
  found, st, en = get_curr_json(inp, 0)  
  curr_json = inp[st + 1: en]
  return parse_jobj(curr_json)
  
#print dumps(tdata)     
     
    


