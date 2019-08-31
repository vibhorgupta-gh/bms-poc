import pickle

pickle_in = open("sequences_with_noise.pickle","rb")
transactions = pickle.load(pickle_in)

fin = []
for trans in transactions:
	for tran in trans:
		a = []
		a.append(tran[0])
		a.append(tran[1])
		a.append(tran[2])
		b = []
		for i in tran[3]:
			b.append(int(i))
		a.append(b)
		fin.append(a)

pickle_out = open("sequences_with_noise.pickle","wb")
pickle.dump(fin, pickle_out,protocol=2)
pickle_out.close()
pickle_in = open("sequences_with_noise.pickle","rb")
transactions = pickle.load(pickle_in)

print (transactions[0])