#!/bin/bash

for i in $(seq 30 40)
do
	python3 starter.py gjp-$i
	printf "\n"
	sleep 5s
done
