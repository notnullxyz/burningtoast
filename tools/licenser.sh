#!/bin/bash

find ../server/ -name "*.py" | while read line; 
do
	sed -i -e '2{x;G};1{h;rlicensehead.txt' -e 'd}' $line
done
