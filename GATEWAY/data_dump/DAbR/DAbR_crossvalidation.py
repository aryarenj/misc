## syntax : "python DAbR_crossvalidation.py bad_IP_data.csv good_IP_data.csv"

import sys
from sets import Set
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import csv
from DAbR import *



def get_real_data(X_test, white_data):
	
	real_data_good, no_of_attr = create_data_dictionary(white_data)
	test_good_count = len(white_data)
	print "Total Good IP's used for testing : ",test_good_count

	real_data_bad, no_of_attr = create_data_dictionary(X_test)
	test_bad_count = len(X_test)
	print "Total Bad IP's used for testing : ",test_bad_count	

	return real_data_good, real_data_bad, test_good_count, test_bad_count


def DAbRScore_TP_FP(real_data, threshold, model, no_of_attr):
	good_detect =0.0
	bad_detect =0.0
	real_IP_data = {}

	for IP, IP_data in real_data.iteritems():
		real_IP_data = {}
		real_IP_data[IP] = IP_data		
		DAbRScore = getReputationScore(IP, real_IP_data, model, no_of_attr)

		if DAbRScore >= threshold:
			good_detect += 1
		if DAbRScore < threshold:
			bad_detect += 1

	print "Number detected as good ",good_detect
	print "Number detected as bad ",bad_detect
	
	return good_detect, bad_detect




def cross_validation(black_data, no_of_cross_val):

	dat = np.asarray(black_data)
	kf = KFold(n_splits=no_of_cross_val)
	kf.get_n_splits(dat)
	ct = 0

	tp_good_avg =[]
	fp_good_avg =[]
	tp_bad_avg =[]
	fp_bad_avg =[]

	for threshold in range(0, 10):	
		tp_good_avg.append(0.0)
		fp_good_avg.append(0.0)
		tp_bad_avg.append(0.0)
		fp_bad_avg.append(0.0)


	for train_index, test_index in kf.split(dat):
	
		print "\n---- Fold ", (ct+1)," ------"
		X_train, X_test = dat[train_index], dat[test_index]
		
		train_data, no_of_attr = create_data_dictionary(X_train)
		print "Total Good IP's used for model creation : ",len(X_train)

		model = CreateModel(train_data, no_of_attr, True)

		white_data = create_data_list(sys.argv[2])
		real_data_good, real_data_bad, test_good_count, test_bad_count = get_real_data(X_test, white_data)
				
		for threshold in range(0, 10):
			TP_good, FP_bad = DAbRScore_TP_FP (real_data_good, threshold, model, no_of_attr)	
			FP_good, TP_bad = DAbRScore_TP_FP (real_data_bad, threshold, model, no_of_attr)
			
			tp_good_avg[threshold] += float(TP_good/test_good_count)
			fp_good_avg[threshold] += float(FP_good/test_bad_count)
			tp_bad_avg[threshold] += float(TP_bad/test_bad_count)
			fp_bad_avg[threshold] += float(FP_bad/test_good_count)

		ct += 1

	return TP_FP_across_crossvalid(tp_good_avg, fp_good_avg, tp_bad_avg, fp_bad_avg, no_of_cross_val)
	

def TP_FP_across_crossvalid(tp_good_avg, fp_good_avg, tp_bad_avg, fp_bad_avg, no_of_cross_val):
	print "\n\nThreshold\t TP_Good\t FP_good \t TP_Bad \t FP_Bad"

	for threshold in range(0, 10) :
		tp_good_avg[threshold] = float(tp_good_avg[threshold]/no_of_cross_val)
		fp_good_avg[threshold] = float(fp_good_avg[threshold]/no_of_cross_val)
		tp_bad_avg[threshold] = float(tp_bad_avg[threshold]/no_of_cross_val)
		fp_bad_avg[threshold] = float(fp_bad_avg[threshold]/no_of_cross_val)
		print threshold,"\t\t",round(tp_good_avg[threshold],3),"\t\t" ,round(fp_good_avg[threshold],3),"\t\t",round(tp_bad_avg[threshold],3),"\t\t",round(fp_bad_avg[threshold],3)

 	return tp_good_avg, fp_good_avg, tp_bad_avg, fp_bad_avg



def plot_ROC(tp_good_avg, fp_good_avg, tp_bad_avg, fp_bad_avg):
	m = list(reversed(tp_good_avg))
	n = list(reversed(fp_good_avg) )

	plt.xlim((0,1.0))
	plt.ylim(0,1.0)
	plt.plot(n,m, 'k', label = 'Detection As Good')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')

	m = list(reversed(tp_bad_avg))
	n = list(reversed(fp_bad_avg) )

	plt.plot(n,m, 'k', linestyle='--', label = 'Detection as Bad' )
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	legend = plt.legend(loc='lower right', shadow=True)

	plt.show()




#------------------functions definitions over-----------------------------------	



def main():
	black_data = create_data_list(sys.argv[1])

	no_of_cross_val = 4
	tp_good_avg, fp_good_avg, tp_bad_avg, fp_bad_avg = cross_validation(black_data, no_of_cross_val)

	plot_ROC(tp_good_avg, fp_good_avg, tp_bad_avg, fp_bad_avg)



if __name__== "__main__":
	main()


