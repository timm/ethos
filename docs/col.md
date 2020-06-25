```py
from lib import Pretty
import math

class Col(Pretty):
  no    = "?"
  less  = "<"
  more  = ">"
  num   = "$"
  klass = "!"
  nums  = ["$",">","<"]
  y     = ["!",">","<"]
  #----------------------------------------
  def __init__(i, txt="", pos=0, tab=None):
    i.txt = txt
    i.pos = pos
    i._tab = pos
    i.w   = -1 if Col.less in txt else 1
    i.n   = 0
  def add(i,x):
    if x is Col.no: return x
    i.n += 1
    return i.add1(x)
  def norm(i,x):
    return x if x==Col.no else i.add1(x)
  def dist(i, x,y):
    if x is Col.no and y is Col.no: 
       return 1
    return i.dist1(x,y)
  def all(i, lst=[]):
    [i.add(x) for x in lst]
```
