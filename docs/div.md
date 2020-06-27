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
  enough = 512
  cols   = "x"

  def __init__(i, t, cols=None):
    i.enough = Div.enough/ len(t.rows)
    i.min    = 2*len(t.rows)**Div.min
    i.div(t,  t.cols[cols or Div.cols],
              [row for row in t.rows if r() < i.enough],
              0)
```
## Methods
### div: Recursive descent
```py
  def div(i,t, cols, rows, lvl):
    t1 = t.clone(rows)
    print(("|.. "*lvl) , len(rows))
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
    one = any(rows)
    lo  = one.far(cols, rows)
    hi  = lo.far( cols, rows)
    c   = lo.dist(hi,   cols)
    mid = 0
    for row in rows:
      a = row.dist(lo, cols)
      b = row.dist(hi, cols)
      x = (a**2 + c**2 - b**2) / (2*c)
      if (x > 1): x = 1
      if (x < 0): x = 0
      mid  += x
      row.x = x
    mid /= len(rows)
    los, his = [],[]
    for row in rows: 
      (los if row.x <= mid else his).append(row)
    return o(kids= [los,his],
             lo = lo,  hi = hi,
             c  = c,   mid= mid)
```
