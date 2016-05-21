#!/bin/bash

files=`find ./data -type f | grep "[0-9]/"`

# should also check for Levi's name which should be unique
# files=`find ./data -type f -exec grep "Levi" {} \; | grep "[0-9]/"`

for file in $files;
do
  date=`echo "$file" | sed -E 's/.*\/([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{6}).*/\1-\2-\3-\1\2\3\4.lst/'`
  cp $file "../data/$date"
  echo "$file $date"
done
