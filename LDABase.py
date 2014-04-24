# -*- coding: UTF-8 -*-
import math

class LDABase:
    def __init__(self,path,k=20,ite=100,alpha=0.1,beta=0.1):
        self.path = path
        self.K = k
        self.ite = ite
        self.alpha = alpha
        self.beta =beta
        self.phi = None
        self.theta = None
#         self.loadcorpus()
    
    def readData(self,path=None):
        path = path or self.path
        fr = open(path,'rb')
        l1 =fr.readline().rstrip()
        [D,W,NNZ]=l1.split(' ')
        self.D = int(D)
        self.W = int(W)
        self.NNZ = int(NNZ)
        print D,W,NNZ
        self.data = []
        lines = fr.readlines()
        self.wtot = 0
        for line in lines:
            d = dict()
            t = line.rstrip().split(' ')
            for i in range(0,len(t),2):
                d.setdefault(int(t[i])-1,0)
                x = int(t[i+1])
                self.wtot += x
                d[int(t[i])-1] += x
            self.data.append(d)
        print 'total words:%s'%self.wtot
        return self.data
    
    def Perplexity(self):
        perp = 0.0
        for d in range(len(self.data)):
            doc = self.data[d]
            for w in sorted(doc.keys()):
                perptot = 0.0
                for k in range(self.K):
                    perptot += (1.0*(self.phi[k][w]+self.beta)/(self.phit[k]+self.W*self.beta)*
                                (self.theta[k][d]+self.alpha)/(self.thetad[d]+self.K*self.alpha))
                perp -= math.log(perptot)*doc[w]
        return math.exp(1.0*perp/self.wtot)
             
            
            
    def loadcorpus(self,path=None):
        path = path or self.path
        fr = open(path,'rb')
        self.data = []
        self.wtot = 0
        words = set()
        lines = fr.readlines()
        for line in lines:
            d = dict()
            line_t = line.rstrip().split(' ')
            for e in line_t[1:]:
                t = e.split(':')
                self.wtot += int(t[1])
                words.add(int(t[0]))
                d.setdefault(int(t[0]),int(t[1]))
            self.data.append(d)
        self.D = len(lines)
        self.W = len(words)
#         print self.D,self.W,self.wtot
        
        fr.close()
        
        
    def getPhi(self):
        pass
    
    def getTheta(self):
        pass

def test():
    path = 'nips.corpus'
    t = LDABase(path)
    t.loadcorpus()

    
        

    