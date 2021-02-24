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
import ok,re,sys,inspect

def same(x): 
  "Return x, unmodified."
  return x

class on:
  """The only class you've ever need? Can convert local functions 
  into methods (which are stored in the container. Pretty
  prints object slots, alphabetically, skipping 'private' 
  attributes (this starting with `_'). """
  def __init__(it, **d) : i.__dict__.update(d)
  def __getitem__(it,k)   : return it.__dict__[k]
  def __setitem__(it,k,v) : i.__dict__[k] = v
  def __add__(it,also): 
    for k in also.__dict__: it[k] = also[k]
    return it
  def __repr__(it): 
    return "{"+ ', '.join(
           [f":{k} {v}" for k, v in sorted(it.__dict__.items()) 
                        if type(v)!=fun and k[0] != "_"])+"}"
  def has(it,d):
    def method(f): return lambda *lst, **kw: f(it, *lst, **kw)
    for k,v in d.items():
      if k[0] != "_":
        if type(v)==fun: it.__dict__[k] = method(v)
    return it

def cli(funs,doc=""):
  "Standard start up function."
  for n,flag in enumerate(sys.argv):
    if flag=="-h": print(doc)
    if flag=="-C": print(doc.split("\n\n")[0])
    if flag=="-L": ok.menu(funs)
    if flag=="-t": ok.some(sys.argv[n+1], funs)
    if flag=="-T": ok.all(funs)
if __name__ == "__main__": cli(locals(),__doc__)

