# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, Tim Menzies (timm@ieee.org) unlicense.org
"""Supervised discretization -y pairs.
Returns `bins` that divides the `x` values in order to
minimize the variability of the `y` values.

Democratization is a two-stage process. Firstly, using the `x` values,
`div`ide the data 
into small chunks of length `width` (that are at cover a range of `epsilon` or more).
Secondly, using the `y` values, keep trying to merge adjacent bins (stopping when no
new merges found)."""

from lib import obj
from sym import Sym
import math

class Bin(obj):
  def __init__(i, down=-math.inf, up=math.inf): 
     i.down, i.up, i.also = down, up, Sym()

def div(xy, epsilon, width):
  while width < 4 and width < len(xy) / 2:
    width *= 1.2  # if width  too small, nudge it up a little.
  xy = sorted(xy)
  now = Bin(down=xy[0][0], up=xy[0][0])
  out = [now]
  for j, (x, y) in enumerate(xy): # always update `now`.
    if j < len(xy) - width:
      if now.also.n >= width:
        if x != xy[j + 1][0]:
          if now.up - now.down > epsilon:
            now = Bin(down=now.up, up=x) # sometimes, make a new `now`
            out += [now]
    now.up = x
    now.also.add(y)
  out[0].down = -math.inf
  out[-1].up = math.inf
  return out

def merge(b4):
  """If anything merges, then  go back and do it all again.
  Returns a  list of `Bin`s."""
  j, tmp, n = 0, [], len(b4)
  while j < n:
    a = b4[j]
    if j < n - 1:
      b = b4[j + 1]
      if c := a.also.merged(b.also):
        a = Bin(a.down, b.up)
        a.also = c
        j += 1
    tmp += [a]
    j += 1
  return merge(tmp) if len(tmp) < len(b4) else b4
