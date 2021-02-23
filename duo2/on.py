#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
(c) 2021, Tim Menzies, MIT license.    
https://choosealicense.com/licenses/mit/

The only class you've ever need? Can convert local functions 
into methods (which are stored in the container. Pretty
prints object slots, alphabetically, skipping 'private' 
attributes (this starting with `_').
"""
import re
from types import FunctionType as fun

class on:
  def __init__(i, **d) : i.__dict__.update(d)
  def __getitem__(i,k)   : return i.__dict__[k]
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __or__(i,j): 
    for k in j.__dict__: i[k] = j[k]
    return i
  def __repr__(i): 
    return "{"+ ', '.join([f":{k} {v}" for k, v in sorted(i.__dict__.items()) 
                                       if type(v)!=fun and k[0] != "_"])+"}"
  def __add__(i,d):
    def method(i,f): return lambda *lst, **kw: f(i, *lst, **kw)
    for k,v in d.items():
      if type(v)==fun: i.__dict__[k] = method(i,v)
    return i
