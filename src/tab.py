# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Manager row, summarized  in columns."""

from lib  import obj,csv
from sym  import Sym
from num  import Num
from skip import Skip
from row  import Row
from ako  import isSkip, isNum, isY, isX, isKlass
import random

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
    return Tab(rows=[[c.txt for c in i.cols.all]] + rows)

  def around(i,r1,the,cols=None,rows=None):
    rows = rows or i.rows
    cols = cols or i.cols.y
    return sorted([(r1.dist(r2,the,cols=cols),r2) 
                   for r2 in rows], key=lambda z:z[0])
  
  def far(i,r1,the,cols=None,rows=None):
    tmp = i.around(r1,the,cols=cols,rows=rows)
    return tmp[ int(the.far * len(tmp)) ][1]
    
  def y(i):      return [col.mid() for col in i.cols.y]
  def mid(i):    return [col.mid() for col in i.cols.all]
  def spread(i): return [col.spread() for col in i.cols.all]

  def __lt__(i,j): 
    return Row(i,i.mid()) < Row(j,j.mid())
    
  def bins(i,j,the):
    return {(kl, (col1.txt, col1.at, span)): f
              for col1, col2 in zip(i.cols.x, j.cols.x)
                 for kl, span, f in col1.discretize(col2, the)}

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

