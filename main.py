#!/usr/bin/python3

import sys
import time
import random
import argparse
import datetime

kNoteInfo = {
        'C': {'abs_pos': 0,
            'blues_harp_pos':1},
        'Db': {'abs_pos': 1,
            'blues_harp_pos':8},
        'D': {'abs_pos': 2,
            'blues_harp_pos':3},
        'Eb': {'abs_pos': 3,
            'blues_harp_pos':10},
        'E': {'abs_pos': 4,
            'blues_harp_pos':5},
        'F': {'abs_pos': 5,
            'blues_harp_pos':12},
        'Gb': {'abs_pos': 6,
            'blues_harp_pos':7},
        'G': {'abs_pos': 7,
            'blues_harp_pos':2},
        'Ab': {'abs_pos': 8,
            'blues_harp_pos':9},
        'A': {'abs_pos': 9,
            'blues_harp_pos':4},
        'Bb': {'abs_pos': 10,
            'blues_harp_pos':11},
        'B': {'abs_pos': 11,
            'blues_harp_pos':6},
        }
kBase = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
kSemi = set(['Db', 'Eb', 'Gb', 'Ab', 'Bb'])
kScale = {}
kScale['Major'] = [2, 2, 1, 2, 2, 2]
kScale['MelodicMinor'] = [2, 1, 2, 2, 2, 2]
kScale['Augment'] = [2, 2, 2, 2, 2]
kScale['DiminishH'] = [2, 1, 2, 1, 2, 1, 2]
kScale['DiminishW'] = [1, 2, 1, 2, 1, 2, 1]
kScale['Pentatonic'] = [2, 2, 3, 2]

kMode = [
        'Ionian'
        , 'Dorian'
        , 'Phrygian'
        , 'Lydian'
        , 'Mixolydian'
        , 'Aeolian'
        , 'Locrian'
        ]
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
    ds = datetime.datetime.now().strftime('%Y%m%d')
    random.shuffle(kBase)
    random.shuffle(kMode)
    interval = kInterval[0:args.interval]
    gaps = [x for x in range(1, 5)]
    motive = ''
    for r in range(0, args.len):
        random.shuffle(interval)
        random.shuffle(gaps)
        motive += str(interval[0][1])
    print('%s,%s,%s,%s'%(ds, kBase[0], kMode[0], motive))
    return 0

def GetInterval(x, y):
    xpos = kNoteInfo[x]['abs_pos']
    ypos = kNoteInfo[y]['abs_pos']
    ret = (len(kBase)+ypos-xpos)%len(kBase)
    if ret > 8:
        ret = len(kBase)-ret
    return ret

def GetColor(scale):
    reg_scale = scale
    if len(scale) < 7:
        reg_scale = scale[0:1]
        for note in scale[1:]+scale[0:1]:
            if GetInterval(reg_scale[-1], note) > 2:
                reg_scale.append('_')
            reg_scale.append(note)
        reg_scale = reg_scale[:-1]
        # print(scale, 'regularize to', reg_scale)

    feat = (
            GetInterval(reg_scale[0], reg_scale[2] if reg_scale[2] != '_' else reg_scale[1]),
            GetInterval(reg_scale[0], reg_scale[4] if reg_scale[4] != '_' else reg_scale[3]),
            )

    # TODO interval to enumerate
    attr = {}
    attr[(2, 7)] = 'sus2'
    attr[(5, 7)] = 'sus4'
    attr[(4, 7)] = 'ma'
    attr[(4, 8)] = 'aug'
    attr[(3, 7)] = 'm'
    attr[(3, 6)] = 'dim'
            
    if feat  in attr:
        return attr[feat]
    # print('undefine color', feat, reg_scale)
    return str(feat)

def BluesHarpScale():
    scales = {}
    for scale_name, intervals in kScale.items():
        for key in range(0, len(kBase)):
            note = key
            scale = [kBase[note]]
            for interval in intervals:
                note = (note+interval)%len(kBase)
                scale.append(kBase[note])
            nsemi = sum([x in kSemi for x in scale])
            if nsemi < 3:
                scales[(scale_name, kNoteInfo[kBase[key]]['blues_harp_pos'], ';'.join(scale))] = nsemi
            else:
                # print('pass', scale_name, scale, nsemi)
                pass

    key_scales = []
    for (scale_name, pos, scale), nsemi in scales.items():
        # print(scale, nsemi)
        seq = scale.split(';')
        for note in seq:
            ind = seq.index(note)
            attr = GetColor(seq[ind:]+seq[:ind])
            key_scales.append((pos, note, attr, nsemi, seq[0]+' '+scale_name, scale))

    print(','.join(['pos', 'key', 'attr', 'hard', 'scale', 'sequence']))
    for key_scale in key_scales:
        print(','.join([str(x) for x in key_scale]))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cps', help='click per second', default=60, type=int);
    p.add_argument('--rnd', help='round', default=60, type=int);
    p.add_argument('--len', help='note number', default=3, type=int);
    p.add_argument('--interval', help='chromatic range', default=11, type=int);
    p.add_argument('--train', default='string', type=str, choices=['motive', 'blues']);
    args = p.parse_args();

    if args.train == 'motive':
        return MotiveTrain(args)
    if args.train == 'blues':
        return BluesHarpScale()
    else:
        return StringTrain(args)

main()
