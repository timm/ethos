# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, Tim Menzies (timm@ieee.org) unlicense.org
"""Recursively divide the data in two
using the cosine rule (divide the data at median
distance of each row's position, projected into
a line between two distant points)."""

import random
from lib import rs

def div(t,the,cols=None,loud=False):
  clusters = []
  cols = cols or t.cols.x
  tiny = len(t.rows)**the.tiny // 1
  def recurse(rows, lvl=0):
     dist    = lambda r1,r2 : r1.dist(r2,the, cols=cols)
     faraway = lambda r1    : t.far(r1, the, cols=cols, rows=rows)
     if loud: 
       print(f"{'|.. ' * lvl}{len(rows)}")
     if len(rows)<2*tiny: 
       clusters.append(t.clone(rows))
     else               : 
       # find  two distant points, in  linear times
       any   = random.choice(rows)
       left  = faraway(any)
       right = faraway(left)
       c     = dist(left,right)
       # map everyone onto a line between the two distant points
       for row in rows:
         a = dist(row,left)
         b = dist(row,right)
         x = (a**2 + c**2 - b**2)/(2*c+1E-32) # cosine rule
         row.fastmapx = x
       # sort everyone along that line
       rows = sorted(rows, key=lambda row: row.fastmapx)
       mid  = len(rows)//2
       recurse(rows[:mid], lvl+1)  # recurse on the left-hand-side half
       recurse(rows[mid:],  lvl+1) # recurse on the right-hand-side half

  #-- main ----------
  recurse(t.rows)
  return clusters
 
