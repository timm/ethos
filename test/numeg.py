# vim: filetype=python ts=2 sw=2 sts=2 et :
from num  import Num

n=Num(at=0,txt='aa',all=[9,2, 5, 4, 12, 7, 8, 11, 9, 3,
           7, 4, 12, 5, 4, 10, 9, 6,9,4])

assert 7==n.mu
assert 3.06 < n.sd < 3.061

