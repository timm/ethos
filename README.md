# DUO = data miners used / used-by optimizers

[install](#install) ::
[license](#license)  ::
doc [it](http://menzies.us/it)  ::
    [clink](http://menzies.us/clink)  ::
    [tab](http://menzies.us/tab) 

(c) Tim Menzies    
2021 MIT License     
https://opensource.org/licenses/MIT

Sort the data by how much each row dominates over rows.  Split the
sort into 'bad' and 'better'.  Discretize data, combining any splits
that do not comment on those splits.  Count how often ranges appear
in 'bad' or 'better'.  Sort the ranges by how likely they appear
in better.  Build rules by combining different ranges; i.e. pick
pairs of better ranges, combine them, then sort them back into the
list.


     :-------:                 explore  = better==bad
     | Ba    | Bad <----.      planning = max(better - bad)
     |    56 |          |      monitor  = max(bad - better)
     :-------:------:   |      tabu     = min(bad + better)
             | B    |   v
             |    5 | Better
             :------:

# Install

Download, cd into src. 

    chmod +x duo.py
    ./duo.py

# License

Copyright (c) 2021 Tim Menzies 

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

