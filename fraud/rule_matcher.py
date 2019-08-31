from string_similarity_calculator import *
import pickle
def r_matcher(sequence):
	weights = {'a':0.9,'b':0.9,'c':0.9,'d':0.9,'e':0.9,'f':0.9,'g':0.9,'h':0.9,'i':0.9,'j':0.9,'k':0.9,'l':0.9,'m':0.9,'n':0.9,'o':0.9}
	if sequence[3][0]==0:
		pickle_in = open("read_rules_with_noise.pickle","rb")
		rules = pickle.load(pickle_in)
		matched_key_elements = 0
		
		if (len(sequence[3])<2):
			# print sequence
			exit()
		s = chr(int(sequence[3][1])+65)
		total_score = 0
		total_denom = 0
		for ind in range(2,len(sequence[3])):
			item_score = 0
			denom = 0
			if chr(int(sequence[3][ind])+65) in rules[sequence[0]].keys():
				for i in rules[sequence[0]][chr(int(sequence[3][ind])+65)]:
					score = sim_score(s,i)
					denom = len(s)
					if score>=item_score and len(i)<=len(s):
						item_score = score
						# denom = len(i)
			# total_score = total_score +  item_score #* weights[chr(int(sequence[3][ind])+65)] 
			# total_denom += denom*1.0
			if denom!=0:
				denom = denom*1.0
				total_score = max(total_score,item_score/denom)
			s = s + chr(int(sequence[3][ind])+65)
		# if total_score/total_denom==1:
		# 	print(sequence,total_denom,total_score)
		# 	print (rules[0])
		# 	exit()
		return total_score


	else:
		pickle_in = open("write_rules_with_noise.pickle","rb")
		rules = pickle.load(pickle_in)
		matched_key_elements = 0
		
		if (len(sequence[3])<2):
			# print sequence
			exit()
		s = chr(int(sequence[3][len(sequence[3])-1])+65)
		total_score = 0
		total_denom = 0
		for ind in range(2,len(sequence[3])-1):
			item_score = 0
			denom = 0
			if chr(int(sequence[3][len(sequence[3]) - ind])+65) in rules[sequence[0]].keys():
				for i in rules[sequence[0]][chr(int(sequence[3][len(sequence[3]) - ind])+65)]:
					score = sim_score(s[::-1],i)
					denom = len(s)
					if score>=item_score and len(i)<=len(s):
						# print (score)
						item_score = score
						# denom = len(i)
			# total_score = total_score + item_score #* weights[chr(int(sequence[3][len(sequence[3]) - ind])+65)]
			# total_denom += denom*1.0
			if denom!=0:
				denom = denom*1.0
				total_score = max(total_score,item_score/denom)
			s = s + chr(int(sequence[3][len(sequence[3]) - ind])+65)
		# if total_score/total_denom==1:
		# 	print(sequence,total_denom,total_score)
		# 	print (rules[0])
			# exit()
		# if total_score<0.5:
		# 	print(total_score,sequence[3],s)
		# 	for i in (rules[sequence[0]]).keys():
		# 		print(i,':',rules[sequence[0]][i])
		# 	exit()
		return total_score

# print r_matcher([0,1,0,[0,4,13,6,12,5,2]])
# print r_matcher([0,1,0,[0,5,7,4,12,2,1]])
# print r_matcher([0,1,0,[0,2,13,3,12,5,2]])