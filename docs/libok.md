
```py
from lib import ok,src,rows,cols,dprint

@ok
def ok1():
  "always no. tests the test engine"
  assert 1==2,'well that is a complete surprise'

@ok
def ok2():
  x=4/2
  assert x==2

@ok
def source1():
  s="""a ,  b,  c
       23, 31, 20
       40, 32, 90
    """
  for c in source(s):
    print(c)

@ok
def rows1():
  for line in cols(rows(src("data/weather4.csv"))):
    assert isinstance(line,list) 
    assert len(line) == 4

@ok
def dprint1():
   print(dprint(dict(x=1,y=dict(k=10,bb=23),c=2)))
```
