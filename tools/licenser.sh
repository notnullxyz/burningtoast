#!/bin/bash

##
## YOU WILL BE WARNED
##
## This script is harsh, I used it for the initial run. It does not check if files
## have already been prepended, and when they are empty, sed doesn't work...
## If you want to use this, make it better first. 
## Preferably, just add licensehead.txt to all source files, by hand
##
## YOU HAVE BEEN WARNED
##

find ../server/ -name "*.py" | while read line; 
do
	sed -i -e '2{x;G};1{h;rlicensehead.txt' -e 'd}' $line
done
