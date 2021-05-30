# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, Tim Menzies (timm@ieee.org) unlicense.org
"""About this  code.
This code finds
structures in the data. Them,
 contrast set learners
are used to report how the  structures  differ.
This process recurse on the better half of the data.

Much recent angst about it being hard to undestand AI softare. cncerns
of not udnerstanding what is going on.

well wht about rewriing that sftwre, starting with undestandability
as a  primary design construct then going  on to see what  can be 
obtained?

counter argument: imnporssible. AI inehrently complex with acrance
intermal mechaisms that will forvery pzzle us. deep elarning

and that might be true for certain kinds of software (10000 wavelets, DL).
but is that kind  of application the  minority, or majoirty case,
for SE? and if it is the  minority case, what can be acheived
for all the  other kinds of software?

evidence that se for ai is different

designing for understandability: the S-model.

The best  software engineers  do not apply AI verbatim
to their problems.
AI tools containing many  choices
and  good software engineers
know to refactor that  code in order  to make it
easy to maintain and explain. 
See box1: AI needs to be adapted for AI

Mores epcifially, ethics

AI for SE is different. Firstly, while other  communities
might accept AI tools as black-box packages, SE people
know that AI software is  software and that,  as such,
it  needs engineers that  can reach inside it  and refactor it as required.
Those engineers work best when they  understand the  code they are changing.
Hence, SE people most need AI  tools they can  comprehend.

Secondly, Software  engineers are the people that fix things
that annoy users. Hence, when users feel they cannot understand  how  AI
tools make conclusions, then they will demand that  software engineers
fix the problem.  

appiied to and  constrast set learnes 
unsupervised: much to be gained by
reasoning over the structure of the data,
even before humans have added labels to parts of that
data.

That  reasoning actually reduces the need
for  labeling  and, done properly, offers 
a range of  important services such as
explanation, active learning, classification,
optimization.

Historically, this work  began with  the notions
of `keys`:

Frm 2006 to 2021, 9 phd students accept the  keys
premise and applied it to  various domains

classfication:

- Tar3 Menzies

optimzation:

-   Tars, Gay: keys, Mitlon, which, krall, + checn otpionat

test case generation:
- chen, snap

privact
- Fayola; reduction, privacy

Expanation:
- Motta: 

taken  together, these seem to be a new kind
of AI  software-- or more accurately,  a  
useful refactoring of a large set of ideas
that are normally treated as seperate subjects.
this 

putting them all together, we  are looking
at some way  to refactor all the  above into
a  class library that 
lets  programmeris mix and match  the above
techniques,  as required.  the  results  have been
surprising: initally, we were targetting
an "iceburg" design  where
all the  above tools where seperate entities
linked  by some 
high-level API,  instead we  seem to be ehading
towards "soup"  where all the  above  have  been
melted  down and refactored into tiny parts
that flow together are 
at some lower level.

the mental model  that  drives this  new formulation
is  "S-growth". When tinkering  with some devide,
humans decide to try this or that. 
Some of those decisions  effective
and performance improves. And after a  while,
further  decisions are seen not to help matters--
at which point, new decisions stop and the design 
freezes

```
performance ^
            |           ..............
            |        ../
            |       /
            |    ../
            |.../
            .----------------------------> decisions
             1    5    10    15   20
```

"""
