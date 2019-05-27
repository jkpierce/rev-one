import numpy as np
import sys

########################################################
# This is the analysis script for the simulation data ##
########################################################

filename = sys.argv[1] # get the filename from the argument passed
n, m, t = np.load(filename).T # load the file
s = int(5e7) # sample size for calculating statistics 
bins = np.hstack((np.array([0]),np.geomspace(1e-7,5e7,num=150)))

# your target is to
# 1. compute pdf of n
# 2. compute pdf of m
# 3. compute E and a
# 4. compute P(T_r > t)
# 5. collect filename, trial parameters,
#    and all of the 4 computed objects into
#    one dict and save it.

#########################################################
# TASK 1: COMPUTE PDF OF N ##############################
#########################################################

sn = min(n.size, s)
n_sample = np.random.choice(n, sn, replace = False)
n_unique, i = np.unique(n_sample, return_inverse = True)
pn = np.bincount(i)
pn = pn/pn.sum()
pdf_n = np.array((n_unique, pn)).T
del sn, n_sample, n_unique, i, pn
# done. The output is called pdf_n
print('step 1: pdf of n computed')

##########################################################
# TASK 2: COMPUTE PDF OF M ###############################
##########################################################

sm = min(m.size, s)
m_sample = np.random.choice(m, sm, replace = False)
m_unique, i = np.unique(m_sample, return_inverse = True)
pm = np.bincount(i)
pm = pm/pm.sum()
pdf_m = np.array((m_unique, pm)).T
del sm, m_sample, i
# done. The output is called pdf_m
print('step 2: pdf of m computed') 

##########################################################
# TASK 3: COMPUTE ########################################
##########################################################
# this also involves calculating some components of TASK 4
erodemask = m[1:]-np.roll(m,1)[1:]==-1  # indices into t[1:] where erosion occurred 
depositmask = m[1:]-np.roll(m,1)[1:]==1 # indices into t[1:] where deposition occurred 
te = t[1:][erodemask]
td = t[1:][depositmask]
me = m[1:][erodemask]
md = m[1:][depositmask]
del erodemask, depositmask, m
E = 1.0/np.diff(te).mean()
a = 1.0/np.diff(np.sort(np.concatenate((td,te)))).mean()
# done. The outputs are called E and a. You expect E == a/2
print('step 3: E computed') 

###########################################################
# TASK 4: COMPUTE P(T_r > t) ##############################
###########################################################

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

    if (len(returns)>1) and (len(departs)>1):
        while (returns[0]<departs[0]):
            returns=returns[1:]
        while (departs[-1]>returns[-1]):
            departs=departs[:-1]
        k = len(departs)-len(returns)
        if k>0:
            departs = departs[k:]
        elif k<0:
            returns = returns[:k]
    crt = returns - departs
    H,_ = np.histogram(crt, bins=bins)
    H = H.cumsum()
    if H.max()>0:
    	H = 1.0 - H/H.max()
    return H

def compute_cdf(inputs, bins=bins):
    te, me, td, md, m, pm = inputs # these come from loader
    cdf = np.zeros(len(bins)-1,dtype=float) # sum into this iteratively
    for mv,p in zip(m, pm): # iterate through all mvalues in question
        c_cdf = compute_crt(te, me, td, md, mv)
        cdf+=c_cdf*p
    data = np.array((bins[1:], cdf))
    return data

inputs = te, me, td, md, m_unique, pm
rt_cdf = compute_cdf(inputs).T
# done. The output is called rt_cdf
print('step 4: pdf of return times computed') 

############################################################
# TASK 5: GROUP ALL OUTPUTS INTO A DICT AND SAVE IT ########
############################################################

# first extract l and the flow condition from the filename
l = float(filename.split('/')[-1].split('-')[1].split('_')[1])
flow = filename.split('/')[-1].split('_')[1][0]
duration = filename.split('/')[-1].split('_')[-1][:-4]
# then determine which parameter set should be included into the data dict
if flow=='a':
    params = {'trial':'a', 'nu':5.45, 'la0':6.59, 'si0':4.67, 'ga':0.77, 'mu0':3.74}
elif flow=='g': 
    params = {'trial':'g', 'nu':7.74, 'la0':8.42, 'si0':4.95, 'ga': 0.56, 'mu0':4.34}
elif flow=='i':
    params = {'trial':'i', 'nu':15.56, 'la0':22.07, 'si0':4.52, 'ga': 0.68, 'mu0':3.56}
elif flow=='l':
    params = {'trial':'l', 'nu':15.52, 'la0':14.64, 'si0':4.77, 'ga': 0.48, 'mu0':4.32}
elif flow=='n':
    params = {'trial':'n', 'nu':15.45, 'la0':24.49, 'si0':4.21, 'ga':0.36, 'mu0':3.64}

# now compute the ancey2008 values expected for mean_n and var_n 
anc_n_mean = (params['la0']+params['nu'])/(params['si0'] + params['ga'] - params['mu0'])
anc_n_var = (params['la0']+params['nu'])*(params['si0'] + params['ga'])/(params['si0'] + params['ga'] - params['mu0'])**2

# now build the output dictionary of all data computed
output = {'filename':filename, 'l':l, 'parameters': params, 'n_pdf':pdf_n, 'm_pdf':pdf_m, 'rt_cdf':rt_cdf, 'ancey_n_stats':{'n_mean':anc_n_mean, 'n_var':anc_n_var}, 'E': E, 'a': a, 'duration':duration}

# now save the output
outfile = filename.split('/')[-1][:-4]+'-analysis' # filename at which to save the output dict 
np.save(outfile, output) # then save the dict
print('computation completed for file %s'%filename)
# completed.
