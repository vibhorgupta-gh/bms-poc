def remove_unwanted(s1, s2):
	l1 = []
	for i in s1:
		l1.append(i)
	
	new_s2 = ''
	for i in s2:
		if i in l1:
			new_s2 += i

	l2 = []
	for i in new_s2:
		l2.append(i)

	new_s1 = ''
	for i in s1:
		if i in l2:
			new_s1 += i

	return (new_s1,new_s2)

def final_strings(pair,s1,s2):
	
	new_s1 = pair[0]
	final_s1 = '('
	dist = 1
	ind = 0
	# print new_s1
	for i in s1:
		if ind<len(new_s1) and i==new_s1[ind]:
			final_s1 = final_s1 + str(dist) + i
			dist = 1
			ind = ind + 1
			# print (i,ind)
		else:
			dist = dist + 1
	final_s1 += str(dist) + ')'

	new_s2 = pair[1]
	final_s2 = '('
	dist = 1
	ind = 0
	for i in s2:
		if ind<len(new_s2) and i==new_s2[ind]:
			final_s2 = final_s2 + str(dist) + i
			dist = 1
			ind = ind + 1
		else:
			dist = dist + 1
	final_s2 += str(dist) + ')'

	return (final_s1,final_s2)


def distance_matrices(new_pair,final_pair):
	
	new_s1 = new_pair[0]
	final_s1 = final_pair[0]
	l1 = []
	for i in new_s1:
		if i not in l1:
			l1.append(i)
	dist_dic_1 = {}
	l1_1 = l1 + [')']
	dist_dic_1['('] = {}
	for i in l1_1:
		dist_dic_1['('][i] = -1
	for i in l1:
		dist_dic_1[i] = {}
		for j in l1_1:
			dist_dic_1[i][j] = -1
	k = 0
	while (k<len(final_s1)):
		if ord(final_s1[k])>=48 and ord(final_s1[k])<=57:
			k = k+1
		else:
			j = k+1
			dist_till_now = 0
			dist = 0
			while (j<len(final_s1)):
				if ord(final_s1[j])>=48 and ord(final_s1[j])<=57:
					dist = dist*10 + int(final_s1[j])
					j=j+1
				else:
					dist_till_now += dist
					dist = 0
					if dist_dic_1[final_s1[k]][final_s1[j]]==-1 or dist_dic_1[final_s1[k]][final_s1[j]]>dist_till_now:
						dist_dic_1[final_s1[k]][final_s1[j]] = dist_till_now
					j=j+1
			k=k+1


	new_s2 = new_pair[1]
	final_s2 = final_pair[1]
	l2 = []
	for i in new_s2:
		if i not in l2:
			l2.append(i)
	dist_dic_2 = {}
	l2_2 = l2 + [')']
	dist_dic_2['('] = {}
	for i in l2_2:
		dist_dic_2['('][i] = -1
	for i in l2:
		dist_dic_2[i] = {}
		for j in l2_2:
			dist_dic_2[i][j] = -1
	k = 0
	while (k<len(final_s2)):
		if ord(final_s2[k])>=48 and ord(final_s2[k])<=57:
			k = k+1
		else:
			j = k+1
			dist_till_now = 0
			dist = 0
			while (j<len(final_s2)):
				if ord(final_s2[j])>=48 and ord(final_s2[j])<=57:
					dist = dist*10 + int(final_s2[j])
					j=j+1
				else:
					dist_till_now += dist
					dist = 0
					if dist_dic_2[final_s2[k]][final_s2[j]]==-1 or dist_dic_2[final_s2[k]][final_s2[j]]>dist_till_now:
						dist_dic_2[final_s2[k]][final_s2[j]] = dist_till_now
					j=j+1
			k=k+1

	# print dist_dic_2
	return (dist_dic_1,dist_dic_2)

def sim_s1_s2(s2,d1,d2):

	#d1 is the diStance dictionary for referring string
	#d2 is the distance dictionary for referred string

	i=1
	score = 0
	s2 = '(' + s2 + ')'
	while (i<len(s2)):
		j = i-1
		f = 1
		additional_distance = 0
		while d2[s2[j]][s2[i]] == -1 and j>0:
			additional_distance += d1[s2[j]][s2[j+1]] 
			j = j-1
			f = f+1

		# print (i,j,f,s2[i],s2[j])
		# print (s2[j],s2[i],abs(d1[s2[j]][s2[j+1]]-d2[s2[j]][s2[i]]+additional_distance),additional_distance)
		score = score + 1/((f*(abs(d1[s2[j]][s2[j+1]]-d2[s2[j]][s2[i]]+additional_distance)+1))*1.0)
		i = i+1
	return score

def sim_s2_s1(s1,d1,d2):

	#d1 is the diStance dictionary for referring string
	#d2 is the distance dictionary for referred string

	i=1
	score = 0
	s1 = '(' + s1 + ')'
	while (i<len(s1)):
		j = i-1
		f = 1
		additional_distance = 0
		while d2[s1[j]][s1[i]] == -1 and j>0:
			additional_distance += d1[s1[j]][s1[j+1]] 
			j = j-1
			f = f+1

		# print (i,j,f,s2[i],s2[j])
		# print (s2[j],s2[i],abs(d1[s2[j]][s2[j+1]]-d2[s2[j]][s2[i]]+additional_distance),additional_distance)
		score = score + 1/((f*(abs(d1[s1[j]][s1[j+1]]-d2[s1[j]][s1[i]]+additional_distance)+1))*1.0)
		i = i+1
	return score



def sim_score(X,Y):
	# X = "efahecfeagyhbffaebyxcgediy"
	# Y = "jmmandopbmqnaoqbjdnnamdocq"

	# new_pair = remove_unwanted(X, Y) 
	# final_pair = final_strings(new_pair,X,Y)
	# dist_pair = distance_matrices (new_pair,final_pair)
	# sim_score_1 = sim_s1_s2 (new_pair[1],dist_pair[1],dist_pair[0])
	# sim_score_2 = sim_s2_s1 (new_pair[0],dist_pair[0],dist_pair[1])
	i=0
	j=0
	score = 0
	while i<len(X) and j<len(Y):
		if X[i]==Y[j]:
			score = score + 1
			j = j+1
		i = i+1
	return score
	# return (sim_score_1 + sim_score_2)/2