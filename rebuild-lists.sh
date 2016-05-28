#!/bin/bash

source ./env/bin/activate

for old in ./data/*.html; do
  new=$(echo $old | sed -E 's/.*\/(.*).html/\1/')
  python getFaces.py --save --date $new
done

deactivate
