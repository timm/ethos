#i!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81:
"""
Reads rows from csv file.

- License: (c) 2021 Tim Menzies <timm@ieee.org>, MIT License  

"""
import re
def anExample():
  rows=[row for row in csv("../data/auto93.csv")]
  assert 399== len(rows)
  assert float is type(rows[1][4])
  assert int   is type(rows[1][0])

def csv(file, sep=",", ignore=r'([\n\t\r ]|#.*)'):
  """Helper function: read csv rows, skip blank lines, coerce strings
     to numbers, if needed."""
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
