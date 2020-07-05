```py
from rx  import group
from lib import ok
from random import random as r

@ok
def _rx1():
  n = 1000
  rx1=[r()      for _ in range(n)]
  rx1a=[x*1.01  for x in rx1]
  rx1b=[x*1.02  for x in rx1]
  rx1c=[x*1.03  for x in rx1]
  rx2=[r()**2   for _ in range(n)]
  rx3=[r()**0.5 for _ in range(n)]
  group(dict(
           rx1=rx1,
           rx1a=rx1a,
           rx1b=rx1b,
           rx1c=rx1c,
           rx2=rx2,
           rx3=rx3))
@ok
def _rx2():
  n = 256
  group(    
     dict(
     x1 = [ 0.34, 0.49 ,0.51, 0.6]*n,
     x2 = [0.6  ,0.7 , 0.8 , 0.89]*n,
     x3 = [0.13 ,0.23, 0.33 , 0.35]*n,
     x4 = [0.6  ,0.7,  0.8 , 0.9]*n,
     x5 = [0.1  ,0.2,  0.3 , 0.4]*n),
     width= 30,
     chops= [.25,  .5, .75],
     marks= ["-", "-", " "])
```
