#!/usr/bin/env bash

python3 fastmap.py > /tmp/$$

cat <<EOF|gnuplot
unset key
#set palette defined ( 0 "red", 0.5 "white", 1 "blue" )



set palette defined ( .1 "#7f0000",\
                      .2 "#ee0000",\
                      .3 "#ff7000",\
                      .4 "#ffee00",\
                      .5 "#90ff70",\
                      .6 "#0fffee",\
                      .7 "#0090ff",\
                      .8 "#000fff",\
                      .9 "#000090")






set terminal pngcairo
set output '/tmp/fmeg.png'
plot '/tmp/$$' using 1:2:3 with points pt 11 ps 2 palette
EOF
open /tmp/fmeg.png
