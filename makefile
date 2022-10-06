all:
	python3 main.py --train blues_prog

string:
	python3 main.py --train string

motive:
	python3 main.py --train motive

scale:
	python3 main.py --train blues_scale > scale.csv

chord:
	python3 main.py --train blues_chord > chord.csv

prog:
	python3 main.py --train blues_prog > prog.csv
