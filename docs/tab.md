
# Tab
Tables stores [Row](row)s. Row values are summarized in 
[Num](num)eric or [Sym](sym)bolic columns.

- [Add headers](#add-headers) : 
- [Add row](#add-row) : 
- [Read a table](#read-a-table) : 

---------------


```py
from lib import Thing,o,cols,rows,src,ins
from col import Col
from sym import Sym
from num import Num
from row import Row

class Tab(Thing):
  def __init__(i, file=None, cols=[], rows=[]):
    i.rows  = []
    i.cols  = o(all= [],   # all columns
               nums= [],   # just the numeric columns
               x   = [],   # just the independent columns
               y   = [],   # just the dependent columns
               klass=None) # just the klass column
    i.headers(cols)        # does nothing in no cols 
    [i.row(one) for one in rows] # does nothing if no rows
    if file: i.read(file)        # does nothing if no file
```
## Add headers
Updating the `i.cols` sublists.

```py
  def headers(i,cols): 
    for pos,txt in enumerate(cols):
      klass = Num if ins(Col.nums, txt) else Sym
      col   = klass(txt,pos)
      xy    = i.cols.y if ins(Col.y, col.txt) else i.cols.x  
      xy   += [col]
      if ins(Col.nums, col.txt) : i.cols.nums += [col]
      if Col.klass in txt       : i.cols.klass = col
      i.cols.all += [col]
```
## Add row
Updating the `i.rows` and, as a side-effect, update
the column summaries

```py
  def row(i,lst):
    if isinstance(lst,Row): 
       return i.row(lst.cells)
    lst     = [ c.add(x) for x,c in zip(lst,i.cols.all) ]
    i.rows += [ Row(lst,i) ]
```
## Read a table

```py
  def read(i, data):
    for lst in cols(rows(src(data))):
      i.row(lst) if i.cols.all else i.headers(lst)
```
## Clone a table
Copy the format of this table to make a new one.
Optionally, add in some rows.

```py
  def clone(i,rows=[]):
    return Tab(cols = [c.txt for c in i.cols.all],
               rows = rows)
```
## Summary
```py
  def summary(i):
    return ', '.join([('%5.2f' % c.mid()) for c in i.cols.y])
```
