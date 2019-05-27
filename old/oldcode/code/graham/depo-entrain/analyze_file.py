import pandas as pd
import numpy as np
import sys

filename = sys.argv[1]
entrainpath = filename.split('/')[-1][:-4]+'-entrains.dat'
depositpath = filename.split('/')[-1][:-4]+'-deposits.dat'
print(entrainpath)

# use pandas to load the file in for analysis.
# pandas is nice because it's faster than np.loadtxt and it also supports chunking

linecount = num_lines = sum(1 for line in open(filename))-2 # this takes time.
print('{} lines to process '.format(linecount))
chunksize = int(2e7) # take 20 million lines at once
print('{} chunks to iterate'.format(float(linecount)/chunksize))
file = pd.read_csv(filename, skiprows = 2, usecols = [0,1,2], header = None,
                   delim_whitespace = True, index_col = False, iterator = True, chunksize = chunksize)


# find all entrainment and deposition times within a file

m0 = 50000 # the value of the top of the last chunk

# useful
# https://www.pythonforthelab.com/blog/introduction-to-storing-data-in-files/

entrainfile = open(entrainpath, 'wb+') # w means write
depositfile = open(depositpath, 'wb+')

i = 0
for f in file:
    print('chunk %d'%i)
    i+=1

    n,m,t = f.values.T # unpack the values from the chunk

    # check for entrainment and deposition on the boundary element
    if m[0]==m0+1: # if deposition occurs on lowest boundary of chunk
        np.savetxt(depositfile, np.column_stack((t[0], m[0])))
    elif m[0]==m0-1: # if entrainment occurs on lowest boundary of chunk
        np.savetxt(entrainfile, np.column_stack((t[0], m[0])))
    m0 = m[-1] # reset the boundary value for the next chunk

    # now check for entrainment and deposition within the chunk. Need to exclude lower boundary
    erodemask = m[1:]-np.roll(m,1)[1:]==-1  # indices into t[1:] where erosion occurred 
    depositmask = m[1:]-np.roll(m,1)[1:]==1 # indices into t[1:] where deposition occurred 
    # chunk save errything
    data = np.array([t[1:][erodemask], m[1:][erodemask]]).T
    np.savetxt(entrainfile, data)
    entrainfile.flush()
    data = np.array([t[1:][depositmask], m[1:][depositmask]]).T
    np.savetxt(depositfile, data)
    depositfile.flush()


entrainfile.close()
depositfile.close()
