# Div
Recursive divide the data using random projections.

- [Methods](#methods) 
  - [div](#div-recursive-descent)  : Recursive descent
  - [lohi](#lohi-split-the-rows-into-lo-and-hi)  : Split the rows into lo and hi

---------------

```py
from lib import Thing,o
from random import random  as r
from random import choice  as any

class Div(Thing):
  min    = 0.5
  enough = 256
  cols   = "y"
  debug  = False

  def __init__(i, t, cols=None):
    i.enough = Div.enough/ len(t.rows)
    i.min    = 2*len(t.rows)**Div.min
    i.div(t,  t.cols[cols or Div.cols],
              [row for row in t.rows if r() < i.enough])

```
## Methods
### div: Recursive descent
```py
  def div(i,t, cols, rows, lvl=0):
    t1 = t.clone(rows)
    if Div.debug : 
      print('%s \t %s%s' % (t1.summary(),
                            "|.. " * lvl,
                            len(rows)))
    if len(rows) <  i.min: 
      here = o(tab=t1, los=None, his=None)
    else:
      here      = i.lohi(cols,  t1.rows)
      here.kids = [i.div(t,cols,a, lvl+1) 
                   for a in here.kids],
      here.tab  = t1
    return here
```
### lohi: Split the rows into lo and hi

```py
  def lohi(i,  cols, rows):
    one  = any(rows)
    lo   = one.far(cols, rows)
    hi   = lo.far( cols, rows)
    c    = lo.dist(hi,   cols)
    mid  = 0
    d   = {}
    for row in rows:
      a = row.dist(lo, cols)
      b = row.dist(hi, cols)
      x = (a**2 + c**2 - b**2) / (2*c)
      if (x > 1): x = 1
      if (x < 0): x = 0
      mid  += x
      d[row] = x
    mid, los, his = mid / len(rows), [],[]
    for row in rows: 
      (los if d[row] <= mid else his).append(row)
    best = 0 if lo.dom(hi) else 1
    return o(kids = [los,his],
             lo=lo, hi =hi,
             best = best, rest = 1 - best,
             c =c,  mid=mid)
```
