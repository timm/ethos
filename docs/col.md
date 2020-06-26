# Columns

- [Magic Constants](#magic-constants) 
- [Methods](#methods) 
  - [Initialization](#initialization) 
  - [Batch processing of a list](#batch-processing-of-a-list) 
  - [Methods that know to avoid don't know](#methods-that-know-to-avoid-dont-know) 

---------------

```py
from lib import Thing
import math
```
## Magic Constants

```py
class Col(Thing):
  no    = "?"
  less  = "<"
  more  = ">"
  num   = "$"
  klass = "!"
  nums  = ["$",">","<"]
  y     = ["!",">","<"]
```

## Methods
### Initialization
Set weight to -1 if txt has "_<_".
```py
  def __init__(i, txt="", pos=0, tab=None):
    i.txt = txt
    i.pos = pos
    i._tab = pos
    i.w   = -1 if Col.less in txt else 1
    i.n   = 0
```
### Batch processing of a list
```py
  def all(i, lst=[]):
    [i.add(x) for x in lst]
```
### Methods that know to avoid don't know

```py
  def add(i,x):
    if x is Col.no: return x
    i.n += 1
    return i.add1(x)
  def norm(i,x):
    return x if x==Col.no else i.norm1(x)
  def dist(i, x,y):
    if x is Col.no and y is Col.no: 
       return 1
    return i.dist1(x,y)
```
