# Welcome

Data miners and optimizers both explore the landscape of data. Data miners divide things up
into parts and 
optimizers report how to jump between the parts. Used together, each can simplify the other.

Data:

| Component | File                | Class                                                                         |
|-----------|---------------------|-------------------------------------------------------------------------------|
| data      | [Tab](tab.md)       | `Tab`les store `Row`s of data                                                 |
|           | [Row](row.md)       | `Rows` hold cells, compute distance and domination between pairs of `Row`s    |
|           | [Col](col.md)       | `Col`s summaries columns of data within `Row`s                                |
|           | [Num](num.md)       | `Num`eric columns                                                             |
|           | [Sym](sym.md)       | `Sym`bolic columns                                                            |
|-----------|---------------------|-------------------------------------------------------------------------------|
| mine      | [Div](div.md)       | Recursive bi-clustering (using random projections)                            |
|           | [Why](why.md)       | Generate rules that distinguish between two tables of best and rest examples  |
|-----------|---------------------|-------------------------------------------------------------------------------|
| optimize  | [Best](best.md)     | Using `Div`, recursive clustering and prune worse half                        |
|           | [Ranges](ranges.md) | Find, then rank, important ranges within numerics. Like a discretizer, but ranges selected by effectiveness for selecting the preferred class.                           |
|-----------|---------------------|-------------------------------------------------------------------------------|
| misc      | [lib](lib.md)       | Misc utils. e.g. unit tests                                                   |


## Details

### Contact

Tim Menzies,   [timm@ieee.org](mailto:timm@ieee.org),   [http://menzies.us](http://menzies.us)   
![Tim Menzies](https://github.com/timm.png?size=80)

### Citation

T. Menzies,
DUO: data miners using/used-by optimizers,
June 2020,
[https://doi.org/10.5281/zenodo.3921771](https://doi.org/10.5281/zenodo.3921771)


```bibtex
@software{duo2020,
  title        = {DUO: data miners using/used by optimizers},
  Author       = {Tim Menzies},
  month        = jun,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {zenodo},
  doi          = {10.5281/zenodo.3921771},
  url          = {https://doi.org/10.5281/zenodo.3921771}
}
```

### License
BSD 2-Clause License

Copyright &copy; 2020    
Tim Menzies   
All rights reserved

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
