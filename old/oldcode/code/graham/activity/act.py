import numpy as np 
import os 
import sys

def loader(mfile): # this is meant to take in an mfile 
    path_m = '/home/kpierce/scratch/reverting-onecell/analysis/m-stats/'
    path_ed = '/home/kpierce/scratch/reverting-onecell/analysis/entrain-deposit/'
    efile = path_ed+mfile[:-10]+'entrains.npy'
    dfile = path_ed+mfile[:-10]+'deposits.npy'
    te, _ = np.load(efile).T
    td, _ = np.load(dfile).T
    return te, td

files = []
for f in os.listdir('/home/kpierce/scratch/reverting-onecell/analysis/m-stats/'):
    if f.endswith('.dat'):
        files.append(f)

out = []
for filename in files:
    te, td  = loader(filename)
    # now group entrain and deposit together.. 
    t = np.sort(np.concatenate((te,td)))
    a = np.diff(t).mean() # mean duration between entrianment or deposition transition
    out.append((filename,a))

out = np.array(out)
np.savetxt('activities.dat',out)
