from random import seed as seed
from random import random as _r
import re,math

#------------------- ------------------- ------------------- ------------------
class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return "{"+ ', '.join(
      [f":{k} {v}" for k, v in sorted(i.__dict__.items()) 
       if not callable(v) and k[0] != "_"])+"}"

def _of(i, methods):
  def of1(i, f): return lambda *l, **d: f(i, *l, **d)
  for k in methods:
    i.__dict__[k] = of1(i, methods[k])
  return i

THE = o(seed=1, skip="?", cohen=.3, id=0, 
        less="<",more=">",path="data",file="auto93.csv",
        Xchop=.5, best=.8, sep=",", ignore=r'([\n\t\r ]|#.*)')

def Counts(): return o(f={}, h={})

def Row(): 
  def tag(i,t): [i.cells[col.pos] for col in t.cols.y]
  return _of(o(cells=[], n=0, _tag=False), locals())

def Tbl(): 
  def ready(i): return i.cols.all
  return _of(o(cols=Cols(), rows=[]), locals())

def Cols(): 
  def add(i,pos,txt):
    if   THE.skip in txt                                       : f = Skip
    elif THE.less in txt or THE.more in txt or txt[0].isupper(): f = Num
    else                                                       : f = Sym
    now = f(txt=txt, pos=pos, w=THE.less in txt)
    i.all += [now]
    if THE.skip not in txt:
      (i.y if THE.less in txt or THE.more in txt else i.x).append(now)
  return _of(o(all=[], y=[], x=[]),locals())

def Span(x,y):
  def _has(i,x,y): return i.down <= x <i.up
  return _of(o(down=x,up=y),locals())

def Skip(pos=0, txt="", w=0): 
  def add(i,x): return x
  return _of(o(pos=pos, txt=txt, w=w, n=0), locals())

def Sym(pos=0,txt="",w=1):
  def ent(i)    : return -sum(v/i.n*math.log(v/i.n,2) for v in i.seen.values())
  def div(i)    : return list(i.seen.keys())
  def add(i,x)  : 
    now = i.seen[x] = i.seen.get(x, 0) + 1
    if now > i.most: i.most, i.mode = now, x
  return _of(o(pos=pos,txt=txt,w=w,n=0,seen={},most=0,mode=None), locals())

def Num(pos=0,txt="",w=1):
  def add(i, x) : i._all += [x]; i.ok = False
  def mid(i)    : n,a= i.all(); return a[int(.5 * n)]
  def var(i)    : n,a= i.all(); return (a[int(.9 * n)] - a[int(.1 * n)]) / 2.56
  def norm(i,x) : _,a= i.all(); return (x-a[0])/(a[-1]-a[0])
  def all(i)    : 
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  def width(i): 
    n = len(i._all)**THE.Xchop
    while n < 4 and n < len(xy) / 2: n *= 1.2
    return int(n)
  def div(i):
    n,a          = i.all()
    width, sd    = i.width(), i.var()
    now, x0, out = width, a[0], []
    while now < n - width:
      now += 1
      x1, x2 = a[now], a[now+1]
      if x1 != x2 and x1 - x0 > sd*THE.cohen:
        out += [Span(x0,x1)]
        x0   = x1
        now += width
    out[-1].up =  math.inf
    out[ 0].down = -math.inf
    return out
  return _of(o(pos=pos, txt=txt, w=w, _all=[], ok=True, n=0), locals())

def _add(i,x):
  if x != THE.skip:
    i.n += 1
    i.add(x)
  return x

def table(src):
  t = Tbl()
  for row in src:
    if t.ready(): t.rows += [ _add(col, x) for col,x in zip(t.cols.all,row)]
    else        : [ t.cols.add(pos, txt) for pos,txt in enumerate(row) ]
  return t

def counts(rows, 
           ranges,# ranges.keys() = colNumberss; ranges[key]=list of Spans, 
           fy=lambda z:z.tag):
  
seed(THE.seed)
n=Num()
for _ in range(10000): _add(n,int(1000*_r()))
print(n.mid())

#print(n.var(), n.mid())
print(n.div())

def _csv(file):
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
      yield [atom(x) for x in re.sub(THE.ignore, '', a).split(THE.sep)]

t=table(_csv(THE.path + "/" + THE.file))
for n,col in enumerate(t.cols.x):
  print("\n",n,col.div())
