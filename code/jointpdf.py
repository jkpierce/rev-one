import numpy as np 
import sys
n,m,t = np.load(sys.argv[1]).T
nn = np.arange(0,25)
mm = np.arange(-40,41)
pairs =  np.array(np.meshgrid(nn,mm)).reshape(-1,2)
del nn, mm 
counts = []
N = len(pairs)
for i,p in enumerate(pairs):
    nn,mm = p
    c = ((nn==n) & (mm==m)).sum()
    counts.append(c)
    print(round(i*100.0/N,1), ' percent complete.')
out = np.empty((3,N))
out[0] = pairs[:,0]
out[1] = pairs[:,1]
out[2] = np.array(counts)
np.save('pdf.npy',out)
