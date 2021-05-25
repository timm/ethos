# vim: filetype=python ts=2 sw=2 sts=2 et :

from lib  import obj,csv
from sym  import Sym
from num  import Num
from skip import Skip
from row  import Row
from ako  import isSkip, isNum, isY, isX, isKlass

class Tab(obj):
  def __init__(i,rows=[],file=None):
    i.rows=[]
    i.cols=None
    if file: [i.add(r) for r in csv(file)]
    if rows: [i.add(r) for r in rows]

  def add(i,a):
    a = a.cells if type(a)==Row else a
    if i.cols:
      i.rows += [Row(i,[col.add(x) 
                 for col,x in zip(i.cols.all, a)])]
    else:
      i.cols = Cols(a)

  def clone(i,rows=[]):
    return Tab(rows= [[c.txt for c in i.cols.all]] + rows)

  def around(i,r1,the):
    return sorted([(r1.dist(r2,i.cols.x,the),r2) for r2 in i.rows],
                  key=lambda z:z[0])

  def far(i,r,the):
    a= i.around(r,the)
    return a[ int(len(a) * the.far) ][1]

class Cols(obj):
  def __init__(i,a):
    i.x,i.y,i.all = [],[],[]
    i.klass=None
    for at,txt in enumerate(a):
      new = Skip(at=at,txt=txt) if isSkip(txt) else (
             Num(at=at,txt=txt)  if isNum(txt) else Sym(at=at,txt=txt))
      i.all += [new]
      if not isSkip(txt):
        if isX(txt):     i.x += [new]
        if isY(txt):     i.y += [new]
        if isKlass(txt): i.klass = new

