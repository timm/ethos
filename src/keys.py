# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib  import obj
import sys

class Keys(obj):
  def __init__(i,t,the):
   clusters = Cluster(t,the)
   best,rest = i.bestRest(t,clusters)
     
  def bestRest(i,t,clusters):
    ordered = sorted(clusters.all)
    best = ordered[0]
    rest = t.clone()
    grab = the.grab*len(best.rows)/(len(t.rows) - len(best.rows))
    for t1 in c[1:]:
      for r in t1.rows:
        if random.random() <= grab: rest.add(row)
    return best,rest
