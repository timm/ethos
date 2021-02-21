#!/usr/bin/env bash

python3 fastmap.py > /tmp/$$

cat <<EOF|gnuplot
unset key
set terminal pngcairo
set output '/tmp/fmeg.png'
plot '/tmp/$$' using 1:2:3 with points pt 11 ps 2 palette
EOF
open /tmp/fmeg.png
