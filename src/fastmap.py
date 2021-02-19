#i!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81:
"""
Recursive k=2 division of data. Centroids picked via
random projection.

- License: (c) 2021 Tim Menzies <timm@ieee.org>, MIT License  

"""
import re
from it import it
from csv import csv

def anExample():
  rows=[row for row in csv("../data/auto93.csv")]
  assert 399== len(rows)
  assert float is type(rows[1][4])
  assert int   is type(rows[1][0])

def fastmap(src):
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(ignore, '', a).split(sep)]

def atom(x):
  "Coerce x to the right kind of string (int, float, or string)"
  try: return int(x)
  except Exception:
    try:              return float(x)
    except Exception: return x

__name__ == "__main__" and anExample()
