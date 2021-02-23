#!/usr/bin/python3

import sys
import time
import random

def main():
    MARK = ['+', '*']

    cps = int(sys.argv[1])
    rnd = int(sys.argv[2])
    print("\n")
    for i in range(0, rnd):
        scale = ['C', 'bD', 'D', 'bE', 'E', 'F', 'bG', 'G', 'bA', 'A', 'bB', 'B']
        random.shuffle(scale)
        for note in scale:
            for x in range(0, 15):
                print(MARK[rnd%2], end='')
            print(" ", rnd, ": ", note, '\r', end='')
            time.sleep(60/cps)

main()
