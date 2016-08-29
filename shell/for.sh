#!/bin/bash

for ((i=1; i<=3; i++))
do
  for ((j=1; j<=3; j++))
  do 
      echo -n "($i, $j)   "
  done
  echo ""
done
