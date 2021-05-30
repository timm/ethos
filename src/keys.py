# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Simple greedy  search for contrast sets."""

from lib  import obj,rs
import random,sys
from row import Row

def keys(t,the,r=2):
  rows = t.rows[:]
  random.shuffle(rows)
  shows([col.txt for col in t.cols.y])
  shows(t.y()        + ["baseline", len(rows)])
  n =int(the.train*len(rows))
  train = t.clone(rows[:n])
  test  = t.clone(rows[n:])
  rules = learn(train,the)
  judge(test,the,rules)
 
def judge(t,the,rules):
  now=t
  for n,(s,col) in enumerate(rules):
    less = now.clone()
    for x in selected(now.rows,*col): less.add(x)
    if (len(less.rows)  == len(now.rows)):
       break
    if Row(t,now.mid()) < Row(t,less.mid()): 
      break
    if len(less.rows) < 10:  break
    shows(less.y() + [ f"round{n+1}", len(less.rows),col])
    now=less
  
def learn(t, the):
  rows  = sorted(t.rows)
  n     = int(len(rows)**the.tiny)
  bests = rows[:n]
  rests = rows[n:]
  if len(rests) >= n*4:
    gap = int(len(rests) / (n*the.mostrest))
    rests = rests[::gap]
  best, rest= t.clone(bests), t.clone(rests)
  shows(rest.y()        + ["rest", len(rest.rows)])
  shows(best.y()        + ["best", len(best.rows)])
  return sorted(br(best,rest,the), 
                 reverse=True,
                 key=lambda z:z[0])

def shows(lst,r=2):
    lst = [(f"{x:.{r}f}" if isinstance(x,(int,float)) else str(x)) for x in lst]
    print(', '.join(lst))

def br(best,rest,the):
  bins = best.bins(rest,the)
  for (kl,col),b in  bins.items():
    if kl==True:
      b = b/len(best.rows)
      r = bins.get((False,col),0) / len(rest.rows)
      s= b**2/(b+r)
      if b>r :
          yield s,col

def selected(rows, txt,col,span):
  def has(x,lo,hi):
    return x=="?" or (x==lo if lo==hi else lo <= x < hi)
  for row in rows:
    if has(row.cells[col],*span):
      yield row

  # def like(lst,hs,the,goal):
  #   prod  = math.prod
  #   nk    = i.nb if goal else i.nr
  #   prior = (nk + the.k) / (i.n + the.k*2)
  #   fs={}
  #   for text,pos,span in lst:
  #     fs[txt] = fs.get(txt,0) + f.get((goal,(txt,pos,span)), 0)
  #   like = prior
  #   for val in fs.values():
  #     like  *= (val + the.m*prior) / (nk + the.m)
  #   return like
  #
  # best, rest = i.bestRest(t, the, sorted(t.rows))
  # bins = best.bins(rest,the)
  # b,r = len(best.rows), len(rest.rows)
  # i.n, i.nb, i.nr = b+r, len(best.rows), len(rest,rows)
  #
