```py
from lib import o
from cocomo import F,I

better = o(
    none    = o( goal=F(1)),
    people  = o( goal=F(1),   acap=I(5), pcap=I(5),  pcon=I(5),
                 aexp=I(5),   plex=I(5), ltex=I(5)),
    tools   = o( goal=F(1),
                 time=I(3),   stor=I(3), pvol=I(2),
                 tool=I(5),   site=I(6)),
    precFlex= o( goal=F(1),
                 time=I(5),   flex=I(5)),
    archResl= o( goal=F(1),
                 arch=I(5)),
    slower  = o( goal=F(1),
                 sced=I(5)),
    process = o( goal=F(1),
                 pmat=I(5)),
    less    = o( goal=F(0.5), data=I(2)),
    team    = o( goal=F(1),
                 team=I(5)),
    worst   = o( goal=F(1),
                 rely=I(1),   docu=I(5), 
                 time=I(3),   cplx=I(3))
)

projects = o(
   osp      = o(goal= F(1),
                prec=I(1,2),    flex=I(2,5), arch=I(1,3),
                team=I(2,3),    pmat=I(1,4), stor=I(3,5),
                ruse=I(2,4),    docu=I(2,4), acap=I(2,3),
                pcon=I(2,3),    aexp=I(2,3), ltex=I(2,4),
                tool=I(2,3),    sced=I(1,3), cplx=I(5,6),
                kloc=F(75,125), data=I(3),   pvol=I(2), rely=I(5),
                pcap=I(3),      plex=I(3),   site=I(3))
)

```


