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
  return sorted(rows, key=cmp_to_key(ordered1(cols)))

def ordered1(cols) : 
  return lambda a,b: (0 if id(a)==id(b)     else (
                      1 if a.better(b,cols) else 
                     -1 ))

#----------------------------------
def test_sort():
  "make a table"
  t=Tab(csv("../data/auto93.csv"))
  tmp = ordered(t.rows(), t.cols)
  for x in tmp[:5]: print(t.cols.ys(x))
  print("")
  for x in tmp[-5:]: print(t.cols.ys(x))

test_sort()

if __name__ == "__main__": cli(locals(),__doc__)
