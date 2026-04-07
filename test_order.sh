#!/bin/bash

for i in $(seq 30 40)
do
	clear && python3 starter.py gjp-$i
	sleep 5s
done
