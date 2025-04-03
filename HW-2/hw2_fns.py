import numpy as np
from numpy.random import choice as choose


def hmm_gen(S, T, a, e):
    '''
    S = observable states. e.g, {Head, Tail}
    T = hidden states. e.g, {0(init/term), 1(Fair), 2(Biased)}
    a = transition probabilites for hidden states
    e = emission probabilities of hidden states
    OUTPUT:
    pi = hidden state chain
    x = observable state chain
    '''
    T =  np.arange(T)
    pi = []
    x = []
    pi.append(choose(T[1:], p=a[0, 1: len(T)]))
    x.append(choose(S, p=e[pi[0]-1, :]))
    while pi[-1] != 0:
        pi.append(choose(T, p=a[pi[-1], :]))
        x.append(choose(S, p=e[pi[-1]-1, :]))
    pi = [int(p) for p in pi]
    x = [str(q) for q in x]
    return pi, x

    
def Viterbi(x, S, T, a, e):#x is obs, h is hid
    obsstates = {S[0]: 0, S[1] : 1}
    v = np.zeros((len(x), T-1))
    v[:, 0] = 0
    v[0, :] = a[0, 1:]
    path = []
    for xi in range(1,len(x)):
        for hi in range(T-1):
            k = []
            for hi2 in range(T-1):
                p_trans = a[hi, hi2]
                p_emssn = e[hi-1, obsstates[x[xi]]]
                k.append(v[xi-1, hi2]*p_trans*p_emssn)
            v[xi, hi] = np.max(k)
        path.append(np.argmax(v[xi, :]))
    return [int(i) for i in path]

def match(pi1, pi2):
    score = 0
    for i in range(len(pi1)):
        if pi1[i] == pi2[i]:
            score+=1
    return score/len(pi1)


def Forward(x, S, T, a, e):
    T = np.arange(T)
    obsstates = {S[0]: 0, S[1] : 1}
    alpha = np.zeros((len(x), len(T)-1))
    alpha[:, 0] = 0
    alpha[0, :] = a[0, 1:]
    path = []
    for xi in range(1,len(x)):
        for hi in range(len(T)-1):
            k = []
            for hi2 in range(len(T)-1):
                p_trans = a[hi, hi2]
                p_emssn = e[hi-1, obsstates[x[xi]]]
                k.append(alpha[xi-1, hi2]*p_trans*p_emssn)
            alpha[xi, hi] = np.sum(k)
    likelihood =  np.sum(alpha[-1, :])
    return likelihood

# def Backward(x, S, T, a, e):
#     T = np.arange(T)
#     obsstates = {S[0]: 0, S[1] : 1}
#     alpha = np.zeros((len(x), len(T)-1))
#     alpha[:, 0] = 0
#     alpha[0, :] = a[0, 1:]
#     path = []
#     for xi in range(1,len(x)):
#         for hi in range(len(T)-1):
#             k = []
#             for hi2 in range(len(T)-1):
#                 p_trans = a[hi, hi2]
#                 p_emssn = e[hi-1, obsstates[x[xi]]]
#                 k.append(alpha[xi-1, hi2]*p_trans*p_emssn)
#             alpha[xi, hi] = np.sum(k)
#     likelihood =  np.sum(alpha[-1, :])
#     return likelihood

