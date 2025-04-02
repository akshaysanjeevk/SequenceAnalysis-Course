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
    T = np.arange(T)
    obstates = {'H' : 0, 'T' : 1}
    v = np.zeros((len(x), len(T)))
    v[:, 0] = 0
    # v[0, :] = a[0, :]
    path = []
    for xi in range(len(x)):
        for hi in range(1, len(T)-1):
            p_trans = a[hi-1, hi]
            p_emssn = e[hi, obstates[x[xi]]]
            v[xi, hi] = v[xi-1, hi-1]*p_trans*p_emssn
        path.append((np.max(v[xi, :]), np.argmax(v[xi, :])))
    print(v)   
    path = [(float(a), int(b)) for a, b in path]
    return path


