# Project
Recursive bisect the data using random projections.

- [Methods](#methods) 
  - [div](#div-recursive-descent)  : Recursive descent
  - [lohi](#lohi-split-the-rows-into-lo-and-hi)  : Split the rows into lo and hi

---------------

```py
from lib import Thing
from random import random  as r
from random import choice  as any

class Project(Thing):
  min    = 0.5
  enough = 256
  cols   = "x"

  def __init__(i, t, cols):
    i.enough = Project.enough/ len(t.rows)
    i.min    = 2*len(t.rows)**Project.min
    i.div(i,t,  t.cols[cols or Project.cols],
                (for r in t.rows if  r() < i.enough))
```
## Methods
### div: Recursive descent
```py
  def div(i,t, cols, rows):
    t1 = t.clone(rows)
    if len(rows) >= i.min: 
      here = o(tab=t1, los=None, his=None)
    else:
      here     = i.lohi(cols,  t1.rows)
      here.los = i.div(i, t, cols, here.los)
      here.his = i.div(i, t, cols, here.his)
      here.tab = t1
    return here
```
### lohi: Split the rows into lo and hi

```py
  def lohi(i,  cols, rows):
    one = any(rows)
    lo  = one.far(cols, rows)
    hi  = lo.far( cols, rows)
    c   = lo.dist(hi,   cols)
    mid  = 0
    for r in rows:
      a = r.dist(lo, cols)
      b = r.dist(hi, cols)
      x = (a**2 + c**2 - b**2) / (2*c)
      if (x > 1): x = 1
      if (x < 0): x = 0
      mid += x/len(rows)
      r.x = x
    los, his = [],[]
    for r in rows: 
      (los if r.x <= mid else ups).append(r)
    return o(los= los, his= his,
             lo = lo,  hi = hi,
             c  = c,   mid= mid)
```
