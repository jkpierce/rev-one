import numpy as np 
import matplotlib.pyplot as plt
import os
import datetime
import sys


# define parameters
tmax = 500*3600 # maximum return time to allow for (seconds) 
dt = 0.5 # bin size in seconds
bins = np.arange(0, tmax, dt) # bins over which to histogram

def compute_crt(te, me, td, md, mv, bins = bins):
    """ 
    compute conditional return time given
    - entrainment timeseries te
    - bed elevations me at entrainment
    - deposition timeseries td
    - bed elevations md at deposition
    - a value mv at which to condition
    - a set of bins in time over which to histogram 
    """
    returns = te[me==mv]
    departs = td[md==mv+1]
    
    if (len(returns)>0) and (len(departs)>0): 
        while (returns[0]<departs[0]):
            returns=returns[1:]
        while (departs[-1]>returns[-1]):
            departs=departs[:-1]
        k = len(departs)-len(returns)
        if k>0:
            departs=departs[k:]
        elif k<0:
            returns=returns[:k]
        crt = returns-departs
        H,_ = np.histogram(crt,bins=bins,density=True)
        F = 1-H.cumsum()*(bins[1]-bins[0])
    else:
        F = np.zeros(len(bins)-1,dtype=float)
    return F


def loader(mfile): # this is meant to take in an mfile 
    path_m = '/home/kpierce/scratch/reverting-onecell/analysis/m-stats/'
    path_ed = '/home/kpierce/scratch/reverting-onecell/analysis/entrain-deposit/'
    efile = path_ed+mfile[:-10]+'entrains.npy'
    dfile = path_ed+mfile[:-10]+'deposits.npy'
    cfile = mfile[:-10]+'rtcdf'
    te, me = np.load(efile).T
    td, md = np.load(dfile).T
    m, pm  = np.loadtxt(path_m+mfile).T
    return (te, me, td, md, m, pm, cfile)

def compute_cdf(inputs, bins=bins):
    te, me, td, md, m, pm, cfile = inputs # these come from loader
    cdf = np.zeros(len(bins)-1,dtype=float) # fill this iteratively
    i = 0 
    for mv,p in zip(m, pm): # iterate through all mvalues in question
        i+=1
        Fmv = compute_crt(te, me, td, md, mv)
        cdf+=Fmv*p
    bins = (bins[1:]+bins[:-1])/2.0 # compute the midpoints of the bins 
    data = np.array((bins, cdf)).T
    np.save(cfile, data)

f = sys.argv[1] # this is the input filename to consider 
inputs = loader(f)
compute_cdf(inputs)

