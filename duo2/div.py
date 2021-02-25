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
import functools 
from tab import Tab, Cols, csv
from lib import cli
from col import Num
from ok  import ok

def ordered(rows,cols): 
  "Sort rows based on `Row.better`."
  def better() : 
    return lambda a,b: (0 if id(a)==id(b)     else (
                       -1 if a.better(b,cols) else 
                        1 ))
  return sorted(rows, key=functools.cmp_to_key(better))

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
