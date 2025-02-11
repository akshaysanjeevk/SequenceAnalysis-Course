from Bio import SeqIO
import numpy as np
import math

def totalcount(x, pseudocount):
    alpha = ['A', 'T', 'G', 'C']
    counts = np.array([np.sum(x==nt) for nt in alpha])
    finalcount = (counts + pseudocount)/(len(x) + 4*pseudocount)
    return finalcount

def profile(DNA, k, pos, log_odd=True):
    N = len(DNA)# or pos0
    x = np.empty((N, k), dtype=str) #matrix with k-mers
    W = np.empty((4, k)) #position weight matrix
    for i in range(N):
        x[i, :] = list(DNA[i][pos[i]:pos[i]+k])
    for j in range(k):
        W[:,j] = totalcount(x[:,j], pseudocount=1)
    if log_odd==True: # log-odds matrix
        W2 = np.log(W*4)/np.log(4)
    else: 
        W2 = W
    return W2

def llr(profile, s):
    ref = {
        'A':0,
        'T':1,
        'G':2,
        'C':3
    }
    llratio = 0
    for i in range(len(s)):
        llratio += profile[ref[s[i]], i]
    return llratio

def motifpos(profile, DNA):
    N = len(DNA)
    k = profile.shape[1]
    pos = np.empty(N, dtype=int)
    for i in range(N):
        maxllr = -math.inf
        for j in range(len(DNA[i])-k+1):
            llrval = llr(profile, DNA[i][j:j+k])
            if llrval > maxllr:
                maxllr = llrval
                pos[i] = j
    return pos  

def GreedySearch(DNA, k):
    N = len(DNA)
    pos = np.array([np.random.randint(0, len(DNA[i]) - k) for i in range(N)])
    while True:
        old_pos = pos.copy()
        pwm = profile(DNA, k, pos)
        pos = motifpos(pwm, DNA)
        if np.array_equal(old_pos, pos):
            break
    return pos

def main(): 
    DNA = []
    for record in SeqIO.parse("data/motif.fa", "fasta"):
        DNA.append(str(record.seq))
    k = 8
    pos = GreedySearch(DNA, k)
    print(pos)

