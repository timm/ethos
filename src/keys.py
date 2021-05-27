# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib  import obj,rs
import sys

def keys(t,the):
  rows  = sorted(t.rows)
  n     = int(len(rows)**the.tiny)
  bests = rows[:n]
  rests = rows[n:]
  if len(rests) >= n*4:
    gap = int(len(rests) / (n*the.mostrest))
    rests = rests[::gap]
  best, rest= t.clone(bests), t.clone(rests)
  maybe = sorted(br(best,rest,the), 
                 reverse=True,
                 key=lambda z:z[0])
  t1 = t.clone()
  print("best",rs(rows[0].y(),1))
  print("mid",rs(t.y(),1))
  print("rest",rs(rows[-1].y(),1))
  for _,col in maybe:
    for x in selects(bests,*col): t1.add(x)
    for x in selects(rests,*col): t1.add(x)
    print(rs(t1.y(),1))

def br(best,rest,the):
  bins = best.bins(rest,the)
  for (kl,col),b in  bins.items():
    if kl==True:
      b = b/len(best.rows)
      r = bins.get((False,col),0) / len(rest.rows)
      if b>r:
        yield b**2/(b+r),col

def selects(rows, txt,col,span):
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
