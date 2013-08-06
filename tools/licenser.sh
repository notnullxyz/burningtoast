#!/bin/bash

x="This file is part of BurningToast, Copyright 2013 Marlon van der Linde.

    BurningToast is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version. Please see the included COPYING
	file or http://www.gnu.org/licenses/gpl.txt for more information
"

find . -name "*.py" | while read line; 
do 
	sed -i '1s/^/$x\n/' CREDITS	
done

