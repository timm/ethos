# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Management of default config options. 
Each option "xx" can be, optionally,
overwritten at start-up time by a flag `-xx value`."""

from lib  import obj,cli
import sys,copy,random

def defaults( d= cli(
     cohen     = .3
     ,data     = "data/weather.csv"
     ,far      = .9 
     ,k        = 1
     ,m        = 2
     ,mostrest = 3
     ,p        = 2 
     ,seed     = 1
     ,train    = .66
     ,tiny     = .6
  )):
  """Calling `default` will return a fresh copy of the defaults
  (optionally updated via command-line flags), and will reset
  the random number seed to the `seed` value shown above."""
  d = copy.deepcopy(obj(**d))
  random.seed(d.seed)
  return d
