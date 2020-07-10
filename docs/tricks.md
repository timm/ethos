```py
import random,traceback,argparse

def elp(txt,**d):
  for k in d:
    key = k
    val = d[k]
    break
  default = val[0] if isinstance(val,list)  else val
  if val is False :
    return key,dict(help=txt, action="store_true")
  m,t = "S",str
  if isinstance(default,int)  : m,t= "I",int
  if isinstance(default,float): m,t= "F",float
  if isinstance(val,list):
    return key,dict(help=txt, choices=val,          
                    default=default, metavar=m ,type=t)
  return key,dict(help=txt + ("; e.g. %s" % val), 
                 default=default, metavar=m, type=t)

def args(before, after, *lst):
  parser = argparse.ArgumentParser(epilog=after, description = before,
               formatter_class = argparse.RawDescriptionHelpFormatter)
  for key, args in lst:
    parser.add_argument("--"+key,**args)
  return parser.parse_args()

def csv(x=None)
  prep=lambda z: re.sub(r'([\n\t\r ]|#.*)','',z.strip())
  if x:
    with open(x) as f:
      for y in f: 
         z = prep(y)
         if z: yield cols(z.split(","))
  else:
   for y in sys.stdin: 
         z = prep(y)
         if z: yield cols(z.split(","))

def cols(src):
  todo = None
  for cells in src:
    todo = todo or [n for n, cell in enumerate(cells)
                    if not "?"in cell]
    yield [cells[n] for n in todo]
```
```py
def dprint(d, pre="",skip="_"):
  def q(z):
    if isinstance(z,float): return "%5.3f" % z
    if callable(z): return "f(%s)" % z.__name__
    return str(z)
  l = sorted([(k,d[k]) for k in d if k[0] != skip])
  return pre+'{'+", ".join([('%s=%s' % (k,q(v))) 
                             for k,v in l]) +'}'
```

```py
t,f = 0,0
def go(f):
  score = lambda s: f"#TEST {s} passes = {t-f} fails = {f}"
  try:
      t += 1
      print("### ",f.__name__)
      random.seed(SEED)
      f()
      print(score("PASS"),':',f.__name__)
    except Exception:
      f += 1
      print(traceback.format_exc())
      print(score("FAIL"),':',f.__name__)
```
