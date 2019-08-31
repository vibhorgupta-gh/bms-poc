# from query_generator import generator
import pickle
# coding: utf-8

# In[1]:


def cum_weight(seq):
    val = 0.0
    for att in seq:
        val = val + att_sensitivity[att]
    return val/len(seq)


# In[2]:


class SeqTuple(object):
    def __init__(self, seq, tsmw):
        self.seq = seq
        self.cnt = 0
        self.swub = 0
        self.wsup = 0
        self.weight = cum_weight(seq)/tsmw


# In[3]:


def get_loc(pattern, seq):
    indices = []
    for ind in range(len(seq)):
        if seq[ind]==pattern[0]:
            flag = True
            for i in range(len(pattern)):
                if ind+i>=len(seq) or seq[ind+i]!=pattern[i]:
                    flag = False
                    break
            if flag==True:
                indices.append(ind)
    return indices


# In[4]:


def finding_WS(x, sdbi, r, thresh, sensitivity, tsmw):
    
    smw = {}
    # tid is transaction id
    for tid in sdbi:
        seq = sdbi[tid]
        smw_seq = 0
        for att in seq:
            smw_seq = max(smw_seq, sensitivity[att])
        smw[tid] = smw_seq
    
    TS = {}
    for tid in sdbi:
        seq = sdbi[tid]
        ind = get_loc(x, seq)
        #print(ind,x,seq)
        for i in range(ind[0]+r,len(seq)):
            subseq = list(x)+[seq[i]]
            if subseq not in TS.keys():
                ST = SeqTuple(subseq, tsmw)
                TS[tuple(subseq)] = ST
    
    for seqx in TS:
        for tid in sdbi:
            seq = sdbi[tid]
            ind = get_loc(seqx[-1], seq[r:])
            if len(ind)>0:
                seqx = tuple(seqx)
                TS[seqx].swub += smw[tid]/tsmw
                TS[seqx].cnt += 1
        TS[seqx].wsup = TS[seqx].weight*TS[seqx].cnt
    
    WFUBX = []
    WSX = []
    for pattern in TS.keys():
        # print(pattern,TS[pattern].swub,TS[pattern].wsup)
        if TS[pattern].swub >= thresh:
            WFUBX.append(pattern)
        if TS[pattern].wsup >= thresh:
            WSX.append(pattern)
    
    PIX = []
    for ix in WFUBX:
        PIX = PIX + list(ix)
    PIX = set(PIX)
    r = r+1
    
    for tid in sdbi.keys():
        seq = sdbi[tid]
        for att in seq:
            if att not in PIX:
                seq.remove(att)
        if len(seq) < r+1:
            del sdbi[tid]
    
    WSX = []
    WFUBX.sort()
    #print("hi",len(WFUBX))
    for seqx in WFUBX:
        sdbx = {}
        for tid in sdbi:
            seq = sdbi[tid]
            ind = get_loc(seqx[-1], seq[r-1:])
            if len(ind)>0:
                sdbx[len(sdbx.keys())] = list(seqx)+seq[ind[0]+r:]
        # print(seqx,sdbx,r)
        WSS = finding_WS(seqx, sdbx, r, thresh, sensitivity, tsmw)
        if len(WSS)==0 and TS[seqx].wsup >= thresh:
            WSS = WSS + [seqx]
        WSX = WSX + WSS
    return WSX


# In[5]:


def IWSPAN(sensitivity, sequences, thresh):
    
    smw = {}
    # tid is transaction id
    for tid in sequences.keys():
        seq = sequences[tid]
        #print(seq)
        smw_seq = 0
        for att in seq:
            smw_seq = max(smw_seq, sensitivity[att])
        #print(smw_seq)
        smw[tid] = smw_seq
        
    tsmw = 0.0
    for tid in smw:
        tsmw = tsmw + smw[tid]
    #print(tsmw)
    
    swub = {}
    wsup = {}
    for tid in sequences:
        seq = sequences[tid]
        for att in seq:
            if att in swub:
                if tid not in swub[att]:
                    swub[att].append(tid)
            else:
                swub[att] = [tid]
    for att in swub:
        in_sequences = swub[att]
        wsup[att] = (sensitivity[att]*len(in_sequences))/tsmw
        val = 0
        for tid in in_sequences:
            val = val + smw[tid]
        swub[att] = (val/tsmw)
        #print(att,swub[att],wsup[att])
        
    # print(swub)     
    WFUB = []
    WS = []
    attributes = sensitivity.keys() 
    ## attributes represent length 1 subsequences
    for att in attributes:
        if att in swub.keys() and swub[att] >= thresh :
            WFUB.append(att)
        if att in wsup.keys() and wsup[att] >= thresh :
            WS.append(att)
    
    r = 1
    PI = WFUB[:]
    for tid in sequences.keys():
        seq = sequences[tid]
        for att in seq:
            if att not in PI:
                seq.remove(att)
        if len(seq) < r+1:
            del sequences[tid]
     
    WSA = []
    WFUB.sort()
    for att in WFUB:
        sdbi = {}
        for tid in sequences:
            seq = sequences[tid]
            ind = get_loc(att, seq)
            if len(ind)>0:
                sdbi[tid] = seq[ind[0]:]
        # print(att,sdbi,r)
        WSI = finding_WS([att], sdbi, r, thresh, sensitivity, tsmw)
        if len(WSI)==0 and wsup[att] >= thresh:
            WSI = WSI + [att]
        WSA = WSA + WSI
    return WSA


