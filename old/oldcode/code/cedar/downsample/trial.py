from reverting import *
import os
import sys
import time


# input these as arguments
# the first argument should be a flow condition like 'a', 'b', 'c', 'd'
# the second argument should be an integer 0,1,2,...7
# first characterizes ancey2008 flow condition
# second characterizes the value of l
# the first arguments should be a, g, i , l , n you decided.
# there are 8 flow conditions so the second arg should max at 7


# get the arguments
flo, no = sys.argv[1], sys.argv[2]
no=int(no) # make the number argument an integer
if flo not in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n']:
    raise ValueError('flow condition invalid (first argument)')
if no not in list(range(8)):
    raise ValueError('l value invalid (second argument)')

param, = [x for x in paramslist if x['trial'] == flo and x['l']==llist[no]]
print('init simulation with flow condition ~{}~ and l={}'.format(flo,str(round(llist[no],2))))


# now run the simulation
#tmax = 5*3600 # local
tmax = 500*3600 # cedar ... 500 hr simulation time
# should take approx 2 hr ?

# print the starting tim
tm = time.localtime()
hour = tm.tm_hour
minu = tm.tm_min
print('simulation started at {}:{}'.format(hour,minu))
del tm,hour,minu

S, si = simulate(param,tmax) #S = (n,m,t); si = sampling interval

# save the simulation
save_path = './' # testing
#save_path = '/home/kpierce/Desktop/reverting-onecell/code/cedar/' # local
#save_path = '/home/kpierce/scratch/reverting-onecell/' # cedar
lstr = str(round(llist[no],2))
timestr = str(round(tmax/3600))
save_name = 'flow_{}-l_{}-time_{}hr-si_{}'.format(flo, lstr, timestr,si)
np.save(save_path+save_name, S)


# print the ending time
tm = time.localtime()
hour = tm.tm_hour
minu = tm.tm_min
print('simulation finished at {}:{}'.format(hour,minu))
del tm,hour,minu
