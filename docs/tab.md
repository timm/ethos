
# Tab
Stores rows. Row values are summarized in columns.

- [Add headers](#add-headers) : 
- [Add row](#add-row) : 
- [Read a table](#read-a-table) : 


```py
from lib import Pretty,o,cols,rows,source,ins
from col import Col
from sym import Sym
from num import Num
from row import Row

class Tab(Pretty):
  def __init__(i,file=None,cols=[],rows=[]):
    i.rows  = []
    i.cols  = o(all=[], nums=[], x=[], y=[],klass=None)
    i.headers(cols)     # does nothing in no cols provided
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
    for lst in cols(rows(source(data))):
      i.row(lst) if i.cols.all else i.headers(lst)
```


