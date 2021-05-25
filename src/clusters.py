# vim: filetype=python ts=2 sw=2 sts=2 et :

class Clusters:
  def __init__(i,t,the):
    i.all=[]
    i.min = len(t.rows)**the.leafs
    i.div(i,rows, t,the)
  
  def div(i,rows,  t,the):
    if len(rows) < 2*i.min:
       i.all += t.clone(rows)
    else:
      one = random.choose(rows)
  

  
 
