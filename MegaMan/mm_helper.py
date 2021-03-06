import sys, os
sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
from py_trees import *
from mm_library import *
from tile_images import *
import random

def compare(s1,s2,vert=False):
	for a,b in zip(s1,s2):
		if a == '-' and b == '-':
			return True
		if vert:
			if a in ['|','-','t'] and b in ['|','-','t']:
				return True
	return False

def sample_dir(this_dr, prev_lev, prev_dr):
	levels = dirs[this_dr]
	if not prev_lev:
		idx = random.choice(levels)
		return chunks[idx]

	prev_t = [''.join(s) for s in zip(*prev_lev)]
	prev_up, prev_down = prev_lev[0], prev_lev[len(prev_lev)-1]
	_, prev_right = prev_t[0], prev_t[len(prev_t)-1]

	while len(levels) > 0:
		idx = random.choice(levels)
		level = chunks[idx]
		level_t = [''.join(s) for s in zip(*level)]
		this_up, this_down = level[0], level[len(level)-1]
		this_left, this_right = level_t[0], level_t[len(prev_t)-1]
		if prev_dr in ['LR','UR','DR']:
			if compare(prev_right,this_left):
				break
		elif prev_dr in ['UL','UD_U']:
			if compare(prev_up,this_down,True):
				break
		elif prev_dr in ['DL','UD_D']:
			if compare(prev_down,this_up,True):
				break
		levels.remove(idx)
	if len(levels) <= 0:
		#print('No valid level with required directionality found!')
		return None
	return chunks[idx]

class MegaManSegmentNode(behaviour.Behaviour):
	def __init__(self,name,dir):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dir',access=common.Access.WRITE)
		self.blackboard.register_key(key='started',access=common.Access.WRITE)
		self.dir = dir
	
	def update(self):
		level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dir)
		if level is None:
			print("Sampling failed!!")
			return common.Status.FAILURE
		self.blackboard.prev = level
		self.blackboard.dir = self.dir
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		if self.dir in ['LR','DR']:
			self.blackboard.x += 1
		elif self.dir in ['UD_U','UL', 'UR']:
			self.blackboard.y -= 1
		elif self.dir in ['UD_D','DL']:
			self.blackboard.y += 1
		if not self.blackboard.started:
			self.blackboard.started = True
		return common.Status.SUCCESS


class GenerateSegment(behaviour.Behaviour):
	def __init__(self, name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dir',access=common.Access.WRITE)
		self.blackboard.register_key(key='generated',access=common.Access.WRITE)
		self.blackboard.register_key(key='started',access=common.Access.WRITE)
		self.this_dir = None
	
	def update(self):
		if self.blackboard.dir == None or self.blackboard.dir in ['DR','UR']:
			self.this_dir = 'LR'
		elif self.blackboard.dir == 'LR':
			self.this_dir = random.choice(['LR','UL','DL'])
		elif self.blackboard.dir == 'UD_U':
			self.this_dir = random.choice(['UD_U','UR','DR'])
		elif self.blackboard.dir == 'UD_D':
			self.this_dir = random.choice(['UD_D','UR'])
		elif self.blackboard.dir == 'UL':
			self.this_dir = 'UD_U'
		elif self.blackboard.dir == 'DL':
			self.this_dir = 'UD_D'
		
		level = sample_dir(self.this_dir[:2],self.blackboard.prev,self.blackboard.dir)
		if level is None:
			return common.Status.FAILURE
		self.blackboard.prev = level
		self.blackboard.dir = self.this_dir
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		if self.this_dir in ['LR','DR','UR']:
			self.blackboard.x += 1
		elif self.this_dir in ['UD_U','UL']:
			self.blackboard.y -= 1
		elif self.this_dir in ['UD_D','DL']:
			self.blackboard.y += 1
		self.blackboard.generated += 1
		if not self.blackboard.started:
			self.blackboard.started = True
		return common.Status.SUCCESS

class MegaManCheckNode(behaviour.Behaviour):
	def __init__(self,name,node_key):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key=node_key,access=common.Access.READ)
		self.node_key = node_key

	def update(self):
		key_val = self.blackboard.get(self.node_key)
		if random.random() < key_val:
			return common.Status.SUCCESS
		return common.Status.FAILURE

class MegaManSection(behaviour.Behaviour):
	def __init__(self,name,dir,num_nodes):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dir',access=common.Access.WRITE)
		self.dir = dir
		self.num_nodes = num_nodes

	def update(self):
		for _ in range(self.num_nodes):
			level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dir)
			if level is None:
				return common.Status.FAILURE
			self.blackboard.prev = level
			self.blackboard.dir = self.dir
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
			if self.dir in ['LR','DR']:
				self.blackboard.x += 1
			elif self.dir in ['UD_U','UL','UR']:
				self.blackboard.y -= 1
			elif self.dir in ['UD_D','DL']:
				self.blackboard.y += 1
		return common.Status.SUCCESS

class CheckStart(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='started',access=common.Access.READ)
		
	def update(self):
		if self.blackboard.started:
			return common.Status.SUCCESS
		return common.Status.FAILURE

class CheckNumSegments(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='num_segments',access=common.Access.READ)
		self.blackboard.register_key(key='generated',access=common.Access.READ)
		
	def update(self):
		if self.blackboard.generated < self.blackboard.num_segments:
			return common.Status.FAILURE
		return common.Status.SUCCESS