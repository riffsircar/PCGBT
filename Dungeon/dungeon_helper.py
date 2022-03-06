import sys, os, random
sys.path.append('..')
from PIL import Image
from Metroid import met_library

zelda_images = {
   "B":Image.open('../tiles/Z_B.png'), # block
   "D":Image.open('../tiles/DMM.png'), # door
   "F":Image.open('../tiles/Z_F.png'), # floor
   "I":Image.open('../tiles/Z_I.png'), # elemental block
   "M":Image.open('../tiles/Z_M.png'), # statue/monster
   "O":Image.open('../tiles/Z_O.png'), # elemental floor
   "P":Image.open('../tiles/Z_P.png'), # pond/lava
   "S":Image.open('../tiles/Z_S.png'), # stairs
   "W":Image.open('../tiles/Z_W.png')  # wall
}

met_images = {
    "#":Image.open('../tiles/Met_X.png'),  # solid
    "(":Image.open('../tiles/0.png'),  # beam around door (ignore using background)
    ")":Image.open('../tiles/0.png'),  # beam around door (ignore using background)
    "+":Image.open('../tiles/Met_+.png'),  # powerup
    "-":Image.open('../tiles/0.png'),   # background
    "B":Image.open('../tiles/Met_B.png'),  # breakable
    "D":Image.open('../tiles/Met_D.png'),  # door
    "E":Image.open('../tiles/Met_E.png'),  # enemy
    "P":Image.open('../tiles/0.png'),   # path
    "[":Image.open('../tiles/Met_[.png'),  # ??
    "]":Image.open('../tiles/Met_].png'),  # ??
    "^":Image.open('../tiles/Met_^2.png'),  # lava
    "v":Image.open('../tiles/0.png')  # ??
}

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
folder = 'zelda_rooms_new/'
for idx, file_name in enumerate(os.listdir(folder)):
	level = open(folder + file_name,'r').read().splitlines()
	label = get_door_label(level)
	if label not in dirs:
		dirs[label] = []
		dirs[label].append(idx)
	chunks[idx] = level