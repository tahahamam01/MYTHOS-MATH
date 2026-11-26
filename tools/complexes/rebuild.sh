#!/bin/bash
# rebuild the chapter from the md sources into /home/claude/tahahamam01/mythos-math
set -e
R=/home/claude/tahahamam01/mythos-math; SC=/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad
cd $R/tools/complexes
python3 -I build.py 2>&1 | head -4
python3 -I inject.py /home/claude/work/index.orig.html $R $SC/cx_block.js "/home/claude/site/complex assets"
python3 -I make_test.py $R/index.html /home/claude/work/test/index_test.html
