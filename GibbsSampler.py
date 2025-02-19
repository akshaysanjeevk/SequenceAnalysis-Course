import  numpy as np
import math

def totalcount(x, pseudocount):
    x=list(x)
    counts = np.array([
        x.count('A'),
        x.count('T'),
        x.count('G'),
        x.count('C')
        ])
    finalcount = (counts + pseudocount)/(len(x) + 4*pseudocount)
    return finalcount

def profile(DNA, k, pos):
    N = len(DNA)# or pos0
    x = np.empty((N, k), dtype=str) #matrix with k-mers
    W = np.empty((4, k), dtype=float) #position weight matrix
    for i in range(N-1):
        x[i, :] = list(DNA[i][pos[i]:pos[i]+k])
    for j in range(k):
        W[:,j] = totalcount(x[:,j], pseudocount=1)
    return W

def likelihoodr(profile, s):
    ref = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
    llratio = 0.0  # Log-sum instead of multiplication
    for i in range(len(s)):
        llratio += profile[ref[s[i]],i] # Log transformation
    return np.exp(llratio)

# def score(pos): 
