# Rx
A treatment "`Rx`" is a label (`i.rx`) and a set of 
values (`i.all`).  
Statistically indistinguishable
treatments can be `group`ed into
sets of similar values.
:w

## Class

```py
from lib import Thing, xtile

class Rx(Thing):
  dull  = [0.147,0.33, 0.474][0]
  b     = 500
  conf  = 0.05
  cohen = 0.3
  def __init__(i, rx="",all=[], lo=0,hi=1):
    i.rx   = rx
    i.all  = sorted([x for x in all if x != "?"])
    i.lo   = min(i.all[0],lo)
    i.hi   = max(i.all[-1],hi)
    i.n    = len(i.all)
    i.med  = i.all[int(i.n/2)]
    i.parts= [i]
  def __lt__(i,j): 
    return i.med < j.med
  def __eq__(i,j):
    return cliffsDelta(i.all,j.all) and bootstrap(i.all,j.all)
  def __add__(i,j):
    k =  Rx(all = i.all + j.all,
            lo=min(i.lo, j.lo), 
            hi=max(i.hi, j.hi))
    k.parts = i.parts + j.parts
    return k
  def __repr__(i):
    return '%10s %s' % (i.rx, xtile(i.all, i.lo, i.hi))
```
## Statistical Tests
### CliffsDelta
```py
def cliffsDelta(lst1, lst2, dull=Rx.dull):
  def runs(lst):
    for j,two in enumerate(lst):
      if j == 0: one,i = two,0
      if one!=two:
        yield j - i,one
        i = j
      one=two
    yield j - i + 1,two
  #---------------------
  m, n = len(lst1), len(lst2)
  lst2 = sorted(lst2)
  j = more = less = 0
  for repeats,x in runs(sorted(lst1)):
    while j <= (n - 1) and lst2[j] <  x: j += 1
    more += j*repeats
    while j <= (n - 1) and lst2[j] == x: j += 1
    less += (n - j)*repeats
  d= (more - less) / (m*n)
  return abs(d)  <= dull
```
### Bootstrap
Two  lists y0,z0 are the same if the same patterns can be seen in
all of them, as well as in 100s to 1000s  sub-samples from each.
From p220 to 223 of the Efron text  'introduction to the bootstrap'.

```py
def bootstrap(y0,z0,conf=Rx.conf,b=Rx.b):
  class Sum():
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
    def __add__(i1,i2): return Sum(i1.all + i2.all)
  def testStatistic(y,z):
     tmp1 = tmp2 = 0
     for y1 in y.all: tmp1 += (y1 - y.mu)**2
     for z1 in z.all: tmp2 += (z1 - z.mu)**2
     s1    = float(tmp1)/(y.n - 1)
     s2    = float(tmp2)/(z.n - 1)
     delta = z.mu - y.mu
     if s1+s2:
       delta =  delta/((s1/y.n + s2/z.n)**0.5)
     return delta
  def one(lst): return lst[ int(any(len(lst))) ]
  def any(n)  : return random.uniform(0,n)
  y,z  = Sum(y0), Sum(z0)
  x    = y + z
  baseline = testStatistic(y,z)
  yhat = [y1 - y.mu + x.mu for y1 in y.all]
  zhat = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0
  for i in range(b):
    if testStatistic(Sum([one(yhat) for _ in yhat]),
                     Sum([one(zhat) for _ in zhat])) > baseline:
      bigger += 1
  return bigger / b >= conf
```
## Output
### Ranks
Given a dictionary of values, sort the values by their median
then iterative merge together adjacent similar items.

```py
def group(d, cohen=0.3):
  def merge(lst, lvl=0):
    j,tmp = 0,[]
    while j < len(lst):
      x = lst[j]
      if j < len(lst) - 1: 
        y = lst[j+1]
        if abs(x.med - y.med) <= tiny or x == y:
          tmp += [x+y]
          j   += 2
          continue
      tmp += [x]
      j   += 1
    if len(tmp) < len(lst):
      merge(tmp, lvl+1) 
    else:
      for n,group in enumerate(lst):
        [print(n, rx) for rx in group.parts]
  # ------------------------------------------
  p    = lambda n: a[ int( n*len(a) )]
  a    = sorted([x for k in d for x in d[k]])
  tiny = (p(.9) - p(.2))/2.56 * Rx.cohen
  merge(sorted([Rx(rx=k, all=d[k], lo=a[0], hi=a[-1]) 
               for k in d]))
```
