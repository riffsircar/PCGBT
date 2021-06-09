from py_trees import *
from smb_library import *
import random
from PIL import Image

images = {
    # TODO: Get T, D, M tiles from Icarus
    "E": Image.open('tiles/E.png'),
    "H": Image.open('tiles/H.png'),
    "G": Image.open('tiles/G.png'),
    "M": Image.open('tiles/M.png'),
    "o": Image.open('tiles/o.png'),
    "S": Image.open('tiles/S.png'),
    "T": Image.open('tiles/T.png'),
    "?": Image.open('tiles/Q.png'),
    "Q": Image.open('tiles/Q.png'),
    "X": Image.open('tiles/X1.png'),
    "#": Image.open('tiles/X.png'),
    "-": Image.open('tiles/-.png'),
    "0": Image.open('tiles/0.png'),
    "D": Image.open('tiles/D.png'),
    "<": Image.open('tiles/PTL.png'),
    ">": Image.open('tiles/PTR.png'),
    "[": Image.open('tiles/[.png'),
    "]": Image.open('tiles/].png'),
    "*": Image.open('tiles/-.png'),
    "P": Image.open('tiles/P.png'),
	"B": Image.open('tiles/B.png'),
	"b": Image.open('tiles/bb.png')
}

def sample_pattern(p):
	levels = []
	for pat in patterns:
		if pat.startswith(p):
			levels.extend(patterns[pat])
	print(len(levels))
	level = random.choice(levels)
	return chunks[level]

def sample_pattern_groups(pats):
	levels = []
	for i, chunk_pat in enumerate(chunk_pats):
		if chunk_pat in pats:
			levels.append(i)
	level = random.choice(levels)
	return chunks[level]


class GapSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Stair up")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_pattern('G')
		self.blackboard.x += 1
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		return common.Status.SUCCESS