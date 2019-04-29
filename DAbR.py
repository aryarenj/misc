## syntax : "python DAbR.py bad_IP_data.csv good_IP_data.csv <IP_address>"

import sys
#from sets import Set
import csv
import pickle

no_of_attr = 7

def create_vector(categories, data, ip, no_of_attr):
	ret_data = []
	for i in range(no_of_attr):
		try:
			ret_data.append(categories[i][data[ip][i]])
		except:
			ret_data.append(0.0)
	return ret_data
	

def conver_categorical_to_score(data, item_no):		#item_no = 2 means 3rd(ie after 0 and 1) column in the data after ip_address => 
													# 180.124.46.93, CN, true, Jiangsu, 4134, 1502727613.0,2  => here if item_no=0 means CN is chosen
	keys = data.keys()
	item = set()
	for i in keys:
		item.add(data[i][item_no])
	ret = {}
	for i in item:
		ret[i] = 0
	for i in keys:
		ret[data[i][item_no]] += 1
	ret_score = {}
	for i in item:
		ret_score[i] = float(ret[i])/float(len(data))
	return ret_score


			

def CreateModel (data, no_of_attr, isReturn):
	normFreq = []
	for i in range(no_of_attr):
		normFreq.append(conver_categorical_to_score(data, i))
		#normFreq is an array of dict. number of elements in the array = no of attr.   ; each dict has normalised freq for each attr value

	ips = data.keys()
	vec_dict = {}
		
	for i in ips:
		vec_dict[i] = create_vector(normFreq, data, i, no_of_attr)
		#returns dictionary of vectors for each training IP address

	largest=0.0
	for ip, attr in vec_dict.items():
		sum_sq = 0
		for i in range(no_of_attr):
			sum_sq = sum_sq + attr[i] * attr[i]

		dist = sum_sq ** (1/2.0)
		if dist > largest:
			largest = dist

	model = {}
	model["normFreq"] = normFreq
	model["largest"] = largest
	model["vectors"] = vec_dict

	if isReturn:
		return model
	with open("DAbR_data/DAbR_model.pkl", 'wb') as f:
		pickle.dump(model, f)


def get_DAbRScore(realVector, no_of_attr, largest):
	sq_sum = 0
	for i in range(no_of_attr):
		sq_sum = sq_sum + (realVector[i] * realVector[i])		
	DAbRScore = 10 - ( (sq_sum ** (1/2.0)) * 10 / largest)

	return DAbRScore


def readModel():
	with open("DAbR_data/DAbR_model.pkl", 'rb') as f:
		model = pickle.load(f)
	return model


	
def getReputationScore(IP, real_IP_data, model, no_of_attr):
	normFreq = model["normFreq"]
	largest = model["largest"]
	#print real_IP_data
	
	realVector = create_vector(normFreq, real_IP_data, IP, no_of_attr)
	DAbRScore = get_DAbRScore(realVector, no_of_attr, largest)
	return DAbRScore


def get_realIP_data(IP, train_data, real_data):
	train_IP = train_data.keys()
	real_IP = real_data.keys()
	
	IP_dict = {}
	if IP in train_IP:
		IP_dict[IP] = train_data[IP]
	elif IP in real_IP:	
		IP_dict[IP] = real_data[IP]
	else:
		attr_list = []
		for i in range(no_of_attr):
			attr_list.append("null")
		IP_dict[IP] = attr_list
	
	return IP_dict
	


def create_data_list(filename):
	con = []
	fil = open(filename, 'r', encoding = "ISO-8859-1")

	for i in fil:
		con.append(i.strip('\n').strip('\r'))

	dat1=[]
	for l in  csv.reader(con, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
		dat1.append(l)
	dat =dat1[1:]
	return dat


def create_data_dictionary(X_train):
	data ={}
	
	for i in X_train:
		app = []
		for j in range(1, len(i)):
			app.append(i[j])
		
		data[i[0]] = app  
		no_of_attr = len(app)
		
	return data, no_of_attr



#------------------functions definitions over-----------------------------------	

isnewModel = False

def DAbR_pipeline(IP):
	black_data, no_of_attr = create_data_dictionary(create_data_list("DAbR_data/bad_IP_data.csv"))		
	if isnewModel:
		CreateModel(black_data, no_of_attr, False)

	white_data, no_of_attr = create_data_dictionary(create_data_list("DAbR_data/good_IP_data.csv"))	
	
	model = readModel()
	real_IP_data = get_realIP_data(IP, black_data, white_data)

	DAbRScore = getReputationScore(IP, real_IP_data, model, no_of_attr)
	print (DAbRScore)



if __name__== "__main__":
	main()
