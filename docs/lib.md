# Lib

- [Class Magic](#class-magic) 
  - [Thing](#thing-a-class-that-knows-how-to-show-off)  : a class that knows how to show off
  - [Simple Structs](#simple-structs) 
- [Lists](#lists) 
  - [Multiple Members](#multiple-members) 
  - [Within](#within) 
- [Dictionaries](#dictionaries) 
  - [Pretty print dictionaries](#pretty-print-dictionaries) 
- [Input](#input) 
  - [Src](#src-read-from-strings-or-file-or-lists-or-zip-files-or-standard-input)  : read from strings or file or lists or zip files or standard input
  - [Rows](#rows-csv-reader)  : csv reader
  - [Cols](#cols-trick-for-skipping-columns)  : trick for skipping columns
- [Error handling](#error-handling) 
- [Unit test tool](#unit-test-tool) 
  - [ok](#ok-decorator-for-run-at-load-tests)  : decorator for "run-at-load" tests
  - [excursion](#excursion-save-state-of-classes--reset-after-test)  : save state of classes , reset after test

---------------

---------------

```py
import sys,random
from zipfile import ZipFile
from contextlib import contextmanager
```

## Class Magic
### Thing: a class that knows how to show off
```py
class Thing:
  def __repr__(i):
    return dprint(i.__dict__, 
                  i.__class__.__name__)
```
### Simple Structs

```py
class o(Thing):
  def __init__(i,**d)    : i.__dict__.update(**d)
  def __getitem__(i,k)  : return i.__dict__[k]
  def __setitem__(i,k,v): i.__dict__[k] = v
  def __iter__(i): 
    for k in i.__dict__: yield k
```

## Maths
### prod
```py
def prod(lst):
  y = 1
  for x in lst: y = y*x
  return y
 
```
## Lists
### Multiple Members
```py
def ins(lst,x):
  for y in lst:
    if y in x: return True
```

### Within 
```py
def within(x,y,z):
  return y>= x and y <= z
```

## Dictionaries
### Pretty print dictionaries
Show keys in sorted order, don't show 
hidden fields (those starting with "\_").

```py
def dprint(d, pre="",no="_"):
  def q(z):
    if isinstance(z,float): return "%5.3f" % z
    if callable(z): return "f(%s)" % z.__name__
    return str(z)
  l = sorted([(k,d[k]) for k in d if k[0] != no])
  return pre+'{'+", ".join([('%s=%s' % (k,q(v))) 
                             for k,v in l]) +'}'
```
### Cache

```py
class Cache(Thing):
   def __init__(i, **funs):
     i.cache={}
     i.funs = funs
   def __getattr__(self, name):
     def _missing(k):
       if not k in i.cache:
         i.cache[k] = i.funs[k](i)
       return i.cache[k]
     return _missing
```

## Input 
### Src: read from strings or file or lists or zip files or standard input

```py
def src(x=None):
  def items(z):
    for y in z: yield y
  def strings(z):
    for y in z.splitlines(): yield y.strip()
  def csv(z):
    with open(z) as fp:
      for y in fp: yield y.strip()
  def stdin(z):
    for y in sys.stdin: yield y.string()
  def zip(z):
    x = x.split("/",1)
    with ZipFile(x[0]) as zf:
      with zf.open(x[1]) as fp:
        for y in fp: yield y.strip()
  if   not x                 : f = stdio
  elif not isinstance(x,str) : f = items
  elif x[-3:]=='zip'         : f = zip
  elif x[-3:]=='csv'         : f = csv
  else                       : f = strings
  for y in f(x): yield y
```
### Rows: csv reader
Convert lines into lists, killing whitespace
and comments. skip over lines of the wrong size.

```py
def rows(src):
  linesize = None
  for n, line in enumerate(src):
    line = re.sub(r'([\n\t\r ]|#.*)','', line.strip())
    if line:
      line = line.split(",")
      if linesize is None:
        linesize = len(line)
      if len(line) == linesize:
        yield line
      else:
        now(False, "E> skipping line %s" % n)
```

### Cols: trick for skipping columns
Skip over any column whose name contains "?".
```py
def cols(src):
  todo = None
  for cells in src:
    todo = todo or [n for n, cell in enumerate(cells)
                    if not "?"in cell]
    yield [cells[n] for n in todo]
```
##  Error handling
```py
def now(t,m):
  if not t:
    sys.stderr.write('#E> '+str(m)+'\n')
    sys.exit()
```

## Unit test tool
### ok: decorator for "run-at-load" tests
```py
import traceback,re

SEED = 1
class ok:
  tries,fails = 0,0  #  tracks the record so far
  def __init__(i,fun=None):
    def score(txt):
      t,f = ok.tries, ok.fails
      return f"#TEST {txt} passes = {t-f} fails = {f}"
    if not fun:     
      return print(score("STATUS"))
    try:
      ok.tries += 1
      print("### ",fun.__name__)
      random.seed(SEED)
      fun()
      print(score("PASS"),':',fun.__name__)
    except Exception:
      ok.fails += 1
      print(ok.fails,ok.tries)
      import traceback
      print(traceback.format_exc())
      print(score("FAIL"),':',fun.__name__)
```
### excursion: save state of classes , reset after test
```py
@contextmanager
def excursion(*l):
  def state():
    for x in l:
      for k in dir(x):
        if k[:2] != "__":
          if not callable(getattr(x,k)):
            yield x,k, getattr(x,k)
  b4 = [s for s in state()]
  yield
  for x,k,v in b4: 
    setattr(x,k,v)
```

