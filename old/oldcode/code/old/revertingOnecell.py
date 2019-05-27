import matplotlib.pyplot as plt 
import numpy as np 
from operator import itemgetter # unpack vals from dicts into variables 
import copy
## parameters 

# parameters from ancey2008 table #3
aparams_a = {'trial':'a','nu':5.45, 'la0': 6.59, 'si0': 4.67, 'ga':0.77, 'mu0':3.74}
aparams_d = {'trial':'d','nu':10.99, 'la0': 21.40, 'si0': 4.91, 'ga':0.74, 'mu0':3.47} 
aparams_h = {'trial':'h','nu':9.41, 'la0':11.24, 'si0':4.74, 'ga':0.69, 'mu0':3.91}
aparams_k = {'trial':'k','nu':9.52, 'la0':10.96, 'si0':4.84, 'ga': 0.43, 'mu0':4.34}
aparams_n = {'trial':'n','nu':15.45, 'la0':24.49, 'si0':4.21, 'ga':0.36, 'mu0':3.64}
aparamslist = [aparams_a, aparams_d, aparams_h, aparams_k, aparams_n]

# dimensions / initial values
a = 0.3 # particle radius 
dx = 22.5 # control volume cell size 
phi = 0.6 # packing fraction 
n0 = 21 #initial number of moving particles 
m0 = 5003 # initial number of stationary particles 
z1 = np.pi*a**2/(phi*dx) # relevant length scale of bed elevations
#b = 100 # magnitude of elevation fluctuations 

blist = [50,250,500,1000,5000,10000,20000,50000,100000] # this should really be replaced by l values now that you figured it out 


paramslist = []
aparamslist0 = copy.deepcopy(aparamslist)

for l in aparamslist0:
    trial = copy.deepcopy(l['trial'])
    for i,b in enumerate(blist): 
        l['trial']=trial+'_'+str(i+1)
        l['la1'] = l['la0']/(b*z1)
        l['si1'] = l['si0']/(b*z1)
        l['mu1'] = l['mu0']/(b*z1)
        l['b'] = b
        paramslist.append(copy.deepcopy(l))
del aparamslist, aparams_a, aparams_d, aparams_h, aparams_k, aparams_n, blist,trial

## rate functions
def z(m):
    """ the elevation function based on porosity phi and cell size dx """
    return z1*(m-m0)

def Lam(n,m,params):
    """ the individual entrainment rate given n,m particles in motion and at rest respectively"""
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)
    out = la0 + la1* z(m)
    if out < 0:
        raise ValueError('entrainment rate is negative. adjust b.')
    return out

def Mu(n,m,params): 
    """ collective entrainment rate """ 
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)  
    out = (mu0 + mu1 * z(m))
    if out < 0:
        raise ValueError('collective entrainment rate is negative. adjust b.')    
    return out 

def Sig(n,m,params):
    """ deposition rate""" 
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)
    out =  (si0-si1*z(m))
    if out < 0:
        raise ValueError('deposition rate is negative. adjust b.')    
    return out 

## simulate 
def react(n,m,t,params):
    """ do a single iteration of the gillespie algorithm. 
    step n,m,t to n+dn,m+dm,t+dt with the increments determined
    by gillespie. 
    return the stepped values.""" 
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)
    # migrate in, entrain, deposit, migrate out
    # generate propensities 
    A = np.array([nu,Lam(n,m,params)+ n*Mu(n,m,params),n*Sig(n,m,params),n*ga])
    a0 = A.sum() # sum of all propensities 
    r1,r2 = np.random.uniform(size=2) # generate unit randoms 
    tau = 1/a0*np.log(1/r1) # timestep 
    t+=tau #step t
    i = np.argmax(np.cumsum(A/a0)>r2) # choose the reaction 
    if i==0: # do the reaction
        n+=1
    elif i==1:
        n+=1
        m-=1
    elif i==2:
        n-=1
        m+=1
    elif i==3:
        n-=1
    return n,m,t # return the stepped values

## visualize 
def view(S,title=None):
    """ show the particle activity and bed elevation pdfs""" 
    n,m,t = np.array(S).T
    M,Cm = np.unique(m,return_counts=True)
    N,Cn = np.unique(n,return_counts=True)
    plt.subplot(1, 2, 1)
    xarg = z(M)#/z1
    xmin = xarg.min() - (xarg.max()-xarg.min())*0.1
    xmax = xarg.max() + (xarg.max()-xarg.min())*0.1
    plt.scatter(xarg,Cm/Cm.sum())
    plt.xlabel('bed elevation (cm)')
    plt.xlim(xmin,xmax)
    plt.ylabel('pdf')
    plt.subplot(1, 2, 2)
    plt.scatter(N,Cn/Cn.sum(),color='purple')
    plt.xlim(N.min()-0.1*(N.max()-N.min()),N.max()+0.1*(N.max()-N.min()))
    #plt.xlim(-5,35)
    plt.xlabel('particle activity')
    if title:
        plt.title(title)
    plt.show()
    del n,m,t,M,Cm,N,Cn