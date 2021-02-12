
Manage tables of data.`Cols` summarize each column.
(c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.

Converts a list of cells into rows, summarized in columns. Row1
name describes each column.
Names with '>' and '<' are goals to maximize or minimize (respectively). For example, in
the following, we want to minimize weight (lbs) while maximizing acceleration (acc)
and miles per gallon (mpg).

    cylinders,displ,hp,<lbs,>acc,model,origin,>mpg

For example, after reading weather.csv,
then `.cols` would have entries like the following (and note that
the first is for a symbolic column and the second is for a numeric):

```
    {'outlook' :  {
            'has': # 'has' for symbolic is a dictionary
                   {'sunny': 5, 'overcast': 4, 'rainy': 5},
            'n'  : 14,
            'pos': 0,
            'txt': '_outlook',
             'w' : 1}
     '<temp'   :   {
            'has': # 'has' for  numerics is a list
                   [64, 85], # min and max value seen in this columnm
            'n'  : 14,
            'pos': 1,
            'txt': '<temp'}
    etc }
```

Tables also collect rows with a 'score' (how often that row
dominates 'rowsamples' other rows) and 'klass' which is often often
that score is better than 'best'. e.g. if 'best'=0.5 then 'klass' is
true if this row 'scores' better than half the others; e.g. from
../data/auto93.csv, here are the first and last four rows sorted by
'score'. Observe that we want to minimize lbs and maximize acc and mpg.
Hence, in the last rows, lbs is lower and acc and mpg is larger:

    score  klass  cylin   displ   hp  <lbs  >acc   model   origin  >mpg
    -----  ------ ------- ------- ---  ----  ----  ------  -------  -----
    0.0    False  8       400     175  5140  12    71      1        10
    0.0    False  8       440     215  4735  11    73      1        10
    0.0    False  8       454     220  4354  9     70      1        10
    0.0    False  8       455     225  4425  10    70      1        10
    0.0    False  8       455     225  4951  11    73      1        10
    -----  ------ ------- ------- ---  ----  ----  ------  -------  -----
    0.98   True   4       91      60   1800  16.4  78      3        40
    0.98   True   4       97      46   1835  20.5  70      2        30
    1.0    True   4       85      '?'  1835  17.3  80      2        40
    1.0    True   4       86      65   2110  17.9  80      3        50
    1.0    True   4       97      52   2130  24.6  82      2        40

Also note that the 'klass' is 'True' for the better half and 'False'
otherwise.


```python

import math
from lib import csv, numsp, symsp, o, isa

def table(src):
  def Tbl(rows=[]): return o(cols={}, x={}, y={}, rows=rows)
  def Row(cells=[]): return o(cells=cells, score=0, klass=True)

  def Col(txt='', pos=0, w=1):
    return o(n=0, txt=txt, pos=pos, has=None, spans=[],
             w=-1 if "<" in txt else 1)

  def head(tbl, x):
    for pos, txt in enumerate(x):
      if not "?" in txt:
        tbl.cols[txt] = tmp = Col(txt, pos)
        if "<" in txt or ">" in txt or "!" in txt:
          tbl.y[txt] = tmp
        else:
          tbl.x[txt] = tmp

  def body(tbl, x):
    def inc(col, x):
      if col.has is None:
        col.has = [math.inf, -
                   math.inf] if isa(x, (float, int)) else {}
        return inc(col, x)
      col.n += 1
      if symsp(col.has):
        col.has[x] = col.has.get(x, 0) + 1
      else:
        if x > col.has[1]:
          col.has[1] = x
        if x < col.has[0]:
          col.has[0] = x
    [inc(c, x[c.pos]) for c in tbl.cols.values() if x[c.pos] != "?"]
    tbl.rows += [Row(x)]

  def footer(tbl):
    for col in tbl.cols.values():
      if numsp(col.has):
        col.has.sort()
  ##########################
  tbl = Tbl()
  for x in src:
    (body if len(tbl.cols) else head)(tbl, x)
  footer(tbl)
  return tbl
```
