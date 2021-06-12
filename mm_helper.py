from py_trees import *
from mm_library import *
import random
from PIL import Image


images = {
    "#":Image.open('tiles/MM_X2.png'),
    "*":Image.open('tiles/MM_star.png'),
    "+":Image.open('tiles/MM_+.png'),
    "-":Image.open('tiles/-.png'),
    "B":Image.open('tiles/MM_B2.png'),
    "C":Image.open('tiles/CMM.png'),
    "D":Image.open('tiles/DMM.png'),
    "H":Image.open('tiles/HMM.png'),
    "L":Image.open('tiles/MM_L.png'),
    "M":Image.open('tiles/MMM.png'),
    "P":Image.open('tiles/-.png'),
    "U":Image.open('tiles/MM_U.png'),
    "W":Image.open('tiles/MM_w.png'),
    "l":Image.open('tiles/MM_L.png'),
    "t":Image.open('tiles/TMM.png'),
    "w":Image.open('tiles/MM_w.png'),
    "|":Image.open('tiles/LMM.png')
}

verbatim = True

def sample_dir(d):
	levels = dirs[d]
	level = random.choice(levels)
	return chunks[level]

class DoHorizontal(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Do Gap")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='h_prob',access=common.Access.READ)

	def update(self):
		levels = []
		if random.random() < self.blackboard.h_prob:
			print('doing horizontal')
			return common.Status.SUCCESS
		print('doing vertical')
		return common.Status.FAILURE

class DoUpward(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Do Gap")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='up_prob',access=common.Access.READ)

	def update(self):
		levels = []
		if random.random() < self.blackboard.up_prob:
			print('doing upward')
			return common.Status.SUCCESS
		print('doing downward')
		return common.Status.FAILURE


class HorizontalSection(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='num_nodes',access=common.Access.READ)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			level = sample_dir('LR')
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
			self.blackboard.x += 1
		return common.Status.SUCCESS

class LeftRightSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="LR")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='num_nodes',access=common.Access.READ)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			level = sample_dir('LR')
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
			self.blackboard.x += 1
		return common.Status.SUCCESS

class UpLeftSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UL")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('UL')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y -= 1
		return common.Status.SUCCESS

class DownLeftSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="DL")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('DL')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y += 1
		return common.Status.SUCCESS

class DownRightSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="DR")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('DR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class UpRightSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UR")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('UR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return common.Status.SUCCESS

class UpwardSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UD")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='num_nodes',access=common.Access.READ)

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			level = sample_dir('UD')
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
			self.blackboard.y -= 1
		return common.Status.SUCCESS

class DownwardSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UD")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('UD')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y += 1
		return common.Status.SUCCESS
