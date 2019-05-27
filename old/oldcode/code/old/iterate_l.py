from reverting_l import *
import os 
import sys 
import time 

trial, no = sys.argv[1],sys.argv[2]
no = int(no)
no-=1

param = [x for x in paramslist if x['trial']==trial and x['l']==llist[no]][0]
print('trial ' + param['trial'] + ' / ', 'l = '+ str(round(param['l'],2)) + '...', 'computation beginning')

# it takes about 150s per 10000s. So run it for 450*t_max/10000 seconds 
# for 200000s that's 2.5hrs which is 02:30:00 

T0 = time.time()
x = simulate(param, flag='C',tmax=10000)
print('computation complete in {} seconds'.format(round(time.time()-T0,2)))
del x
