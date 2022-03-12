import sys, os, random
sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
from Metroid import met_library
from tile_images import *

def sample_dir(d):
	levels = dirs[d]
	level = random.choice(levels)
	return chunks[level]

def sample_met(d):
	if d == 'DR':
		d = 'UDR'
	if d == 'DLR':
		d = 'UDLR'
	if d == 'U':
		d = 'UD'
	levels = met_library.dirs[d]
	level = random.choice(levels)
	return met_library.chunks[level]

def get_door_label(room):
    label = ''
    room_string = ''
    for l in room:
        room_string += ''.join(l)
    room_t = [''.join(s) for s in zip(*room)]
    if 'D' in room[1]:
        label += 'U'
    if 'D' in room[len(room)-2]:
        label += 'D'
    if 'D' in room_t[1]:
        label += 'L'
    if 'D' in room_t[len(room_t)-2]:
        label += 'R'
    return label


dirs = {}
chunks = {}
path = os.path.dirname(__file__)
folder = path + '/zelda_rooms_new/'
for idx, file_name in enumerate(os.listdir(folder)):
	level = open(folder + file_name,'r').read().splitlines()
	label = get_door_label(level)
	if label not in dirs:
		dirs[label] = []
		dirs[label].append(idx)
	chunks[idx] = level