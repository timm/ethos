#!/usr/bin/env bash
Duo=$(cd $( dirname "${BASH_SOURCE[0]}" ) && pwd )

cd $Duo/docs
sh ../o
for i in *ok.py; do
    echo
    echo "---- $g |---------------------------------"
    echo
   python3 $i
done

