```py

_ = 0

ne=   [      [_,_,_,1,2,_], # bad if lohi 
             [_,_,_,_,1,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_]]
nw=  [       [2,1,_,_,_,_], # bad if lolo 
             [1,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_]]
nw4= [       [4,2,1,_,_,_], # very bad if  lolo 
             [2,1,_,_,_,_],
             [1,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_]]
sw4= [       [_,_,_,_,_,_], # very bad if  hilo 
             [_,_,_,_,_,_],
             [1,_,_,_,_,_],
             [2,1,_,_,_,_],
             [4,2,1,_,_,_],
             [_,_,_,_,_,_]]

# bounded by 1..6
ne46= [      [_,_,_,1,2,4], # very bad if lohi
             [_,_,_,_,1,2],
             [_,_,_,_,_,1],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_]]
sw=   [      [_,_,_,_,_,_], # bad if hilo
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [1,_,_,_,_,_],
             [2,1,_,_,_,_]]
sw26= [      [_,_,_,_,_,_], # bad if hilo
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [1,_,_,_,_,_],
             [2,1,_,_,_,_]]
sw46= [      [_,_,_,_,_,_], # very bad if hilo
             [_,_,_,_,_,_],
             [_,_,_,_,_,_],
             [1,_,_,_,_,_],
             [2,1,_,_,_,_],
             [4,2,1,_,_,_]]

rules= dict( 
  cplx= dict(acap=sw46, pcap=sw46, tool=sw46), #12
  ltex= dict(pcap=nw4),  # 4
  pmat= dict(acap=nw,  pcap=sw46), # 6
  pvol= dict(plex=sw), #2
  rely= dict(acap=sw4,  pcap=sw4,  pmat=sw4), # 12
  ruse= dict(aexp=sw46, ltex=sw46),  #8
  sced= dict(
    cplx=ne46, time=ne46, pcap=nw4, aexp=nw4, acap=nw4,  
    plex=nw4, ltex=nw, pmat=nw, rely=ne, pvol=ne, tool=nw), # 34
  stor= dict(acap=sw46, pcap=sw46), #8
  team= dict(aexp=nw,  sced=nw,  site=nw), #6
  time= dict(acap=sw46, pcap=sw46, tool=sw26), #10
  tool= dict(acap=nw,  pcap=nw,  pmat=nw)) # 6

def risk(c):
  r = 0
  for k1,rules1 in rules.items():
    for k2,m in rules1.items():
      x  = int(getattr(c, k1).x)
      y  = int(getattr(c, k2).x)
      print(k1,x,k2,y)
      r += m[x][r]
  return r
```
