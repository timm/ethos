# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib  import obj
import sys

def keys(t,the):
  def bestRest(i,t,the, rows):
    n     = int(len(rows)**the.tiny)
    bests = rows[:n]
    rests = rows[n:]
    if len(rests) >= n*4:
      gap = int(len(rests) / (n*the.mostrest))
      rests = rests[::gap]
    return t.clone(bests), t.clone(rests)

  def like(lst,hs,the,goal):
    prod  = math.prod
    nk    = i.nb if goal else i.nr
    prior = (nk + the.k) / (i.n + the.k*2)
    fs={}
    for text,pos,span in lst:
      fs[txt] = fs.get(txt,0) + f.get((goal,(txt,pos,span)), 0)
    like = prior
    for val in fs.values():
      like  *= (val + the.m*prior) / (nk + the.m)
    return like

  best, rest = i.bestRest(t, the, sorted(t.rows))
  bins = best.bins(rest,the)
  b,r = len(best.rows), len(rest.rows)
  i.n, i.nb, i.nr = b+r, len(best.rows), len(rest,rows)
  