# In[6]:


# att_sensitivity = dict({'A':0.1,'B':0.15,'C':0.2,'D':0.3,'E':0.45,'F':0.55,'G':0.65,'H':0.95})
# transaction_list = dict({'TID_1': ['B', 'C', 'B'], 'TID_2': ['D','E','C','H','F'], 'TID_3': ['A','C','F','D','E','F'], 'TID_4':['F','G','H'], 'TID_5':['C','D','A','C','E','F']})
# print(IWSPAN(att_sensitivity, transaction_list, 0.3))

att_sensitivity = {}
for i in range(0,70):
    att_sensitivity[chr(i+65)] = 0.9

# print (att_sensitivity['['])
# exit()

pickle_in = open("sequences_with_noise.pickle","rb")
transactions = pickle.load(pickle_in)
# transactions = generator()

patterns = {}
patterns_numbers = {}
for roleid in range(0,5):
    i=1
    m=1
    readsq = {}
    writesq = {}
    for transaction in transactions:
        # if transaction[0]==roleid:
            # print (transaction[3])
        if transaction[0]==roleid and transaction[3][0]==0:
            # print(chr(transaction[3]+97))
            # if roleid == 0:
            #     toprint = []
            #     for j in range(1,len(transaction[3])):
            #         toprint.append(chr(transaction[3][j]+97))
            #     print(toprint)
            # print('hey')
            rs = []
            for j in range(1,len(transaction[3])):
                rs.append(chr(transaction[3][j]+65))

            readsq[str(i)]=rs
            i=i+1

        elif transaction[0]==roleid and transaction[3][0]==1:
            # print(chr(transaction[3]+97))
            # toprint = []
            # for j in range(1,len(transaction[3])):
            #     toprint.append(chr(transaction[3][j]+97))
            # print(toprint)
            ws = []
            for j in range(1,len(transaction[3])):
                ws.append(chr(transaction[3][j]+65))

            writesq[str(m)]=ws
            m=m+1
            # print (ws,transaction[3])
            # exit()

    # print (readsq)
    # exit()

    patterns_read = IWSPAN(att_sensitivity, readsq, 0.15)
    patterns_write = IWSPAN(att_sensitivity, writesq, 0.15)

    patterns_read_new = []
    for pattern in patterns_read:
        pattern_new = []
        for element in pattern:
            pattern_new.append((ord(element))-65)
        patterns_read_new.append(pattern_new)

    patterns_write_new = []
    for pattern in patterns_write:
        pattern_new = []
        for element in pattern:
            pattern_new.append((ord(element))-65)
        patterns_write_new.append(pattern_new)

    patterns_numbers[roleid] = (patterns_read_new,patterns_write_new) 

    patterns_req_read = []
    for i in patterns_read:
            pat = []
            for j in i:
                    pat.append(j)
            patterns_req_read.append(pat)

    patterns[roleid] = (patterns_read,patterns_write)

    patterns_req_write = []
    for i in patterns_write:
            pat = []
            for j in i:
                    pat.append(j)
            patterns_req_write.append(pat)

    patterns[roleid] = (patterns_req_read,patterns_req_write)
    # print(patterns_numbers,patterns)
    # exit()
    # break

# print(readsq)
# print(patterns)
# for i in patterns.keys():
#     print (patterns[i][0])
#     print ()
#     print (patterns[i][1])
#     print ()
print (patterns[0][0])
print ()
print (patterns[0][1])
print ()
pickle_out = open("patterns_with_noise.pickle","wb")
pickle.dump(patterns, pickle_out,protocol=2)
pickle_out.close()
pickle_out = open("patterns_numbers_with_noise.pickle","wb")
pickle.dump(patterns_numbers, pickle_out,protocol=2)
pickle_out.close()
