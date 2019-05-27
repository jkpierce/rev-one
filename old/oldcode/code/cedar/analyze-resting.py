import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter # unpack vals from dicts into variables
import copy
from reverting import *
import analysis_tools as at
import os

# get all filenames
#directory = '/home/kpierce/scratch/reverting-onecell' # cedar
directory = '/home/kpierce/Desktop/reverting-onecell/simulations' # local
files = []
for f in os.listdir(directory):
    if '.npy' in f:
        files.append(f)

# make directory to save in if it doesn't exist already
if not os.path.isdir(directory+'/rt_analysis/'):
    os.mkdir(directory+'/rt_analysis/')
    print(' made save directory for resting time outputs')
    print(' its location is ' + directory+'/rt_analysis .')

# now iterate thru each and get the resting time distribution
tmax = 1500*3600 #account for 15hrs in the distribution
for f in files:
    n,m,t = np.load(directory+'/'+f) # load the simulation output from file f
    bins, cdf = at.rt_unconditional(t,m,tmax=tmax) # compute the cdf from analysis_tools module 
    sf = f[:-4]+'-RestTime' # the save filename for the cdf
    np.save(directory+'/rt_analysis/'+sf,cdf) # save the cdf from this trial
    del n,m,t,cdf
np.save(directory+'/rt_analysis/bins', bins)  # save the set of times used to compute cdf 
del bins

print(' all trials analyzed ' )
