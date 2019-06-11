#!/usr/bin/env python3

import sys
from math import *

import numpy

from sympy import Symbol
from sympy.physics.hydrogen import Psi_nlm

from argv import argv

r = Symbol("r", real=True, positive=True)
phi = Symbol("phi", real=True)
theta = Symbol("theta", real=True)
Z = Symbol("Z", positive=True, integer=True, nonzero=True)

"""
# Psi_nlm(n, l, m, r, phi, theta, Z)
n, l, m quantum numbers ‘n’, ‘l’ and ‘m’
r radial coordinate
phi azimuthal angle 
theta polar angle 
Z atomic number (1 for Hydrogen, 2 for Helium, …)
"""

f = Psi_nlm(2, 1, 0, r, phi, theta, 1)
print("psi(r, phi, theta) =", f)


vmin = -30.
vmax = 30.
N = 32
delta = (vmax-vmin)/N
vals = list(numpy.arange(vmin, vmax, delta))
nx = ny = nz = len(vals)
sup = 0.

data = []
for x in vals:
 for y in vals:
  for z in vals:
    if abs(x) < 1e-6:
        x += 1e-6 # hack
    _r = sqrt(x**2+y**2+z**2)
    _phi = atan(y/x)
    _theta = acos(z/_r)
    val = f.evalf(subs={r:_r, phi:_phi, theta:_theta})
    val = complex(val)
    val = 10*abs(val)
    if val > sup:
        sup = val
    data.append(val)
print("sup:", sup)

s = ' '.join(str(v) for v in data)

data = """
MakeNamedMedium "smoke" "string type" "heterogeneous" 
        "integer nx" %d "integer ny" %d "integer nz" %d
    "point p0" [ 0.010000 0.010000 0.010000 ] 
    "point p1" [ 1.99 1.99 1.99 ]
    "float density" [
    %s
]
""" % (nx, ny, nz, s)

#name = sys.argv[1]
name = "psi.pbrt"

print("writing to", name)
f = open(name, "w")
f.write(data)
f.close()



