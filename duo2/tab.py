#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
tab.py : store rows, summarize them in columns"
(c) 2021, Tim Menzies, MIT license.      
https://choosealicense.com/licenses/mit/  
  
USAGE ./tab.py [OPTIONS]  
  
 -t S  run demo functions matching S  
 -T    run all demo functions  
 -L    list all demo functions  
 -h    run help  
 -C    show copyright  
"""
import re, math, functools
from lib import chunks, cli, on
from ok  import ok
from col import column,Some

def data(src, cols=None):
  "Read data, updatiing columns as we go."
  cols = cols or Cols(next(src))
  for row in src:
    row = [col.add(x) for col,x in zip(cols.all,row)]
    yield cols,row

def Row(x):
  "Thing to store row data."
  new = on(gt=0, tag=None, cells = (x if type(x) else x.cells))
  def better(i,j,cols):
    s1,s2,n = 0,0,len(cols.y)
    for col in cols.y:
      pos,w = col.pos, col.w
      a,b   = i.cells[pos], j.cells[pos]
      a,b   = col.norm(a), col.norm(b)
      s1   -= math.e**(w*(a-b)/n)
      s2   -= math.e**(w*(b-a)/n)
    return s1/n < s2/n
  return new.has(locals())

def Cols(lst):
  """Makes a `Num`,`Sym`, or `Skip`, sores 
  it in `i.all` and either `i.x` or `i.y`."""
  new = on(header=lst, x=[], y=[], all=[])
  for pos,txt in enumerate(lst):
    one = column(pos,txt)
    new.all.append(one)
    if "?" not in txt: 
      (new.y if txt[-1] in "+-" else new.x).append(one)
  def ys(i,row): 
    return [row.cells[col.pos] for col in i.y]
  return new.has(dict(ys=ys))

def Tab(src=[], keep=1024, div=lambda z:2*len(z)**.5):
  new = on(_rows=Some(keep=keep), cols=None)
  for cols, row in  data(src):
    new.cols = cols
    new._rows.add(Row(row))
  def clone(i): 
    return Cols([i.cols.header])
  def clusters(i): 
    f= lambda a,b:(0 if id(a)==id(b) else (-1 if a.better(b,cols) else 1))
    return list(chunks(sorted(i.rows(), key=functools.cmp_to_key(f)),
                        div(i.rows())))
  def rows(i): 
    return i._rows._all
  return new.has(locals())

def csv(file):
  "Read lists from  file strings (separating on commas)."
  with open(file) as fp:
    for line in fp: 
      line = re.sub(r'([\n\t\r ]|#.*)','',line)
      if line:
         yield line.split(",")

#----------------------------------
def test_tab():
  "make a table"
  t=Tab(csv("../data/auto93.csv"))
  one = t.cols.all[1]
  t1 = Tab(iter([t.cols.header]))
  rows=[]
  for cols, row in data([t.cols.header]+[row for row in t.rows]):
    rows += [Row(row)]
  print(len(rows))   
  # print([len(a) for a in t.clusters()])
  # ok(395 == one.n, "summarized right?")
  # print([len(a) for a in t.clusters()])
  # ok(395 == len(t._rows._all),"kept enough?")
  #
test_tab()

if __name__ == "__main__": cli(locals(),__doc__)
