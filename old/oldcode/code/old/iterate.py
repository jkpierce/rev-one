from revertingOnecell import *
import os 

if not os.path.isdir('./simulations'):
    os.mkdir('./simulations')
    
i=0
for p in paramslist:
    print('trial %03d'%i)
    x = simulate(p,flag='_100000_A',tmax=100000)
    del x
    i+=1