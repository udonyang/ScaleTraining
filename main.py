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

kGapInfo = {
        'union': {'cat': 1,
            'abs_gap': 0,
            'deg': 'I',
            },

        'm2': {'cat': 2,
            'abs_gap': 1,
            'deg': 'bII',
            },

        'M2': {'cat': 2,
            'abs_gap': 2,
            'deg': 'II',
            },

        'm3': {'cat': 3,
            'abs_gap': 3,
            'deg': 'bIII',
            },

        'M3': {'cat': 3,
            'abs_gap': 4,
            'deg': 'III',
            },

        'P4': {'cat': 4,
            'abs_gap': 5,
            'deg': 'IV',
            },

        'D5': {'cat': 4,
            'abs_gap': 6,
            'deg': 'bV',
            },

        'P5': {'cat': 5,
            'abs_gap': 7,
            'deg': 'V',
            },

        'm6': {'cat': 6,
            'abs_gap': 8,
            'deg': 'bVI',
            },

        'M6': {'cat': 6,
            'abs_gap': 9,
            'deg': 'VI',
            },

        'm7': {'cat': 7,
                'abs_gap': 10,
                'deg': 'bVII',
                },

        'M7': {'cat': 7,
                'abs_gap': 11,
                'deg': 'VII',
                },

        'octave': {'cat': 8,
                'abs_gap': 12,
                'deg': 'I',
                },
        }

kChordInfo = {
        'ma': {
            'family': 'major',
            'seq': ['M3', 'P5'],
            },
        'ma7': {
            'family': 'major',
            'seq': ['M3', 'P5', 'M7'],
            },
        'm': {
            'family': 'minor',
            'seq': ['m3', 'P5'],
            },
        'm7': {
            'family': 'minor',
            'seq': ['m3', 'P5', 'm7'],
            },
        'm7': {
            'family': 'minor',
            'seq': ['m3', 'P5', 'M7'],
            },
        '7': {
            'family': 'dominate',
            'seq': ['M3', 'P5', 'm7'],
            },
        'dim': {
            'family': 'dominate',
            'seq': ['m3', 'D5'],
            },
        'm7b5': {
            'family': 'dominate',
            'seq': ['m3', 'D5', 'm7'],
            },
        'dim6': {
            'family': 'dominate',
            'seq': ['m3', 'D5', 'M6'],
            },
        'aug': {
            'family': 'dominate',
            'seq': ['M3', 'm6'],
            },
        }

kProgInfo = [
        {
            'seq': [('M2', 'm'), ('P5', 'ma')],
            },
        {
            'seq': [('M2', 'dim'), ('P5', 'm')],
            },
        {
            'seq': [('M2', 'm7'), ('P5', '7')],
            },
        {
            'seq': [('union', 'ma7'), ('M6', 'm7'), ('M2', 'm7'), ('P5', '7')],
            },
        {
            'seq': [('union', 'ma'), ('M6', 'm'), ('M2', 'm'), ('P5', 'ma')],
            },
        {
            'seq': [('M2', 'm7'), ('P5', '7')],
            },
        {
            'seq': [('M2', 'm7'), ('P5', '7')],
            },
        {
            'seq': [('union', 'ma7'), ('M6', 'm7')],
            },
        {
            'seq': [('union', 'ma7'), ('P4', 'ma7')],
            },
        ]
def GetProgName(proginfo):
    return ' '.join([kGapInfo[gap]['deg']+chord for gap, chord in proginfo['seq']])

kBase = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
kSemi = set(['Db', 'Eb', 'Gb', 'Ab', 'Bb'])
kScale = {}
kScale['Major'] = ['M2', 'M2', 'm2', 'M2', 'M2', 'M2']
kScale['HarmonicMinor'] = ['M2', 'm2', 'M2', 'M2', 'm2', 'm3']
kScale['MelodicMinor'] = ['M2', 'm2', 'M2', 'M2', 'M2', 'M2']
kScale['Augment'] = ['M2', 'M2', 'M2', 'M2', 'M2']
kScale['DiminishH'] = ['M2', 'm2', 'M2', 'm2', 'M2', 'm2', 'M2']
kScale['DiminishW'] = ['m2', 'M2', 'm2', 'M2', 'm2', 'M2', 'm2']
kScale['Pentatonic'] = ['M2', 'M2', 'm3', 'M2']

def ShiftNote(key, gap):
    return kBase[(kNoteInfo[key]['abs_pos']+kGapInfo[gap]['abs_gap'])%len(kBase)]

def GetScaleSeq(scale):
    return [kGapInfo[gap]['abs_gap'] for gap in scale]

