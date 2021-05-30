# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Standard library functions."""

import re
import sys
import copy

class obj:
  "Simple base class with pretty print"
  def __init__(i, **d): i.__dict__.update(d)
  def __repr__(i) : return i.__class__.__name__+"{" + ', '.join(
      [f":{k} {v}" for k, v in sorted(i.__dict__.items()) if k[0] != "_"]) + "}"
  def clone(i): return obj(**copy.deepcopy(i.__dict__))

def cli(**d):
  "If command line has :key val, and 'key' is in d, then d[key]=val"
  i=-1
  while i<len(sys.argv)-1:
    i, key, now = i+1, sys.argv[i][1:], coerce(sys.argv[i+1])
    if key in d:
      i += 1
      if type(now) == type(d[key]): d[key] = now
  return d

def csv(src=None):
  """Iterator. returns lines from files or standard input or a string, 
  return an iterator for the lines."""
  def lines(src):
    for line in src:
      line = re.sub(r'([\n\t\r ]|#.*)', '', line)
      if line: 
        line = line.split(",")
        line = [coerce(x) for x in line]
        yield line
  if src and src[-4:] == ".csv":
    with open(src) as fp:  
      for out in lines(fp): yield out
  else:
    src = src.split("\n") if src else sys.stdin
    for out in lines(src):
      yield out

def coerce(string):
  """When  appropriate, coerce `string` into some type. 
  Supports floats, ints, booleans and strings."""
  if string == "True": return True
  if string == "False": return False
  try: return int(string)
  except Exception:
    try: return float(string)
    except Exception: return string

def rs(l,r=0): 
  "Round a list to `r` decimal places."
  return [(f"{x:.{r}f}" if isinstace(x,(inf,float)) else str(x))
          for x in l]
