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
savedir = directory+'/prob_analysis/'
if not os.path.isdir(savedir):
    os.mkdir(savedir)
    print(' made save directory for entrainment rate and pdf outputs')
    print(' its location is ' + savedir)

# now iterate thru each and get the joint pdf of n,m

for f in files:
    n,m,t = np.load(directory+'/'+f) # load the simulation output from file f

    # compute P(n,m) 
    dn = 1 # bin size for particle activity
    dm = 1 # bin size for bed elevations 
    nr = np.arange(0,round(10*n.std())+dn,dn) # range of n values over which to eval P(n,m)
    mr = np.arange(round(m.mean()-5*m.std()),round(m.mean()+5*m.std())+dm,dm) # range of m vals
    bins = [nr,mr] 
    hist,nr,mr =np.histogram2d(n,m,bins=bins,normed=True) # hist.shape = (nrange.size,mrange.size)
    nr, mr = np.meshgrid(nr[:-1], mr[:-1])
    vals = np.c_[nr.ravel('F'), mr.ravel('F'), hist.ravel()]
    nn,mm,pp = vals.T # n, m, p pairs .. p is probability P(n,m) 


    sf = f[:-4]+'-JointPDF' # the save filename for the joint pdf of n and m 
    np.save(savedir+sf,vals) # save the pdf from this trial
    del n,m,t,pdf
    print('pdf of ' +f + ' analyzed' )
print(' all trials analyzed ' )
