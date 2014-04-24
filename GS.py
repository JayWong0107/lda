# -*- coding: UTF-8 -*-
import random
from LDABase import LDABase
import time

class GS(LDABase):
    def __init__(self,path,k=10,ite=100,alpha=0.01,beta=0.01):
        LDABase.__init__(self,path, k, ite, alpha, beta)
    
    def init(self):
        random.seed(time.time())
        self.phit = [0]*self.K
        self.thetad = [0]*self.D
        self.phi = list()
        self.theta = list()
        for i in range(self.K):
            self.phi.append([0]*self.W)
            self.theta.append([0]*self.D)
        self.topic = []
        for d in range(len(self.data)):
            doc = self.data[d]
            topic_d = dict()
            for w in sorted(doc.keys()):
                topic_d.setdefault(w,list())
                self.thetad[d] += doc[w]
                for i in range(doc[w]):
                    z = random.randint(0,self.K-1)
                    topic_d[w].append(z)
                    self.phit[z] += 1
#                     print self.phit[z]
                    self.phi[z][w] += 1
#                     print sum(self.phi[z])
                    self.theta[z][d] += 1
            self.topic.append(topic_d)

        print 'Initialize finished!'
    
    def getTopic(self,d,w):
        topic_t = self.topic[d][w]
#         print self.data[d][w]
#         print topic_t
        Wbeta = self.W*self.beta
        for z in topic_t:
            self.topic[d][w].remove(z)
            self.phit[z] -= 1
            self.phi[z][w] -= 1
            self.theta[z][d] -= 1
        
            p = [0.0]*self.K
            ptot = 0.0
            for k in range(self.K):
                p[k] = (1.0*self.phi[k][w]+self.beta)/(self.phit[k]+Wbeta)*(self.theta[k][d]+self.alpha)
                ptot += p[k]
                
            r = random.random()*ptot
            ptot = 0.0
            for topic in range(self.K):
                ptot += p[topic]
                if r < ptot:
                    break
                
            self.phit[topic] += 1    
            self.phi[topic][w] += 1
            self.theta[topic][d] += 1
            self.topic[d][w].append(topic)
#         print self.topic[d][w]
    
    def GibbsSampling(self):
        fw = open('result_gs.txt','wb')
        start = time.time()
        self.init()
        for i in range(self.ite):
            if((i+1)%10 == 0):
                perp = self.Perplexity()
                print 'Iteration:%s Perplexity:%s'%(i+1,perp)
                fw.write('Iteration:%s Perplexity:%s'%(i+1,perp))
            
            for d in range(len(self.data)):
                doc = self.data[d]
                for w in sorted(doc.keys()):
                    self.getTopic(d, w)   
                    
        end = time.time()
        print 'Gibbs sampling finished!Time Costed%s'%(end-start)
        fw.write('Gibbs sampling finished!Time Costed%s'%(end-start))
        fw.close()
        
def main():
    path = 'nips.corpus'
    lda = GS(path)
    lda.loadcorpus()
    lda.GibbsSampling()
    
main()
        
            
        
            
        
                    
        
    
    
