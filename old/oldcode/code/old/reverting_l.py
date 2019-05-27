import matplotlib.pyplot as plt 
import numpy as np 
from operator import itemgetter # unpack vals from dicts into variables 
import copy
## parameters 

# parameters from ancey2008 table #3
aparams_a = {'trial':'a','nu':5.45, 'la0': 6.59, 'si0': 4.67, 'ga':0.77, 'mu0':3.74}
aparams_b = {'trial':'b','nu':7.76, 'la0':11.21, 'si0':5.28, 'ga':0.79 , 'mu0':4.14}
aparams_c = {'trial':'c','nu':9.20, 'la0':15.14, 'si0':5.05, 'ga':0.75 , 'mu0':3.81}
aparams_d = {'trial':'d','nu':10.99, 'la0': 21.40, 'si0': 4.91, 'ga':0.74, 'mu0':3.47} 
aparams_e = {'trial':'e','nu':5.72, 'la0':1.53, 'si0': 5.13, 'ga': 0.60, 'mu0':4.96}
aparams_f = {'trial':'f','nu':6.85, 'la0':7.80, 'si0':4.86 , 'ga': 0.69, 'mu0':4.07}
aparams_g = {'trial':'g','nu':7.74, 'la0':8.42, 'si0':4.95, 'ga': 0.56, 'mu0':4.34}
aparams_h = {'trial':'h','nu':9.41, 'la0':11.24, 'si0':4.74, 'ga':0.69, 'mu0':3.91}
aparams_i = {'trial':'i','nu':15.56, 'la0':22.07, 'si0':4.52, 'ga': 0.68, 'mu0':3.56}
aparams_j = {'trial':'j','nu':20.57, 'la0':24.78, 'si0':4.39, 'ga': 0.60, 'mu0':3.67}
aparams_k = {'trial':'k','nu':9.52, 'la0':10.96, 'si0':4.84, 'ga': 0.43, 'mu0':4.34}
aparams_l = {'trial':'l','nu':15.52, 'la0':14.64, 'si0':4.77, 'ga': 0.48, 'mu0':4.32}
aparams_m = {'trial':'m','nu':19.86, 'la0':13.62, 'si0':4.51, 'ga': 0.52, 'mu0':4.16}
aparams_n = {'trial':'n','nu':15.45, 'la0':24.49, 'si0':4.21, 'ga':0.36, 'mu0':3.64}
aparamslist = [aparams_a, aparams_b, aparams_c, aparams_d, aparams_e, aparams_f, aparams_g, aparams_h, aparams_i, aparams_j, aparams_k, aparams_l, aparams_m, aparams_n]

# dimensions / initial values
a = 0.3 # particle radius 
dx = 22.5 # control volume cell size 
phi = 0.6 # packing fraction 
n0 = 21 #initial number of moving particles 
m0 = 5003 # initial number of stationary particles 
z1 = np.pi*a**2/(phi*dx) # relevant length scale of bed elevations
#b = 100 # magnitude of elevation fluctuations 

#blist = [50,250,500,1000,5000,10000,20000,50000,100000] # this should really be replaced by l values now that you figured it out 
#llist = [np.sqrt(x)*z1/2 for x in blist]
llist = [x*z1 for x in range(5,275,25)] # 11 of these l values
# x is # of particles that it can fluctuate while $z1$ is elevation per particle. 

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
del aparamslist0, aparams_a, aparams_b, aparams_c, aparams_d, aparams_e, aparams_f, aparams_g, aparams_h, aparams_i, aparams_j, aparams_k, aparams_l, aparams_m, aparams_n, trial
## now aparamslist has dicts of all experimental conditions. transport parameters + the bed parameter l

# in the interest of iterating this script over all conditions simultaneously, I'll write this up so I can call two indices x and y
# from the command line which will select the desired trial + l combination from paramslist and iterate only that one. 
# then I'll write a bash script with a double for loop to sbatch all conditions simultaneously 

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
    
def simulate(param, flag='C', tmax = 200000):
    t = 0
    n = n0
    m = m0 
    S = []
    while t<tmax:
        n,m,t = react(n,m,t,param)
        S.append(np.copy(np.array([n,m,t])))
    S = np.array(S)
    lval = round(param['l'],2)
    fname = './simulations/{}-{}-{}-'.format(param['trial'],lval, tmax) + flag
    paramfname = fname+'-params'
    np.save(fname, S)
    np.save(paramfname, param)
    del S
