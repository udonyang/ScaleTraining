#!/usr/bin/python3

import sys
import time
import random
import argparse
import datetime

kBase = ['C', 'bD', 'D', 'bE', 'E', 'F', 'bG', 'G', 'bA', 'A', 'bB', 'B']
kInterval = [
        ('union', 1, 0),
        ('m2', 2, 1),
        ('M2', 2, 2),
        ('m3', 3, 3),
        ('M3', 3, 4),
        ('P4', 4, 5),
        ('P5', 5, 6),
        ('m6', 6, 7),
        ('M6', 6, 8),
        ('m7', 7, 9),
        ('M7', 7, 10),
        ('octave', 8, 11),
        ]
kMark = ['+', '*']

def StringTrain(args):
    scale = kBase
    cps = args.cps
    rnd = args.rnd
    print("\n")
    for i in range(0, rnd):
        random.shuffle(scale)
        for note in scale:
            for x in range(0, 15):
                print(kMark[rnd%2], end='')
            print(" ", rnd, ": ", note, '\r', end='')
            time.sleep(60/cps)

    return 0

def MotiveTrain(args):
    random.shuffle(kBase)
    interval = kInterval[0:args.interval]
    gaps = [x for x in range(1, 5)]
    print(kBase[0])
    for r in range(0, args.len):
        random.shuffle(interval)
        random.shuffle(gaps)
        print(interval[0][1], "1/%s"%(2**gaps[0]))
    return 0


def main():
    print(datetime.datetime.now().strftime('%Y%m%d'))
    p = argparse.ArgumentParser()
    p.add_argument('--cps', help='click per second', default=60, type=int);
    p.add_argument('--rnd', help='round', default=60, type=int);
    p.add_argument('--len', help='note number', default=3, type=int);
    p.add_argument('--interval', help='chromatic range', default=11, type=int);
    p.add_argument('--train', help='string|motive', default='string', type=str);
    args = p.parse_args();

    if args.train == 'motive':
        return MotiveTrain(args)
    else:
        return StringTrain(args)

main()
