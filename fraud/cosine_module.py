from fraud.dynamic_sensitivity_useraccess_matrix import *
from math import sqrt
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing


def cosine_cal_1(trans):
	weights = {1:0.9,2:0.2,3:0.4,4:0.9,5:0.9,6:0.4,7:0.4,8:0.9,9:0.2,10:0.4,11:0.9,12:0.4,13:0.2,14:0.2,15:0.9}
	# (aub,sus_score) = AUB_generator(trans)
	# aub = np.array(aub_1)
	# aub_normalized = preprocessing.normalize(aub)
	# print (aub_normalized)
	sus_score = 0
	pickle_in = open("fraud/aub.pickle","rb")
	AUB = pickle.load(pickle_in)
	aub = AUB[trans[0]]
	seq = trans[3]
	count  = 1
	attr = len(seq)-1
	table = [0,0,0,0,0]
	# high = 0
	# low = 0
	# med = 0
	read = 0
	write = 0
	if (seq[0]==0):
		read = len(seq)-1
	else:
		write = len(seq)-1

	for i in range(1,len(seq)):
		# if weights[seq[i]]<0.3:
		# 	low+=1
		# elif weights[seq[i]]<0.6:
		# 	med+=1
		# else:
		# 	high+=1
		ind = int(seq[i]/10)
		table[ind] += 1


	aub_new = [sus_score,table[0],table[1],table[2],table[3],table[4],read,write]


	num = 0
	denom1 = 0
	denom2 = 0
	counter = 0
	cosine_dist = 0
	for aub_old in aub:
		if (aub_old[6]==0 and aub_new[6]==0) or (aub_old[7]==0 and aub_new[7]==0):
			for i in range(1,6):
				num += aub_new[i]*aub_old[i]
				denom1 += aub_new[i]*aub_new[i]
				denom2 += aub_old[i]*aub_old[i]
			cosine_dist = max(cosine_dist , num/(sqrt(denom1)*sqrt(denom2)))
			counter = counter + 1
		# print(cosine_dist)
	return (1-cosine_dist)




# print (cosine_cal([0,0,0,[1, 5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,9,9,9,9,9,9,5,5]]))
# pickle_in = open("malicious_attr_queries.pickle","rb")
# mal = pickle.load(pickle_in)
# print('*********')
# print(cosine_cal(mal[0]))
# print('*********')
# print(cosine_cal(mal[1]))
# pickle_in = open("sequences_with_noise.pickle","rb")
# mal1 = pickle.load(pickle_in)
# print('*********')
# print(cosine_cal(mal1[0]))
# print('*********')
# print(cosine_cal(mal1[1]))

# print (cosine_cal_1([0,0,0,[1, 12,10,22,35,45,35,45,35]]))
# print (cosine_cal_1([0,0,0,[0, 12,10,22,35,45,35,45,35]]))
# print (cosine_cal_1([0,0,0,[1, 12,10,22,35,45, 12,10,22,35,45, 12,10,22,35,45, 12,10,22,35,45, 12,10,22,35,45]]))
# print (cosine_cal_1([0,0,0,[0, 12,10,22,35,45,35,45,35,35,45,35,45,35,35,45,35,45,35,35,45,35,45,35,35,45,35,45,35,35,45,35,45,35,35,45,35,45,35,35,45,35,45,35]]))
# pickle_in = open("malicious_attr_queries.pickle","rb")
# mal = pickle.load(pickle_in)
# print('*********')
# print(cosine_cal_2(mal[0]))
# print('*********')
# print(cosine_cal_2(mal[1]))
# pickle_in = open("sequences_with_noise.pickle","rb")
# mal1 = pickle.load(pickle_in)
# print('*********')
# print(cosine_cal_2(mal1[0]))
# print('*********')
# print(cosine_cal_2(mal1[1]))



