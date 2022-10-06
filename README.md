# Usage

## MusicTheory
```bash
# random composing，random key x random mode x random sequence
python3 main.py --train motive [--len <sequence len> [--interval <gap between sequence, [0, 12)>]
```

## Guitar
```bash
# random absolute pitch, find it on all guitar string
python3 main.py --train string [--cps <bpm>] [--rnd <round, 12 note per round>]  
```

## Harmonica

### improvise material
find position for playing jazz standard
- semitone less than 2, aka less blending or overblow

```bash
# progress
python3 main.py --train blues_prog > prog.csv

# chord
python3 main.py --train blues_chord > chord.csv

# scale
python3 main.py --train blues_scale > scale.csv
```
