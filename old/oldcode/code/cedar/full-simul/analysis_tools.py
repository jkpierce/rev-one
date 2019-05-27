import numpy as np 


# S = np.load('../simulations/flow_i-l_2.199-time_2500hr-rate_5Hz.npy')
# n,m,t = S

def rt_cdf_marginal(t,m,mstar,dt,tmax):
    """compute the return time distribution conditional to (integer) elevation mstar given a time series of transitions t
    and a series m(t) of bed elevations across this time series"""
    departures, = np.where( (np.roll(m,1) <= mstar) & (m > mstar) ) # indices of depature from mstar
    returns, = np.where( (np.roll(m,1) > mstar) & (m <= mstar)  ) # indices of return to mstar
    # must start from a departure
    while returns.min()<departures.min():
        returns = returns[1:]
    # must end at a return
    while returns.max()<departures.max():
        departures = departures[:-1]
    # compute the return times    
    rt = t[returns] - t[departures] 
    # generate a return time distribution to elevation mstar from above
    bins = np.arange(0,tmax, dt)
    H,bins = np.histogram( rt , bins = bins, normed = True)
    dx = bins[1] - bins[0] # bin size 
    F = 1-np.cumsum(H)*dx # cumulative distribution of return time 
    return F  

def rt_unconditional(t,m,dt=3.0,dm=5,tmax=5*3600):
    """compute the unconditional return time from above of the bed elevation time series
    dt is the time resolution... suggested 5.0s 
    dm is the space resolution... suggested 5 (particles)
    t is the times at which bed elevations change
    m is the time series of bed elevation values at these times
    tmax is the maximum return time to accommodate
    """
    mmin = round(m.mean()-3*m.std()) # the minimum m value to include 
    mmax = round(m.mean()+3*m.std()) # the range of m values to include into the computation of the resting time cdf 
    #dm = 5  # the interval between m values to discretize bed elevations over 
    mvals = np.arange(mmin,mmax+dm,dm) # the set of values of m over which to calculate the pdf of bed elevations 
    pm,_ = np.histogram(m,bins=mvals, normed=True)    # the pdf of bed elevations 
    pm = pm*dm # pdf of bed elevations
    mvals = np.arange(mmin,mmax,dm) # the set of m values over which the bed elevation pdf is known
    bins = np.arange(0,tmax, dt)
    pTm = np.array([rt_cdf_marginal(t,m,mv,dt,tmax) for mv in mvals]) # marginal cdf of return time from above across elevations
    cdf = (pTm*pm.reshape(-1,1)).sum(axis=0)  # cumulative resting time distribution -- convolve all bed elevations like Yang and Sayre or Nakagawa Tsujimoto 
    # or Voepel and Hassan 
    return bins[1:],cdf # return times t and cumulative distribution P(T>t) 
