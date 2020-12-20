#!/usr/bin/python3

import sys
import time
import random

def main():
    cps = int(sys.argv[1])
    while True:
        scale = ['C', 'bD', 'D', 'bE', 'E', 'F', 'bG', 'G', 'bA', 'A', 'bB', 'B']
        print(random.choice(scale), '\r', end='')
        time.sleep(60/cps)

main()
