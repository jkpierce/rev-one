#from reverting_l import *
import matplotlib.pyplot as plt
import os
import numpy as np
import sys
file = sys.argv[1]
z = sys.argv[2]

z1 = 0.020943951023931956

# RETURN TIME DIST
# first load trial $h$ / $l=1.68$ in:
bury_S = np.load('../simulations/'+file)

# unpack it and lose the n values
nb,mb,tb = bury_S.T
del nb

# resample the data every 5s
increments = np.arange(0,int(tb.max()/5.0)*5.0,5)
indlist = tb.searchsorted(increments) # the set of indices where t is about a multiple of 5 
mb = mb[np.array(indlist)]
tb = tb[np.array(indlist)]

mstar = round(mb.mean())+float(z)/z1 # set the elevation in m units
mstar = int(mstar)

# np.roll(x,-1) brings the future element to the current position
# np.roll(x,1) brings the past element to the current position
departures, = np.where( (np.roll(mb,1) <= mstar) & (mb > mstar) )#& (np.roll(mb,-1) > mstar) ) # indices of departure from elevation mstar
returns, = np.where( (np.roll(mb,1) > mstar) & (mb <= mstar)  )#& (np.roll(mb,-1) <= mstar) )  # indices of return to elevation mstar
# must start from a departure
while returns.min()<departures.min():
    returns = returns[1:]
# must end at a return
while returns.max()<departures.max():
    departures = departures[:-1]
returntimes = tb[returns] - tb[departures] # compute the return times
trial, l, = file.split('-')[:2]
#print(z)
savestr = './trial_{}_l_{}_depth_{}'.format(trial,l,z)
np.save(savestr,returntimes)
