import numpy as np
import sys

class ERHNet:
    def __init__(self,nn,p):
        self.nn = nn
        self.p = p
        self.nodes = np.array([ ERHNode(np.random.random(nn),p,np.random.random()) for x in range(nn) ])

    def __getitem__(self,i):
        if isinstance(i,np.ndarray):
            if all([ isinstance(y,np.bool_) for y in i ]):
                return( [x.state for j,x,n in zip(i,self.nodes,range(i.size)) if j])
            elif len(i) != nn:
                raise Exception('Logical index be same size as ERHNet instance!')
            else:
                raise Exception('Index array must contain stricly booleans!')
        elif isinstance(i,tuple):
            if all([ isinstance(y,int) for y in i]):
                return( [self.nodes[x].state for x in i] )
            else:
                raise Exception('Index tuple must contain stricly integers!')
        elif isinstance(i,slice):
            return([x.state for x in self.nodes[i]])
        else:
            return self.nodes[i].state

    def __iter__(self):
        return self.nodes.__iter__()

    def __len__(self):
        return(len(nodes))

    def update(self):
        for node in self.nodes:
            node.update(self)

class ERHNode:
    def __init__(self,networkArray,nPrb,state):
        self.receives =  networkArray < nPrb 
        if state > 0.:
            self.state = 1
        else:
            self.state = 0
        self.threshold = 2

    def update(self,network):
        postSynaptic = network[self.receives]
        
        nodeInput = np.sum(postSynaptic)
        if nodeInput > self.threshold:
            self.state=1
        else:
            self.state=0

nn = 1000
p = float(sys.argv[1])

n1 = ERHNet(nn,p)
x=[]
[ x.append(n.state) for n in n1 ]
print('step ',0,'\n',x)
jj=0
while(True):
    jj+=1
    y=np.array(x)
    n1.update()
    x=[]
    [ x.append(n.state) for n in n1 ]
    z=np.array(x)
    if np.all(z-y==0):
        break
    print('step ',jj+1,'\n',x)
