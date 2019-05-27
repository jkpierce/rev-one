## parameters 

# rates 
b = 100.0 # controls bed fluctuations
nu = 10.99 # emigration rate
la0 = 21.40 # entrainment rate 
la1 = la0/b # entrainment rate fluctuations
si0 = 4.91 # deposition rate 
si1 = si0/b # deposition rate fluctuations 
ga = 0.74 # immigration rate 
mu0 = 3.47 # collective entrainment rate 
mu1 = mu0/b # collective entrainment rate fluctuations 

# dimensions
a = 0.25 # particle radius 
dx = 22.5 # control volume cell size 
phi = 0.6 # packing fraction 

# initial values 
n0 = 21 #initial number of moving particles 
m0 = 503 # initial number of stationary particles 