import pickle

def dynamic_sens():
	count = {}
	pickle_in = open("sequences_with_noise.pickle","rb")
	trans = pickle.load(pickle_in)
	for tran in trans:
		role = tran[0]
		atts = tran[3]
		ind=0
		if role in count.keys():
			for att in atts:
				if ind!=0:
					if att in count[role].keys():
						count[role][att] += 1 
					else:
						count[role][att] = 1
				ind+=1
		else:
			count[role] = {}
			for att in atts:
				if ind!=0:
					count[role][att] = 1
				ind+=1

	dyn_sen = {}
	for i in count.keys():
		dyn_sen[i] = {}
		for j in count[i].keys():
			dyn_sen[i][j] = (1/float(count[i][j]**0.2),ret_sens_mapping(count[i][j]))


	return dyn_sen



def user_access_matrix():
	count = {}
	pickle_in = open("sequences_with_noise.pickle","rb")
	trans = pickle.load(pickle_in)	
	for tran in trans:
		user = str(tran[0]) + str(tran[2])
		atts = tran[3]
		ind = 0
		if user in count.keys():
			for att in atts:
				if ind!=0:
					if att in count[user].keys():
						count[user][att] += 1 
					else:
						count[user][att] = 1
				ind+=1
		else:
			count[user] = {}
			for att in atts:
				if ind!=0:
					count[user][att] = 1
				ind+=1

	return count

def singulrity_index(dyn_sens,user_acc_mat):
	si_matrix = {}
	for role in range(0,5):
		for user in range(0,5):
			si_matrix[str(role)+str(user)] = {}
			for att in range(0,90):
				if att in dyn_sens[role].keys():
					si_matrix[str(role)+str(user)][att] = (user_acc_mat[str(role)+str(user)][att])/(dyn_sens[role][att][0])
	return si_matrix


def suspic_score(si_matrix):
	sus_score = {}
	for i in si_matrix.keys():
		sum = 0
		for j in si_matrix[i].keys():
			sum += si_matrix[i][j]
		sus_score[i] = sum
	return sus_score

def AUB_create(si_matrix,role,user):
	weights = {1:0.9,2:0.2,3:0.4,4:0.9,5:0.9,6:0.4,7:0.4,8:0.9,9:0.2,10:0.4,11:0.9,12:0.4,13:0.2,14:0.2,15:0.9}
	pickle_in = open("sequences_with_noise.pickle","rb")
	trans = pickle.load(pickle_in)
	#15 - 7
	AUB = {0:[],1:[],2:[],3:[],4:[]}

	for tran in trans:
		count  = 0
		# attr = 0
		# high = 0
		# low = 0
		# med = 0
		read = 0
		write = 0
		score = 0
		table = [0,0,0,0,0]

		if True:
			seq = tran[3]
			count += 1
			if seq[0]==0:
				read += len(seq)-1
			else:
				write += len(seq)-1
			map_att = []
			for i in range(1,len(seq)):
				# attr += 1
				ind = int((seq[i])/10)
				table[ind] += 1 
				# if weights[i]<0.3:
				# 	low += 1
				# elif weights[i]>0.3 and weights[i]<0.6:
				# 	med += 1
				# else:
				# 	high += 1
				# if (seq[i] not in map_att) and :
				# 	score = score + si_matrix[str(role) + str(user)][seq[i]]
				# 	map_att.append(seq[i])
			uid = str(role)+str(user)
			AUB[tran[0]].append([score,table[0]/count,table[1]/count,table[2]/count,table[3]/count,table[4]/count,read/count,write/count])

	return (AUB)



def ret_sens_mapping(count):
	
	if count<=3 :
		return 'low'
	elif count<=6 :
		return 'moderate'
	else:
		return 'high'



# print(dynamic_sens())
# print(user_access_matrix())
# # user_access_mat = user_access_matrix()
# # for i in user_access_mat.keys():
# # 	print (i)

def AUB_generator(trans):
	dyn_sens = dynamic_sens()
	user_acc_mat = user_access_matrix()
	si_matrix = singulrity_index(dyn_sens,user_acc_mat)
	sus_score = suspic_score(si_matrix)
	sus_score_query = 0
	pickle_out = open("si_matrix.pickle","wb")
	pickle.dump(si_matrix, pickle_out,protocol=2)
	pickle_out.close()
	pickle_out = open("sus_score.pickle","wb")
	pickle.dump(sus_score, pickle_out,protocol=2)
	pickle_out.close()
	map_sus = []
	aub = AUB_create(si_matrix,trans[0],trans[2])
	pickle_out = open("aub.pickle","wb")
	pickle.dump(aub, pickle_out,protocol=2)
	pickle_out.close()
	exit()
	# print (si_matrix)
	# for i in range(1,len(trans[3])):
	# 	if trans[3][i] not in map_sus:
	# 		sus_score_query += si_matrix[str(trans[0])+str(trans[2])][trans[3][i]]
	# 		map_sus.append(trans[3][i])
	# return (AUB_create(si_matrix,trans[0],trans[2]),sus_score_query)


# pickle_in = open("sequences_with_noise.pickle","rb")
# trans = pickle.load(pickle_in)

# AUB = AUB_generator(trans[0])
# print(len(AUB[0]),AUB[0])
# counter=0
# for i in trans:
# 	if i[0]==0 and i[2]==0:
# 		counter+=1
# 		print(i)

# print(counter)