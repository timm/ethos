# DUO = data miners used / used-by optimizers.
# (c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.
from random import seed as seed
from random import random as _r
import re,math

class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return "{"+ ', '.join(
      [f":{k} {v}" for k, v in sorted(i.__dict__.items()) 
       if  not callable(v) and k[0] != "_"])+"}"

def _of(i, methods):
  def of1(i, f): return lambda *l, **d: f(i, *l, **d)
  for k in methods: i.__dict__[k] = of1(i, methods[k])
  return i

THE = o(seed=1, skip="?", cohen=.3, id=0, 
        less="<",more=">",path="data",file="auto93.csv",
        Xchop=.5, best=.8, sep=",", ignore=r'([\n\t\r ]|#.*)')

def Counts(): return o(f={}, h={})

def Row(cells=[]): 
  def score(i,t): 
    print(">>>>",t.cols.y[0])
    i.n = i.n if i.n else sum(c.norm(i.cells[c.pos]) for c in t.cols.y)
  return _of(o(cells=cells, n=0, _tag=False), locals())

def Tbl(): 
  def ready(i): return i.cols.all
  return _of(o(cols=Cols(), rows=[]), locals())

def Cols(): 
  def add(i,pos,txt):
    if   THE.skip in txt                                       : f = Skip
    elif THE.less in txt or THE.more in txt or txt[0].isupper(): f = Num
    else                                                       : f = Sym
    now = f(pos, txt, -1 if THE.less in txt else 1)
    i.all += [now]
    if THE.skip not in txt:
      (i.y if THE.less in txt or THE.more in txt else i.x).append(now)
    return now
  return _of(o(all=[], y=[], x=[]),locals())

def Span(x,y):
  def _has(i,x,y): return i.down <= x <i.up
  return _of(o(down=x,up=y),locals())

def Skip(place=0,text="",weight=1):
  def add(i,x): return x
  return _of(o(pos=place, txt=text, w=weight, n=0), locals())

def Sym(place=0,text="",weight=1):
  def ent(i)  : return -sum(v/i.n*math.log(v/i.n,2) for v in i.seen.values())
  def div(i)  : return list(i.seen.keys())
  def add(i,x): 
    now = i.seen[x] = i.seen.get(x, 0) + 1
    if now > i.most: i.most, i.mode = now, x
  return _of(o(pos=place,txt=text,w=weight,n=0,seen={},most=0,mode=None), 
            locals())

def Num(place=0,text="",weight=1):
  def add(i, x): i._all += [x]; i.ok = False
  def mid(i)   : n,a = i.all(); return a[int(n/2)]
  def var(i)   : n,a = i.all(); return (a[int(.9*n)] - a[int(n/10)]) / 2.56
  def norm(i,x): 
    _,a = i.all() 
    tmp = (x - a[0]) / (a[-1] - a[0])
    return tmp if i.w>0 else 1 - tmp
  def all(i)   : 
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
  return _of(o(pos=place, txt=text, w=weight, _all=[], ok=True, n=0), locals())

def _add(i,x):
  if x != THE.skip:
    i.n += 1
    i.add(x)
  return x

def table(src):
  t = Tbl()
  for row in src:
    if t.ready(): t.rows += [Row([_add(c, x) for c,x in zip(t.cols.all,row)])]
    else        : [ t.cols.add(pos, txt) for pos,txt in enumerate(row) ]
  return t


seed(THE.seed)
n=Num()
for _ in range(10000): _add(n,int(1000*_r()))
#print(n.mid())

#print(n.var(), n.mid())
#print(n.div())

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
#for row in t.rows: print(row)
#for n,col in enumerate(t.cols.x): print("\n",n,col.div())
#print(sorted((row.score(t) for row in t.rows)))

print(t.cols.y[0].norm(3000))
#rows[0].score(t)
