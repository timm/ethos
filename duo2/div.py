#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
group.py : divide rows in groups of similar ranks  
(c) 2021, Tim Menzies, MIT license.      
https://choosealicense.com/licenses/mit/  
  
USAGE ./group.py [OPTIONS]  
  
 -t S  run demo functions matching S  
 -T    run all demo functions  
 -L    list all demo functions  
 -h    run help  
 -C    show copyright  
"""
from functools import cmp_to_key
from tab import Tab, Cols, csv
from lib import cli
from col import Num
from ok  import ok

def ordered(rows,cols): 
  "Sort rows based on `Row.better`."
  def cmp(cols) : 
    return lambda a,b: (0 if id(a)==id(b)     else (
                       -1 if a.better(b,cols) else 
                        1 ))
  return sorted(rows, key=cmp_to_key(cmp(cols)))

def Span(down,up): 
  new = on(down = down, up = up, _all=[])
  def add(i,x): i._all += [x]
  return new.has(locals())

def unsuper(lst,fx,chop=.5, cohen=.35):
  lst, nums = [], Num()
  for one in enumerate(lst):
    if fx(one) != "?": 
      lst += [nums.add( fx(one) )]
  sd     = nums.sd()
  width  = len(lst)**chop
  while width < 4 and width < len(lst): width *= 1.2
  x      = fx(lst[0])
  latest = Span(x, x)
  out    = [latest]
  b4     = 0
  diffent=1 #XXXX
  for now,one in enumerate(lst):
    x = fx(one)
    if now < len(lst) - width:
      if len(latest._all) > width:
       if latest.up - latest.down > sd*cohen:
         if x != fx(lst[now+1]):
           latest  = Span(latest.up, fx(one))
           out    += [latest]
    latest.up    = x
    latest._all += [one]
  out[ 0].down = -math.inf
  out[-1].up   = math.inf
  return out

#----------------------------------
def test_sort():
  "make a table"
  t=Tab(csv("../data/auto93.csv"))
  tmp = ordered(t.rows(), t.cols)
  for col in t.cols.y:
    print(col.txt, col.mid(), col.sd()*.35)
  for one in tmp[:5]: print(t.cols.ys(one))
  print("")
  for one in tmp[-5:]: print(t.cols.ys(one))

test_sort()

#if __name__ == "__main__": cli(locals(),__doc__)
