# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib  import obj,cli
import sys
import copy
import random

def defaults( d= cli(
     seed=1,
     p=2, 
     cohen=.3, 
     enough=.5, 
     far=.9, 
     fars=128, 
     grab=4,
     data="data/weather.csv")):
  d = obj(**d)
  random.seed(d.seed)
  return d
