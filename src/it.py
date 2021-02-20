#i!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81:
"""
Very succinct object system that bundles nested functions and some get set
methods into a container.

- License: (c) 2021 Tim Menzies <timm@ieee.org>, MIT License  
- Example: see the [demoIt](#it.demoIt) function.

"""
from types import FunctionType as Fun

class it:
  "Simple container of names fields, with methods."
  def __init__(i, **d): i.__dict__.update(d)

  def __repr__(i):
    "Pretty print, sorted keys, ignore private keys (those  with `_`)."
    return "{"+ ', '.join( 
      [f":{k} {v}" for k, v in sorted(i.__dict__.items())
       if  type(v) != Fun and k[0] != "_"])+"}"

  def __add__(i, maybe):
    "For all functions, add them as methods to `i`."
    def method(i,f): 
      return lambda *lst, **kw: f(i, *lst, **kw)
    def memo(i,k,f):
      def worker(*l, **kw):
        if k not in i._memos: i._memos[k] = f(*l, *kw)
        return i._memos[k]
      return worker
    for k,f in maybe.items():
      if type(f) == Fun and k[0] != "_": 
        if k[-1] == "0":
          i._memos = {}
          k = k[:-1]
          f = memo(i,k,f)
        i.__dict__[k] = method(i,f) 
    return i

def anExample():
  from datetime import datetime as date
  def Person(name="Abraham",yob=1809):
    def age(i)   : return date.now().year - i.yob
    def heavy0(i): print(1); return i.age() + i.age()*10
    def exp0(i)  : print(2); return i.age() + i.age()*100
    return it(name=name, smarts=0,yob=yob,weight=0) + locals()
  #---------------------------
  p = Person(name="John")
  print(p)
  p.heavy();  
  p.heavy();  
  p.heavy();  
  p.exp();  
  p.exp();  
  p.exp();  
  print(p._memos)

__name__ == "__main__" and anExample()
