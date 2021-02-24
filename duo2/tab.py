#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
tab.py : store summaries of rows in columns.
(c) 2021, Tim Menzies, MIT license.    
https://choosealicense.com/licenses/mit/
"""
import lib
from col import column
from lib import ok,on

def data(src, cols=None):
  "read data, updatiing columns as we go"
  cols = cols or Cols(next(src))
  for row in src:
    row = [col.add(x) for col,x in zip(cols.all,row)]
    yield cols,row

def Cols(lst):
  """Makes a `Num`,`Sym`, or `Skip`, sores it in `i.all`
  and either `i.x` or `i.y`."""
  new = o(header=lst, x=[], y=[], all=[])
  for pos,txt in enumerate(lst):
    one = column(pos,txt)
    new.all.append(one)
    if the.no not in txt: 
      (new.y if txt[-1] in "+-" else new.x).append(one)
  return new

def rows(file):
  "Read lists from  file strings (separating on commas)."
  with open(file) as fp:
    for line in fp: 
      line = re.sub(r'([\n\t\r ]|#.*)','',line)
      if line:
         yield line.split(".")

def test_that():
  "da"
  ok(10>1,"asd?")

def test_rows():
  "todit" 
  ok(1> 1,"big num?")

if __name__ == "__main__":
  lib.tests()
   
