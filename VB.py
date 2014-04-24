import time
from LDABase import LDABase

class VB(LDABase):
    
    def __init__(self,path,k=10,ite=100,alpha=0.01,beta=0.01):
        LDABase.__init__(self,path, k, ite, alpha, beta)
    
    def VB(self):
        pass
    

        