def GetChordSeq(key, chordinfo):
    ret = [key]
    for gap in chordinfo['seq']:
        ret.append(ShiftNote(key, gap))
    return ret

kMode = [
        'Ionian'
        , 'Dorian'
        , 'Phrygian'
        , 'Lydian'
        , 'Mixolydian'
        , 'Aeolian'
        , 'Locrian'
        ]

kGap = [
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
    interval = kGap[0:args.interval]
    gaps = [x for x in range(1, 5)]
    motive = ''
    for r in range(0, args.len):
        random.shuffle(interval)
        random.shuffle(gaps)
        motive += str(interval[0][1])
    print('%s,%s,%s,%s'%(ds, kBase[0], kMode[0], motive))
    return 0

def GetGap(x, y):
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
            if GetGap(reg_scale[-1], note) > 2:
                reg_scale.append('_')
            reg_scale.append(note)
        reg_scale = reg_scale[:-1]
        # print(scale, 'regularize to', reg_scale)

    feat = (
            GetGap(reg_scale[0], reg_scale[2] if reg_scale[2] != '_' else reg_scale[1]),
            GetGap(reg_scale[0], reg_scale[4] if reg_scale[4] != '_' else reg_scale[3]),
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
    return str(feat).replace(',', ' ')

def GetNsemi(seq):
    return sum([x in kSemi for x in seq])

def MatchBluesHarp(seq):
    return GetNsemi(seq) < 3

def GetTupleCsv(t):
    return ','.join([str(x) for x in t])

def BluesHarpScale():
    scales = {}
    for scale_name, intervals in kScale.items():
        for key in range(0, len(kBase)):
            note = key
            scale = [kBase[note]]
            for interval in GetScaleSeq(intervals):
                note = (note+interval)%len(kBase)
                scale.append(kBase[note])
            nsemi = sum([x in kSemi for x in scale])
            if nsemi < 3:
                scales[(scale_name, kNoteInfo[kBase[key]]['blues_harp_pos'], ' '.join(scale))] = nsemi
            else:
                # print('pass', scale_name, scale, nsemi)
                pass

    key_scales = []
    for (scale_name, pos, scale), nsemi in scales.items():
        # print(scale, nsemi)
        seq = scale.split(' ')
        for note in seq:
            ind = seq.index(note)
            attr = GetColor(seq[ind:]+seq[:ind])
            key_scales.append((pos, note, attr, nsemi, seq[0], scale_name, scale))

    print(','.join(['position', 'key', 'attr', 'hard', 'position_key', 'scale', 'sequence']))
    for key_scale in key_scales:
        print(GetTupleCsv(key_scales))

def BluesHarpChord():
    chord_seqs = set()
    for key, keyinfo  in kNoteInfo.items():
        for chord, chordinfo in kChordInfo.items():
            seq = GetChordSeq(key, chordinfo)
            if GetNsemi(seq) < 3:
                chord_seqs.add((key, chord, ' '.join(seq)))

    print(','.join(['key', 'attr', 'seq']))
    for chord_seq in chord_seqs:
        print(GetTupleCsv(chord_seq))

def BluesHarpProg():
    prog_seqs = set()
    for key, keyinfo in kNoteInfo.items():
        for proginfo in kProgInfo:
            seq = set()
            for gap, chord in proginfo['seq']:
                root = ShiftNote(key, gap)
                seq.update(GetChordSeq(root, kChordInfo[chord]))
            if GetNsemi(seq) < 3:
                seq.add(key)
                seq = list(seq)
                seq.sort(key=lambda x: kNoteInfo[x]['abs_pos'])
                seq = seq[seq.index(key):]+seq[:seq.index(key)]
                prog_seqs.add((key, GetProgName(proginfo), ' '.join(seq[1:])))

    print(','.join(['key', 'prog', 'seq']))
    for prog_seq in prog_seqs:
        print(GetTupleCsv(prog_seq))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cps', help='click per second', default=60, type=int) 
    p.add_argument('--rnd', help='round', default=60, type=int) 
    p.add_argument('--len', help='note number', default=3, type=int) 
    p.add_argument('--interval', help='chromatic range', default=11, type=int) 
    p.add_argument('--train', required=True, type=str, choices=['string', 'motive', 'blues_scale', 'blues_chord', 'blues_prog']) 
    args = p.parse_args() 

    if args.train == 'motive':
        return MotiveTrain(args)
    elif args.train == 'string':
        return StringTrain(args)
    elif args.train == 'blues_scale':
        return BluesHarpScale()
    elif args.train == 'blues_chord':
        return BluesHarpChord()
    elif args.train == 'blues_prog':
        return BluesHarpProg()
    else:
        return StringTrain(args)

main()
