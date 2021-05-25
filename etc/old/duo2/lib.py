#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
lib.py : v1.0,  misc Python functions    
(c) 2021, Tim Menzies, MIT license.      
https://choosealicense.com/licenses/mit/  
  
USAGE ./lib.py [OPTIONS]  
  
 -t S  run demo functions matching S  
 -T    run all demo functions  
 -L    list all demo functions  
 -h    run help  
 -C    show copyright  
"""
from types import FunctionType as fun
import ok,re,sys,inspect,functools

def same(x): 
  "Return x, unmodified."
  return x

def chunks(a, n):
  """Yield successive n-sized chunks from lst. If there's 
  any leftover slack, add that to the middle chunk."""
  n    = int(n)
  mid  = len(a)//2-n
  jump = n+n+len(a)%n
  for i in range(0, mid, n): yield a[i:i+n]
  yield a[i+n:i+jump] 
  for i in range(i+jump, len(a), n): yield a[i:i+n]

class on:
  """The only class you've ever need? Can convert local functions 
  into methods (which are stored in the container. Pretty
  prints object slots, alphabetically, skipping 'private' 
  attributes (this starting with `_'). """
  def __init__(i, **d)   : i.__dict__.update(d)
  def __getitem__(i,k)   : return i.__dict__[k]
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __add__(i,j): 
    for k in j.__dict__: i[k] = j[k]
    return i
  def __repr__(i): 
    return "{"+ ', '.join(
           [f":{k} {v}" for k, v in sorted(i.__dict__.items()) 
                        if type(v)!=fun and k[0] != "_"])+"}"
  def has(i,d):
    "Add any functions from `d` as methods inside `i`."
    def method(f): return lambda *lst, **kw: f(i, *lst, **kw)
    for k,v in d.items():
      if k[0] != "_":
        if type(v)==fun: i.__dict__[k] = method(v)
    return i

def cli(funs,doc=""):
  "Standard start up function."
  for n,flag in enumerate(sys.argv):
    if flag=="-h": print(doc)
    if flag=="-C": print(doc.split("\n\n")[0])
    if flag=="-L": ok.menu(funs)
    if flag=="-t": ok.some(sys.argv[n+1], funs)
    if flag=="-T": ok.all(funs)

#------------------------------------------------
def test_chunks():
  "Divide a list into chunks"
  lst = [x for x in range(87)]
  lst = [len(a) for a in chunks(lst, int(len(lst)**0.5))]
  print(lst[9], lst)
  #ok.ok( lst[ 0] == 9, "want seven" )
  #ok.ok( lst[-1] == 9, "want nine" )

if __name__ == "__main__": cli(locals(),__doc__)

