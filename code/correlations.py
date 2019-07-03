from scipy.interpolate import interp1d
from scipy.signal import correlate
import numpy as np
import sys

# load the data, crop it, mean shift it
filename = sys.argv[1]
dats = np.load(filename,mmap_mode='r')
m = dats[:,1]
t = dats[:,2]
time = 500*3600 # 500 hrs
m = m[t<time]
t = t[t<time]
m-= m.mean()
print('data loaded')

# resample it
dt = 0.5
t1 = np.arange(0,time,dt)
f1 = interp1d(t,m,fill_value='extrapolate')
m1 = f1(t1)
print('data resampled')

# compute the correlation function
cc = correlate(m1,m1)[-len(m1):]
cc = cc/cc.max()
print('correlation computed')

out = [t1,cc]
np.save(filename[:-4]+'_corr',out)
