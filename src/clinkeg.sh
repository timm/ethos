#!/usr/bin/env bash
o() {  printf "\n#-------\n%% "; echo "$@"; $@; }

(
o python3 clink.py -h
o python3 clink.py
o python3 clink.py -w vic
o python3 clink.py -s 1000 
) | cat -n > clinkeg.out

cat clinkeg.out
