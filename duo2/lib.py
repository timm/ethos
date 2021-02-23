#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
(c) 2021, Tim Menzies, MIT license.    
https://choosealicense.com/licenses/mit/
"""
import sys,inspect,datetime
from pyfiglet import Figlet

def same(x): return x

class color:
  all=dict(
      PURPLE    = '\033[1;35;48m',
      CYAN      = '\033[1;36;48m',
      BOLD      = '\033[1;37;48m',
      BLUE      = '\033[1;34;48m',
      GREEN     = '\033[1;32;48m',
      YELLOW    = '\033[1;33;48m',
      RED       = '\033[1;31;48m',
      BLACK     = '\033[1;30;48m',
      UNDERLINE = '\033[4;37;48m',
      END       = '\033[1;37;0m')
  def say(**d):
    c=color.all
    for k,v in d.items(): 
      return c["BOLD"]+c[k]+v+c["END"]

def ok(x,y):
  print(f"-- {y} ",end=""); 
  try:
    assert x,y
    print(color.say(GREEN="PASS"))
  except Exception:
    print(color.say(RED="FAIL"))

def tests():
  def test(fun):
    print(color.say(YELLOE=f"\n# {fun.__name__} "+("-"*25)))
    print(fun.__doc__)
    fun()
  ############################
  funs = inspect.stack()[1].frame.f_locals
  args = sys.argv
  for n,flag in enumerate(args):
    if flag=="-t":
      test( funs["test_" + args[n+1]] )
    if flag=="-T":
      fig = Figlet(font='larry3d')
      print(fig.renderText('tests')[:-38],end="")
      print(datetime.datetime.now().strftime("%c"))
      for k,fun in funs.items():
        if k[:5] == "test_": test(fun)
