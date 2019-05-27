import numpy as np 
import sys
file = sys.argv[1]
gile = file.split('/')[-1][:-4] # numpy filename
arr = np.loadtxt(file)
np.save(gile, arr)
print(file, ' converted to ', gile)
