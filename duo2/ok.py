#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
ok.py : very simple test engine.
(c) 2021, Tim Menzies, MIT license.    
https://choosealicense.com/licenses/mit/

Functions name `test_xxx` are "demo" functions which 
can be run en masse, or just the selected few."
"""
from types import FunctionType as fun
from kolor import say
import pyfiglet
import datetime

def all(funs):
  "Run all functions starting with `test_`."
  print(say(CYAN=pyfiglet.figlet_format("tests", font = "larry3d")), 
        end="")
  print(datetime.datetime.now().strftime("%c"))
  some("test_", funs)

def one(fun):
  "Run one `fun`ction, ignore crashes."
  print(say(YELLOW=f"\n# {fun.__name__} "+("-"*25)))
  print("--",fun.__doc__)
  try: fun()
  except Exception: pass

def menu(funs):
  "List known demo functions"
  for k,v in funs.items():
    if type(v) == fun and k[:-5] == "test_":
      print(fun.__name__, ":", fun.__doc__)

def ok(x,y):
  "Pretty print run of `assert`."
  print(f"  -- {y} ",end=""); 
  try:
    assert x,y    
    print(say(GREEN="PASS"))
  except Exception:
    print(say(RED="FAIL"))

def some(want,funs):
  "Run all functions matching `want`."
  for k,f in funs.items():
    if type(f) == fun:
      if k[:5]=="test_" and want in k: one(f)

#---------------------------------------
def test_ok1(): 
  "ok one ing?"
  ok(1>2, "less-ing?")

def test_ok2(): 
  "ok two ing?"
  ok(10>2, "more-ing?")

if __name__ == "__main__": all(locals())
