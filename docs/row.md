# Row

- [Domination](#domination) : 
- [Distance](#distance) : 
  - [dist](#dist) : 
  - [around](#around) : 
  - [far](#far) : 

---------------

```py
from lib import Pretty
import math

class Row(Pretty):
  p=2
  def __init__(i, cells=[], tab=None):
    i.cells = cells
    i.dom = 0
    i._tab=None
    i.p = 2
    i.distant=0.9
```
## Domination
```py
  def dom(i,j):
    cols    = i._tab.cols.y
    s1,s2,n = 0,0,len(cols)+0.0001
    for c in cols:
      x   = i.cells[c.pos]
      y   = j.cells[c.pos]
      x   = c.norm(x)
      y   = c.norm(y)
      s1 -= math.e**(c.w*(x-y)/n)
      s2 -= math.e**(c.w*(y-x)/n)
    return s1/n < s2/n
```
## Distance
Distance is calculated using `cols` which defaults to `i._tab.cols.x`.
### dist
```py
  def dist(i,j, cols=None):
    d, n, p = 0, 0.001, Row.p
    for c in  cols or i._tab.cols.x:
      x   = i.cells[c.pos]
      y   = y.cells[c.pos]
      inc = c.dist(x, y)
      d  += inc**p
      n  += 1
    return (d/n)**1/p
```

### around
```py
  def around(i, cols=[], rows=[]):
    return [(i.dist(i,j, cols), i,j) 
             for j in rows or i._tab.rows].sort()
```
### far
```py
  def far(i, cols=[], rows=[]):
    a= i.around(i, cols, rows)
    return a[ int( len(a) * i.distant ) ][2]

