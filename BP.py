# -*- coding: UTF-8 -*-
from LDABase import LDABase
import random
import time

class BP(LDABase):
    
    def __init__(self,path,k=10,ite=100,alpha=0.01,beta=0.01):
        LDABase.__init__(self, path, k, ite, alpha, beta)
        
    def init(self):
        random.seed(time.time())
        self.phit = [0.0]*self.K
        self.thetad = [0.0]*self.D
        self.phi = list()
        self.theta = list()
#         self.phi = [[0.0]*self.W]*self.K
#         self.theta = [[0.0]*self.D]*self.K
        for i in range(self.K):
            self.phi.append([0]*self.W)
            self.theta.append([0]*self.D)
        self.mu = []
        
        for d in range(len(self.data)):
            doc = self.data[d]
            mu_d = dict()
            for w in sorted(doc.keys()):
                mu_d.setdefault(w,list())
                mu_w = [0.0]*self.K
                z = random.randint(0,self.K-1)
                mu_w[z] = 1.0
                mu_d[w] = mu_w
                self.phit[z] += doc[w]
                self.phi[z][w] += doc[w]
                self.thetad[d] += doc[w]
                self.theta[z][d] += doc[w]
            self.mu.append(mu_d)
        print 'Initialize finished!'
        
    def BeliefPropagation(self):
        fw = open('result_bp.txt','wb')
        self.init()
        Wbeta = self.W*self.beta

        for i in range(self.ite):
#             print i
            if((i+1)%10 == 0):
                perp = self.Perplexity()
                print 'Iteration:%s Perplexity:%s\n'%(i+1,perp)
                fw.write('Iteration:%s Perplexity:%s\n'%(i+1,perp))
            for d in range(len(self.data)):
                doc = self.data[d]
                mu_d = dict()
                for w in sorted(doc.keys()):
                    mu_d.setdefault(w,list())
                    mu_w = [0.0]*self.K
                    x = doc[w]
                    mu_tot = 0.0
                    for k in range(self.K):
                        mu_w[k] = (1.0*(self.phi[k][w]-x*self.mu[d][w][k]+self.beta)
                                    /(self.phit[k]-x*self.mu[d][w][k]+Wbeta)*(self.theta[k][d]-x*self.mu[d][w][k]+self.alpha))
                        mu_tot += mu_w[k]
                    for k in range(self.K):
                        mu_w[k] /= mu_tot
                    mu_d[w] = mu_w
                self.mu[d] = mu_d
                
            self.phit = [0.0]*self.K
#             self.phi = [[0.0]*self.W]*self.K
#             self.theta = [[0.0]*self.D]*self.K
            self.phi = list()
            self.theta = list()
            for i in range(self.K):
                self.phi.append([0]*self.W)
                self.theta.append([0]*self.D)
            
            for d in range(len(self.data)):
                doc = self.data[d]
                for w in sorted(doc.keys()):
                    for k in range(self.K):
                        self.phit[k] += doc[w]*self.mu[d][w][k]
                        self.phi[k][w] += doc[w]*self.mu[d][w][k]
                        self.theta[k][d] += doc[w]*self.mu[d][w][k]
        fw.close()
        print 'Belief Propagation Finished!\n'
                
                
def main():
    path = 'nips.corpus'
    bp = BP(path)
    bp.loadcorpus()
    bp.BeliefPropagation()

main()
