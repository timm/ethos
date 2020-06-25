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
  distant = 0.9
  def __init__(i, cells=[], tab=None):
    i.cells = cells
    i.dom = 0
    i._tab=tab
```
## Domination: multi-objective ranking of two rows

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
## Distance: via the Minkowski  calculation.
Distance is calculated using `cols` which defaults to `i._tab.cols.x`.
### dist
```py
  def dist(i,j, cols=None):
    d, n, p = 0, 0.001, Row.p
    for c in  cols or i._tab.cols.x:
      x   = i.cells[c.pos]
      y   = j.cells[c.pos]
      inc = c.dist(x, y)
      d  += inc**p
      n  += 1
    return (d/n)**1/p
```

### around
Return a list of other rows, sorted by
the distance to this row.
```py
  def around(i, cols=[], rows=[]):
    a = [(i.dist(j, cols), i,j) for j in rows or i._tab.rows]
    a.sort(key=lambda z:z[0])
    return a
```
### far
Return something `i.distant` away (e.g. 90%
to the most distant row).

```py
  def far(i, cols=[], rows=[]):
    a= i.around(i, cols, rows)
    return a[ int( len(a) * Row.distant ) ][2]
```
