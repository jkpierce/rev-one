import pandas as pd
import numpy as np 
import sys 

filename = sys.argv[1]
filenameshort = filename.split('/')[-1]
print(filename, 'to be analyzed') 
mstatsfilename = filenameshort[:-4]+'-mstats.dat'

# data loader 
load = lambda filename: pd.read_csv(filename, skiprows = 2, usecols = [0,1,2], header = None, 
               delim_whitespace = True, index_col = False, iterator = True, chunksize = 50000)#, nrows=100)

file = load(filename)
i = 0 #keep track of which chunk you're on 
chunked_mean = 0 # running sum of mean(m) values from each chunk 
for chunk in file: 
    _, m, _ = chunk.values.T
    chunked_mean += m.mean()
    i+=1 # keep track of chunk number 
mean_m = chunked_mean/i # the mean

i=0
chunked_var = 0 # running sum of (m-mean(m))**2/chunksize
file = load(filename)
for chunk in file:
    _, m, _ = chunk.values.T
    chunked_var += ((m-mean_m)**2).sum()/m.size # compute the variance of the chunk
    i+=1
std_m = np.sqrt(chunked_var/i)


# compute all of the m values to consider.. go from mean(m)-3*std(m) to mean(m)+3*std(m) 
mvals = np.arange(int(round(mean_m-3*std_m)), int(round(mean_m+3*std_m))+1, 1)
# so now you have the range of m values to consider


# compute the probabilities of each m value 
file = load(filename) # load the iterators again
counts = []
for chunk in file:
    _, m, _ = chunk.values.T
    chunkcounts = []
    for mv in mvals:
        mvcounts = (m == mv).sum()
        chunkcounts.append(mvcounts)
    chunkcounts = np.array(chunkcounts)
    counts.append(chunkcounts)
counts = np.array(counts)
counts = counts.sum(axis = 0)
pmvals = counts/counts.sum()
data = np.array((mvals, pmvals)).T

print(data)
# now you're done, so save the file in TMPDIR
print(mstatsfilename, 'filename to save in TMPDIR')
np.savetxt(mstatsfilename, data)
