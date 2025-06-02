class Node:
    def __init__(self,label,height=0.0):
        self.label = label
        self.children = []
        self.height = height
        
def split_string_by_bracket(s):
    splitlist = []
    substr = ""
    nleft = 0
    nright = 0
    for c in s:
        if c == "(":
            nleft += 1
        elif c == ")":
            nright += 1
        if c=="," and nleft==nright:
            splitlist += [substr]
            substr = ""
        else:
            substr += c
    splitlist += [substr]
    return splitlist
    
def newick_to_tree(s):
    if s[-1] == ";":    # full tree
        if s[-2]==")":  # no root height
            height = 0.0
        else:
            height = float(s.split(":")[-1][0:-1]) # the thing after ":" and before ;
    else:
        height = float(s.split(":")[-1]) # no ; for internal nodes
    tree = Node("",height)
    if s[0]=="(": # find closing brace
        last = len(s)-1
        try:
            while s[last]!= ")":
                last -= 1
        except:
            print(s)
            raise ValueError
        children = split_string_by_bracket(s[1:last])
        tree.children = [newick_to_tree(c) for c in children]
    else: # leaf
        tree.label = s.split(":")[0]
    return tree
        
def tree_to_newick_nosc(t):
    if t.children==[]:
        return t.label+":"+str(t.height)
    else:
        return "("+",".join([tree_to_newick(x) for x in t.children])\
                    +"):"+str(t.height)
                    
def tree_to_newick(t, depth=0):
    if depth==0:
        endtoken = ";"
    else:
        endtoken = ""
    if t.children==[]:
        return t.label+":"+str(t.height)+endtoken
    else:
        return "("+",".join([tree_to_newick(x,depth+1) for x in t.children])\
                    +"):"+str(t.height)+endtoken
def get_leaves(node):
    if node.children == []:
        return [node.label]
    else:
        return sum([get_leaves(c) for c in node.children],[])
    
## UPGMA implimentation

def dist_nodes(node1, node2, dist_matrix, label_dict):
    leaves1 = get_leaves(node1) 
    leaves2 = get_leaves(node2)
    d = 0.0
    for l1 in leaves1:
        for l2 in leaves2:
            d += dist_matrix[label_dict[l1],label_dict[l2]]
    return d/len(leaves1)/len(leaves2)
def total_height(node): # get the distance from the node to its first leaf, assume equal height to all leaves
    if node.children==[]:
        return 0.0
    else:
        return node.children[0].height + total_height(node.children[0])
    
def join_nodes(node1, node2, height):
    parent = Node("",0.0) 
    node1.height = height/2 - total_height(node1)
    node2.height = height/2 - total_height(node2)# height is uniformly distributed
    parent.children=[node1,node2]
    return parent

def closest_nodes(clusters,dist_matrix,label_dict):
    mindist = 1e12 #large number
    minnodes = ()
    for n1 in range(len(clusters)-1):
        for n2 in range(n1+1, len(clusters)):
            node1 = clusters[n1]
            node2 = clusters[n2]
            dist = dist_nodes(node1, node2, dist_matrix, label_dict)
            if dist < mindist:
                mindist = dist
                minnodes = (node1, node2)
    return minnodes[0], minnodes[1], mindist

def upgma(dist_matrix,label_dict):
    # initialize every leaf as its own cluster, ie node
    clusters = []
    for l in label_dict.keys():
        clusters += [Node(l,0.0)]
    while len(clusters) > 1:
        node1, node2, height = closest_nodes(clusters,dist_matrix,label_dict)
        clusters.remove(node1)
        clusters.remove(node2)
        node3 = join_nodes(node1, node2, height)
        clusters.append(node3)
    return clusters[0]
