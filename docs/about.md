# DUO, overview

- [Classes](#classes) 
  - [Storage](#storage) 
  - [Mining](#mining) 
  - [Optimize](#optimize) 
  - [Misc](#misc) 

---------------

##  Classes

### Storage

|  Class               | Super | Notes
|---------------------|---- |-------------------------------------------------------------------------------|
| [Tab](tab.md)       |     | `Tab`les store `Row`s of data                                                 |
| [Row](row.md)       |     | `Rows` hold cells, compute distance and domination between pairs of `Row`s    |
| [Col](col.md)       |     | `Col`s summaries columns of data within `Row`s                                |
| [Num](num.md)       | Col |  `Num`eric columns                                                  |
| [Sym](sym.md)       | Col | `Sym`bolic columns                                                 |

### Mining

| Class               | Super | Notes
|---------------------|-----|-------------------------------------------------------------------------|
| [Div](div.md)       |     | Recursive bi-clustering (using random projections)                            |
| [Why](why.md)       | Div | Generate rules that distinguish between two tables of best and rest examples  |

### Optimize

| Class               | Super | Notes
|---------------------|-------------------------------------------------------------------------------|
| [Best](best.md)     | Div | Ecursive clustering and prune worse half                                |
| [Ranges](ranges.md) |     | Find, then rank, important ranges within numerics. Like a discretizer, but ranges selected by how effective they are  for selecting the preferred class.                           |

### Misc

|  Class               | Super | Notes
|---------------------|-----|-------------------------------------------------------------------------|
| [lib](lib.md)       |     | Misc utils. e.g. unit tests (see [`ok`](lib.html#ok-decorator-for-run-at-load-tests)); pretty prints for classes and dictionaries (see [`dprint`](lib.html#pretty-print-dictionaries) and 
[`Thing`](lib.html#thing-a-class-that-knows-how-to-show-off)), and the reader of [`rows`](lib.html#rows-csv-reader) from a csv file.  |
