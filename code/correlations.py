import numpy as np
import scipy
from scipy import signal



def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size//2:]/result.max()

print('go!')
corrs={}
files = ['../data/flow_a-l_0.6-time_1500.0hr_CAT.npy'] # temporary
time = 10*3600 # total seconds to include
dt = 5 # sampling interval in seconds 
N = int(time/dt) 

for f in files:
    _,m,t = np.load(f,mmap_mode='r').T
    mm = m[t<time] 
    tt = np.arange(0,N*dt,dt)
    mm = scipy.signal.resample(mm,N)
    mm = mm - mm.mean()
    cc = autocorr(mm)
    tt = tt[:cc.size]
    print(tt.size,cc.size)
    corrs['f']=[tt,cc]
    
np.save('../correlations',corrs)

