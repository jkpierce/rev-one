import pandas as pd
import numpy as np 
import sys 

filename = sys.argv[1] # the full path of the data file
filenameshort = filename.split('/')[-1] # the filename of the data file

mstatsfilename = sys.argv[2] # the full path of the mstats file
# the entire unconditional return time analysis sequence 

def load(filename, chunksize = 100000000): # 100 million lines should be about 4GB
    """filename is the original output file of the simulation
    chunksize is the size at which to chunk the entrain and deposit file output """
    filenameshort = filename.split('/')[-1]
    datpath = '/home/kpierce/scratch/reverting-onecell/analysis/entrain-deposit/' 
    entrainpath = datpath+filenameshort[:-4]+'-entrains.dat' # generate the filenames for entrainment and deposition 
    depositpath = datpath+filenameshort[:-4]+'-deposits.dat' #
    entrainfile = pd.read_csv(entrainpath, delim_whitespace = True, 
                              index_col = None, iterator = True, chunksize = chunksize)
    depositfile = pd.read_csv(depositpath, delim_whitespace = True,
                              index_col = None, iterator = True, chunksize = chunksize)
    return entrainfile, depositfile # return iteratables for each file 




# define the parameters for analysis 
tmax = 500*3600 # maximum return time to allow for (seconds) 
dt = 0.5 # bin size in seconds
bins = np.arange(0, tmax, dt) # bins 


# define the conditional return time function



def conditional_rt(entrainfile, depositfile, mstar, bins = bins, dt = 0.5, tmax = tmax):
    """compute the return time distribution conditional to elevation mstar
    given entrainfile, the dat of all t, m at entrainment, and depositfile
    the analogue for deposition"""
    
    # first compute all return times
    returns = np.array([]) # compute all of the return times to mstar
    for chunk in entrainfile: # iterate thru entrainment times 
        te,me = chunk.values.T
        chunk_times = te[me==mstar] # returns to mstar within the chunk
        returns = np.concatenate((returns, chunk_times))
    # then compute the departure times     
    departures = np.array([]) # compute all of the departure times from mstar 
    for chunk in depositfile: # compute all of the departures from mstar 
        td,md = chunk.values.T
        chunk_times = td[md==mstar+1]
        departures = np.concatenate((departures, chunk_times))
    
    if ( len(returns) > 0 ) and ( len(departures) > 0 ):

        while ( returns[0] < departures[0] ): # while first return smaller than first departure
            returns = returns[1:] # crop off first return  
        while ( departures[-1] > returns[-1] ): # while last departure greater than last return 
            departures = departures[:-1] # crop off last departure
            
        # at this point, the return time series starts from a departure and end from a return 
        # but there is no guarantee that it doesn't start with k departures or k returns 
        
        # so if it isn't woven as |d,r,d,r,d,r,d,r| ...  that's because 
        # (a) there are two or more departures prior to the first return, |d,d,d,r,d,r,d,r,d,r,d,r| ... or 
        # (b) there are two or more returns post the last departure, |d,r,d,r,d,r,r,r,r| .... 
        # so the number k of repeats is 
        k = len(departures) - len(returns)
        # and if k > 0 it's case (a)
        # and if k < 0 it's case b
        if k > 0: # if there are two or more departures prior to the first return 
            departures = departures[k:] # k is the number of excess departures
        if k < 0: # if there are two or more returns post the last departure
            returns = returns[:k] # k is the number of excess returns

            
        # Now compute the return time distribution 
        crt = returns - departures # compute the conditional return times
        H, bins = np.histogram(crt, bins = bins, density = True) # compute the cdf
        F = 1 - H.cumsum()*dt # each val is the probability that TR exceeds the bin in question
    else:
        F = np.zeros(len(bins)-1,dtype=float)
    
    return F 


# get the statistics of m 
cdffilename = filenameshort[:-4]+'-rtcdf' # filename of the cdf
m, pm = np.loadtxt(mstatsfilename).T # load the m statistics 

# compute all of the conditional return time cdfs for each m value under consideration
cdf = np.zeros(len(bins)-1,dtype=float) # fill this iteratively
# sum in the conditional cdf at every m value multipled by the probability
# of that m value. 
# this is the nakagawa & tusjimoto 1980 / yang & sayre 1971 equation

for mv,p in zip(m, pm): # iterate through all mvalues in question
    entrainfile, depositfile = load(filename) # load in the files again to refresh the iterator 
    Fmv = conditional_rt(entrainfile, depositfile, mv) # calculate the rt cdf conditional to mv
    cdf+=Fmv*p  # append the conditional distribution to the output  

bins = (bins[1:]+bins[:-1])/2.0 # compute the midpoints of the bins 
data = np.array((bins, cdf)).T
np.save(cdffilename, data)
