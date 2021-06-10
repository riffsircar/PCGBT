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
	for key in chunk_pats:
		chunk_pat = chunk_pats[key]
		for pat in pats:
			for cp in chunk_pat:
				if cp.startswith(pat):
					levels.append(key)
	level = random.choice(levels)
	return chunks[level]

def get_pipe_levels():
	levels = []
	for pat in patterns:
		if pat == 'VP' or pat == 'GP':
			levels.extend(patterns[pat])
	return levels

class PathsPipesSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Paths Pipes")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		#level = chunks[11]
		print('Sampling PP')
		level = sample_pattern_groups(['VP','P','RR'])
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class StairsEnemiesSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Stairs Enemies")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		#level = chunks[11]
		print('Sampling SE')
		level = sample_pattern_groups(['E','S'])
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class DoPathPipe(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Do Path Pipe")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='pp_prob',access=common.Access.READ)

	def update(self):
		levels = []
		#level = chunks[11]
		#self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		#self.blackboard.x += 1
		if random.random() < self.blackboard.pp_prob:
			print('doing pp')
			return common.Status.SUCCESS
		print('doing se')
		return common.Status.FAILURE

class InitSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="init")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_pattern_groups(['I'])
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class StairUpSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Stair up")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = chunks[11]
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class StairValleySegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Stair Valley")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = chunks[9]
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class PipeValleySegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Stair up")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = chunks[2]
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class RiskRewardSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="RR")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = chunks[7]
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class EnemyWithPathsSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="EWP")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = chunks[1]
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class EnemyHordeSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="EH")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = chunks[7]
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS


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