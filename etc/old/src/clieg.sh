#!/usr/bin/env bash
o() {  printf "\n#-------\n%% "; echo "$@"; $@; }
f=cli
(
o python3 $f.py -h
o python3 $f.py
o python3 $f.py -w vic
o python3 $f.py -s 1000 
) | cat -n > ${f}eg.out

cat ${f}eg.out
