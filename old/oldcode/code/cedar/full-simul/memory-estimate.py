from reverting import *
import os
import sys
import time


mem1 = 8*3  # 8 bytes/item  memory of saving 1 point in the simulation
m0 = 50000
tmax=1000*3600
for flo in ['a','g','i','l','n']:
    for no in list(range(8)):
        param, = [x for x in paramslist if x['trial'] == flo and x['l']==llist[no]]
        nu,la0,la1,si0,si1,mu0,mu1,ga = itemgetter('nu','la0','la1','si0','si1','mu0','mu1','ga')(param)
        nbar = (nu+la0)/(ga+si0-mu0) # mean expected from ancey2008 lambda/(alpha-mu).. lambda = nu + la0, alpha = ga + si0
        rt = np.array([nu,Lam(nbar,m0,param)+ nbar*Mu(nbar,m0,param),nbar*Sig(nbar,m0,param),nbar*ga]).sum()
        nt = rt*tmax # total number of transitions expected
        totmem = round(nt*mem1/1e9,2) # total memory required if all transitions sampled in Gb
        l = round(llist[no],2)
        print('flow {} and l = {} -- memory required is {} Gb for {}hr simulation.'.format(flo, no, totmem, int(tmax/3600)))
