"""
Misc python utils
(c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.
"""

import argparse
import random
import time
import math
import sys
import re
from tiny import o, of

def r():
  "Return a random number."
  return random.random()

def seed(x):
  "Reset the seed."
  return random.seed(x)

def any(lst):
  "Return any item from a list."
  return random.choice(lst)

def isa(x, y):
  "Returns true if `x` is of type `y`."
  return isinstance(x, y)

def numsp(x):
  "Returns true if `x` is a container for numbers."
  return isa(x, list)

def symsp(x):
  "Returns true if `x` is a container for symbols."
  return isa(x, dict)

def mu(lst):
  "Mean of a list."
  return sum(lst) / len(lst)

def sd(lst):
  "Standard deviation of a list."
  return (lst[int(.9 * len(lst))] - lst[int(.1 * len(lst))]) / 2.56

def csv(file, sep=",", ignore=r'([\n\t\r ]|#.*)'):
  """Misc: reads csv files into list of strings.
  Kill whitespace and comments.
  Converts  strings to numbers, it needed. For example,
  the file .. / data / weather.csv is turned into

    ['outlook', '<temp', 'humid', '?wind', '?!play']
    ['sunny', 85, 85, 'FALSE', 'no']
    ['sunny', 80, 90, 'TRUE', 'no']
    ['overcast', 83, 86, 'FALSE', 'yes']
    ['rainy', 70, 96, 'FALSE', 'yes']
    etc

    """
  def atom(x):
    try:
      return int(x)
    except Exception:
      try:
        return float(x)
      except Exception:
        return x
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(ignore, '', a).split(sep)]


def args(what, txt, d):
  """Misc: Converts a dictionary `d` of key = val
   into command line arguments."""
  def arg(txt, val):
    eg = "[%s]" % val
    if val is False:
      return dict(help=eg, action='store_true')
    return dict(help=eg, default=val,
                metavar=("I" if isa(val, int) else (
                    "F" if isa(val, float) else "S")),
                type=(int if isa(val, int) else (
                    float if isa(val, float) else str)))

  ###############
  p = argparse
  parser = p.ArgumentParser(
      prog=what, description=txt,
      formatter_class=p.RawDescriptionHelpFormatter)
  for key, v in d.__dict__.items():
    parser.add_argument("-" + key, **arg(key, v))
  return o(**vars(parser.parse_args()))
