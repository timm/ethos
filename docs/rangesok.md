```py
from lib import ok
from ranges import Ranges
from random import random as r

@ok
def _range1():
  a,n = [],100
  for i in range(n*2):
    a += [[i, i > n]]
  print("")
  for n,lo,hi,s in Ranges(a,1).prune():
    print(n,lo,hi,s)


@ok
def _range2():
  a,n = [],1000
  for i in range(n):
    a += [[i, i > .1*n and i<.2*n or 
          i>.6*n and i<.7*n]]
  print("")
  for n,lo,hi,s in Ranges(a,1).prune():
    print(n,lo,hi,s)


```
