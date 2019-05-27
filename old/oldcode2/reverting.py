import matplotlib.pyplot as plt 
import numpy as np 
from operator import itemgetter # unpack vals from dicts into variables 
import copy

## parameters 

# parameters from ancey2008 table #3
aparams_a = {'trial':'a','nu':5.45, 'la0': 6.59, 'si0': 4.67, 'ga':0.77, 'mu0':3.74}
aparams_g = {'trial':'g','nu':7.74, 'la0':8.42, 'si0':4.95, 'ga': 0.56, 'mu0':4.34}
aparams_i = {'trial':'i','nu':15.56, 'la0':22.07, 'si0':4.52, 'ga': 0.68, 'mu0':3.56}
aparams_l = {'trial':'l','nu':15.52, 'la0':14.64, 'si0':4.77, 'ga': 0.48, 'mu0':4.32}
aparams_n = {'trial':'n','nu':15.45, 'la0':24.49, 'si0':4.21, 'ga':0.36, 'mu0':3.64}
aparamslist = [aparams_a, aparams_g, aparams_i, aparams_l, aparams_n]

# dimensions / initial values
a = 0.3 # particle radius 
dx = 22.5 # control volume cell size 
phi = 0.6 # packing fraction 
n0 = 21 #initial number of moving particles 
m0 = 50000 # initial number of stationary particles 
z1 = np.pi*a**2/(phi*dx) # relevant length scale of bed elevations

llist = [a, 2*a, 3*a, 4*a, 5*a, 6*a, 7*a, 8*a, 9*a, 10*a] # active layer is multiple of radius 
paramslist = []
aparamslist0 = copy.deepcopy(aparamslist)

for l in aparamslist0:
    trial = copy.deepcopy(l['trial'])
    for i,ll in enumerate(llist): 
        l['trial']=trial
        l['la1'] = l['la0']/(4*ll**2/z1) # this should be the proper scaling with l to make var(z) = l**2 or var(m) = (l/z1)**2. 
        l['si1'] = l['si0']/(4*ll**2/z1)
        l['mu1'] = l['mu0']/(4*ll**2/z1)
        l['l'] = ll
        paramslist.append(copy.deepcopy(l))
del aparamslist0, aparams_a, aparams_g, aparams_i, aparams_l, aparams_n, trial
## now aparamslist has dicts of all experimental conditions. transport parameters + the differential erosion/deposition parameter l

## rate functions
def z(m):
    """ the elevation function based on porosity phi and cell size dx """
    return z1*(m-m0)

def Lam(n,m,params):
    """ the individual entrainment rate given n,m particles in motion and at rest respectively"""
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)
    out = la0 + la1 * z(m)
    if out < 0:
        raise ValueError('entrainment rate is negative. adjust l.')
    return out

def Mu(n,m,params): 
    """ collective entrainment rate """ 
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)  
    out = mu0 + mu1 * z(m)
    if out < 0:
        raise ValueError('collective entrainment rate is negative. adjust l.')    
    return out 

def Sig(n,m,params):
    """ deposition rate""" 
    nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(params)
    out =  si0-si1*z(m)
    if out < 0:
        raise ValueError('deposition rate is negative. adjust l.')    
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
    t=t+tau #step t
    i = np.argmax(np.cumsum(A/a0)>r2) # choose the reaction 
    if i==0: # migration in 
        n=n+1
    elif i==1: # entrainment 
        n=n+1
        m=m-1
    elif i==2: # deposition 
        n=n-1
        m=m+1
    elif i==3: # migration out
        n=n-1
    return n,m,t # return the stepped values
    
def simulate(param, tmax, filename):
    """dt is the sampling interval"""
    t = 0
    n = n0
    m = m0 
    S = []
    while t<tmax:
        n,m,t = react(n,m,t,param)
        S.append([n,m,t]) # perform the reaction
    S = np.array(S)
    np.save(filename, S.T)
    print('simulation complete.')


