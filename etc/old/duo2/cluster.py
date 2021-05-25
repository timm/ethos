#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
(c) 2021, Tim Menzies, MIT license.    
https://choosealicense.com/licenses/mit/
"""

def dist(r1, r2, cols):
  def norms(col, x): x=col.norm(x); return x,(1 if x<0 else 0)
  d,n = 0,1E-32
  for col in cols.y:
    a,b  = r1[col.pos], r2[col.pos]
    a,b  = col.norm(a), col.norm(b)
    d   += (a-b)**2
    n   += 1
  return (d/n)**.5

def far(r1, rows, cols):
  most = -1
  for r2 in rows:
    tmp = dist(r1,r2,cols)
    if tmp>most: most,out = tmp,r2
  return out

def poles(rows):
  one = far(random.choice(rows), rows)
  two = far(one,rows)
  ones, twos = [], []
  for row in rows:
    (twos if dist(row,two,about) < dist(row,one,about) else ones).append(row)
  return o(_rows=rows,up=None,down=None,one=one,ones=ones,two=two,twos=twos) 

def rows2tree(rows, lo, lvl=0):
  if len(rows) > lo and lvl<10:
    here      = poles(rows)
    here.down = rows2tree(here.twos, lo, lvl+1)
    here.up   = rows2tree(here.ones, lo, lvl+1)
    return here
  return worker(rows0, len(rows0)**0.5)

def leaves(tree,lvl=0):
  if tree and tree.up:
    for x in leaves(tree.up,   lvl+1): yield x
    for x in leaves(tree.down, lvl+1): yield x
  else:
    yield lvl,tree._rows
