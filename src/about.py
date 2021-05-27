# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib  import obj,cli
import sys
import copy
import random

def defaults( d= cli(
     cohen     = .3
     ,data     = "data/weather.csv"
     ,far      = .9 
     ,k        = 1
     ,m        = 2
     ,mostrest = 3
     ,p        = 2 
     ,seed     = 1
     ,tiny     = .5
  )):
  d = obj(**d)
  random.seed(d.seed)
  return d
