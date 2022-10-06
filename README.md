# Usage

## Define
|column|desc
|-|-
|key|tonic key
|scale|eg. major, melodic minor
|prog|chord progression
|attr|chord color or attribute, eg. ma7, m7, dim
|seq|note sequence, represent chord/scale detail
|cat|category
|position|C bluesharp position
|position\_key|C bluesharp position key
|nsemi|semitone count, represent if it's easy for C bluesharp

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
Search position for playing jazz standard
- triad semiton < 2
- 7th chord < 3
- scale semitone < 3

```bash
# progress
python3 main.py --train blues_prog > prog.csv

# chord
python3 main.py --train blues_chord > chord.csv

# scale
python3 main.py --train blues_scale > scale.csv
```
