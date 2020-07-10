#!/usr/bin/env bash
Duo=$(cd $( dirname "${BASH_SOURCE[0]}" ) && pwd )

cd $Duo/docs
sh $Duo/u -c
for f in *ok.py; do
    echo
    echo "----| $f |---------------------------------"
    echo
   pypy3 $f
done

