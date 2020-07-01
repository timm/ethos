```py
from lib import ok
from ranges import Ranges
from random import random as r


def _range0(xy):
  print("")
  for x,y,z in Ranges(xy).ranges(): 
    print(x,y,0, '%5.3f'%z)


@ok
def _range1():
  n = 10
  _range0([[i,i>n] for i in range(n*2)])

@ok
def _range2():
  n = 10**4
  _range0( [[i, i > .1*n and i<.2*n or i>.7*n ] for i in range(n)])

@ok
def _range3():
  n = 10**4
  _range0( [[i, i > .1*n and i<.2*n or i>.6*n and i<.7*n] for i in range(n)])

@ok
def _range4():
  n = 10**3
  _range0( [[i, 0 if r() < 0.5 else 1] for i in range(n)])

@ok
def _range5():
  n = 10**3
  _range0( [[i, 0] for i in range(n)])

@ok
def _range6():
  n = 10**3
  _range0( [[i, i> .4*n and i < .6*n] for i in range(n)] )
```
