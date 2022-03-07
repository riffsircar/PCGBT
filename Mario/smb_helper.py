import sys, os
sys.path.append(os.path.dirname(__file__))
from py_trees import *
from smb_library import *
from tile_images import *
import random
from PIL import Image

dp = {
	'E': ['E1','E2','E3','E4','R','GE','RR'],
	'G': ['G1','GM','GP','GE','GV'],
	'V': ['V','VP','VN','VE','VR','GV'],
	'P': ['P2','P3','RR'],
	'S': ['SU','SD','SVN','SVE','SVG'],
	'|': ['VP','GP'],
	'I': ['I']
}

def level_to_image(level):
	width, height = 0, 0
	xs = [x for (x,y) in level]
	ys = [y for (x,y) in level]
	width, height = max(xs), max(ys)
	level_img = Image.new('RGB',((width+1)*(16*16), 15*16))
	print(level_img.size)
	for x,y in level:
		print(x,y)
		lev = level[(x,y)]
		img = Image.new('RGB',(16*16,15*16))
		for row, seq in enumerate(lev):
			for col, tile in enumerate(seq):
				img.paste(smb_images[tile],(col*16,row*16))
		level_img.paste(img,(x*256,y*240))
	level_img.save('test.png')

def sample_pattern(p):
	levels = []
	for pat in patterns:
		if pat.startswith(p):
			levels.extend(patterns[pat])
	print(len(levels))
	level = random.choice(levels)
	return chunks[level]

def sample_pattern_groups(pats,exact=False):
	levels = []
	for key in chunk_pats:
		chunk_pat = chunk_pats[key]
		for pat in pats:
			if not exact:
				if any(p in chunk_pat for p in dp[pat]):
					levels.append(key)
			else:
				if all(p in chunk_pat for p in dp[pat]):
					levels.append(key)
			"""
			for cp in chunk_pat:
				if cp.startswith(pat):
					levels.append(key)
			"""
	level = random.choice(levels)
	print(chunk_pats[level])
	return chunks[level]

def get_pipe_levels():
	levels = []
	for pat in patterns:
		if pat == 'VP' or pat == 'GP':
			levels.extend(patterns[pat])
	return levels

class MarioSegmentNode(behaviour.Behaviour):
	def __init__(self,name,pattern):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.pattern = pattern
	
	def update(self):
		print('Sampling ' + self.name)
		level = sample_pattern_groups(self.pattern)
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		print('Level: ', self.blackboard.level)
		self.blackboard.x += 1
		return common.Status.SUCCESS

class MarioCheckNode(behaviour.Behaviour):
	def __init__(self,name,node_key):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key=node_key,access=common.Access.READ)
		self.node_key = node_key

	def update(self):
		levels = []
		key_val = self.blackboard.get(self.node_key)
		#if random.random() < self.blackboard.pp_prob:
		if random.random() < key_val:
			print('doing pp')
			return common.Status.SUCCESS
		print('doing se')
		return common.Status.FAILURE