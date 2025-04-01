import numpy as np

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
    pi.append(np.random.choice(T[1:], p=a[0, 1: len(T)]))
    x.append(np.random.choice(S, p=e[pi[0]-1, :]))
    while pi[-1] != 0:
        pi.append(np.random.choice(T, p=a[pi[-1], :]))
        x.append(np.random.choice(S, p=e[pi[-1]-1, :]))
        
    return pi, x

