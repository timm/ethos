#!/usr/bin/env bash
o() {  printf "\n#-------\n%% "; echo "$@"; $@; }

o python3 it.py | cat -n > iteg.out

cat iteg.out
