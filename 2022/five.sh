#!/bin/bash

sed -r 's/move ([0-9]+) from ([0-9]) to ([0-9])/\1-\2-\3/g' input_05.txt > bla.txt
python five.py
