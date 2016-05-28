#!/bin/bash

for old in ./data/*; do
  new=$(echo $old | perl -pe 's/(\d{4})-(\d{1})-/$1-0$2-/g' | perl -pe 's/(\d{4})-(\d{2})-(\d{1}\W)/$1-$2-0$3/g' | perl -pe 's/-082579f376c26032755c069485ef4663//g')
  mv -v "$old" "$new"
done
