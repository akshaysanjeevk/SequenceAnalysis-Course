import numpy as np

def hmm_gen(N, S, T, a, e):
    '''
    N= length of hidden markov sequence desired to be generated,
    S = observable states. e.g, {Head, Tail}
    T = hidden states. e.g, {Fair, Biased}
    a = transition probabilites for hidden states
    e = emission probabilities of hidden states
    '''
    
    hdn_seq = np.zeros(N, dtype=int)
    obs_seq = np.zeros(N, dtype=str)
    hdn_seq[0] = np.random.choice(T[1:], p=a[0, 1: len(T)])
    obs_seq[0] = np.random.choice(S, p=e[hdn_seq[0]-1, :])

    for i in range(1, N):
        hdn_seq[i] = np.random.choice(T[1:], p=a[])


    


S = ['H', 'T']
T = np.arange(3)

a = np.array([[  0,  .5,  .5], #tranisiton proba
              [.01, .94, .05],
              [.01, .05, .94]])
e = np.array([[.5, .5],
              [.8, .2]])

hmm_gen(2, S, T, a, e)