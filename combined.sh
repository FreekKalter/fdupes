#!/bin/bash
./fdupes --recurse --size --sameline /data/bad /data/archives | tee log.txt && python3 parse.py
