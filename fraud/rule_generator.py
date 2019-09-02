import pickle

pickle_in = open("fraud/patterns_with_noise.pickle","rb")
patterns = pickle.load(pickle_in)
# print(patterns)

read_rule_dict = {}

for i in range(0,5):
	read_rule_dict[i] = {}

for roleid in patterns.keys():
	rdsequences = patterns[roleid][0]
	for rdsequence in rdsequences:
		s = rdsequence[0]
		# print(s,len(rdsequence))
		# print(s not in rule_dict[roleid].keys())
		for ind in range(1,len(rdsequence)):
			if rdsequence[ind] not in read_rule_dict[roleid].keys():
				read_rule_dict[roleid][rdsequence[ind]] = []
				read_rule_dict[roleid][rdsequence[ind]].append(s)
			else:
				rules = read_rule_dict[roleid][rdsequence[ind]]
				if s not in rules:
					read_rule_dict[roleid][rdsequence[ind]].append(s)
			s = s + rdsequence[ind]


# print(read_rule_dict)
pickle_out = open("fraud/read_rules_with_noise.pickle","wb")
pickle.dump(read_rule_dict, pickle_out,protocol=2)
pickle_out.close()

write_rule_dict = {}

for i in range(0,5):
	write_rule_dict[i] = {}

for roleid in patterns.keys():
	rdsequences = patterns[roleid][1]
	# if roleid==0:
	# 	print(rdsequences)
	for rdsequence in rdsequences:
		s = rdsequence[len(rdsequence)-1]
		# print(s,len(rdsequence))
		# print(s not in rule_dict[roleid].keys())
		for ind in range(2,len(rdsequence)):
			if rdsequence[len(rdsequence)-ind] not in write_rule_dict[roleid].keys():
				write_rule_dict[roleid][rdsequence[len(rdsequence)-ind]] = []
				write_rule_dict[roleid][rdsequence[len(rdsequence)-ind]].append(s[::-1])
			else:
				rules = write_rule_dict[roleid][rdsequence[len(rdsequence)-ind]]
				if s not in rules:
					write_rule_dict[roleid][rdsequence[len(rdsequence)-ind]].append(s[::-1])
			s = s + rdsequence[len(rdsequence)-ind]


# print(write_rule_dict)
pickle_out = open("fraud/write_rules_with_noise.pickle","wb")
pickle.dump(write_rule_dict, pickle_out,protocol=2)
pickle_out.close()




