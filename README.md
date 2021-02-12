
# DUO = data miners used / used-by optimizers.

<img align=right src="/etc/img/duo.png">

(c) Tim Menzies    
2021 MIT License     
https://opensource.org/licenses/MIT
<br clear=all>


Sort the data by how much each row dominates over rows.  
Split the sort into 'bad' and 'better'. 
Discretize data, combining any splits that do not 
comment on those splits.  
Count how often ranges appear in 'bad' or 'better'.  
Sort the ranges by how likely they appear in better.  
Build rules by combining different ranges; 
i.e. pick pairs of better ranges, combine them, 
then sort them back into the list.


     :-------:                 explore  = better==bad
     | Ba    | Bad <----.      planning = max(better - bad)
     |    56 |          |      monitor  = max(bad - better)
     :-------:------:   |      tabu     = min(bad + better)
             | B    |   v
             |    5 | Better
             :------:


