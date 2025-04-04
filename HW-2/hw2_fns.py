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
    v[0, :] = a[0, 1:]
    path = []
    for xi in range(1,len(x)):
        for hi in range(T-1):
            v[xi, hi] = np.max([
                v[xi-1, i] * a[i, hi] * e[hi, obsstates[x[xi]]]
                for i in range(T-1)
            ])
        path.append(np.argmax(v[xi, :]))
    return [int(i) for i in path]

def match(pi1, pi2):
    score = 0
    for i in range(len(pi1)):
        if pi1[i] == pi2[i]:
            score+=1
    return score/len(pi1)

def Forward(x, S, T, a, e):
    obs_index = {obs: i for i, obs in enumerate(S)}
    alpha = np.zeros((len(x), T-1))
    for i in range(T-1):
        alpha[0, i] = a[0, i+1] * e[i, obs_index[x[0]]]
    for xi in range(1, len(x)):
        obs_idx = obs_index[x[xi]]
        for hi in range(T-1):
            alpha[xi, hi] = np.sum(
                alpha[xi-1, :] * a[1:, hi+1] * e[hi, obs_idx])
    return np.sum(alpha[-1, :])

def Backward(x, S, T, a, e):
    obs_index = {s: i for i, s in enumerate(S)}
    N = T - 1
    beta = np.zeros((len(x), T))
    beta[-1, 1:] = 1  
    for xi in reversed(range(len(x)-1)):
        for hi in range(1, T):
            beta[xi, hi] = np.sum(
                beta[xi+1, 1:] * a[hi, 1:] * e[:, obs_index[x[xi+1]]])
    likelihood = np.sum(a[0, 1:] * e[:, obs_index[x[0]]] * beta[0, 1:])
    return likelihood

