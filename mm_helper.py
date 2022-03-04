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

def level_to_image(level):
	width, height = 0, 0
	xs = [x for (x,y) in level]
	ys = [y for (x,y) in level]
	min_y = min(ys)
	ys_adj = [y+abs(min_y) for y in ys]
	width, height = max(xs), max(ys_adj)
	level_img = Image.new('RGB',((width+1)*(16*16), (height+1)*15*16))
	print(level_img.size)
	for x,y in level:
		print(x,y)
		lev = level[(x,y)]
		img = Image.new('RGB',(16*16,15*16))
		for row, seq in enumerate(lev):
			for col, tile in enumerate(seq):
				img.paste(images[tile],(col*16,row*16))
		y_adj = y+abs(min_y)
		level_img.paste(img,(x*256,y_adj*240))
	level_img.save('test.png')

def compare(s1,s2,vert=False):
	print('in compare')
	for a,b in zip(s1,s2):
		if a == '-' and b == '-':
			return True
		if vert:
			if a in ['|','-'] and b in ['|','-']:
				return True
	return False

def sample_dir(dr,prev_lev, prev_dr):
	levels = dirs[dr]
	if not prev_lev:
		idx = random.choice(levels)
		return chunks[idx]
	prev_t = [''.join(s) for s in zip(*prev_lev)]
	prev_up, prev_down = prev_lev[0], prev_lev[len(prev_lev)-1]
	prev_left, prev_right = prev_t[0], prev_t[len(prev_t)-1]
	
	while True:
		idx = random.choice(levels)
		level = chunks[idx]
		level_t = [''.join(s) for s in zip(*level)]
		this_up, this_down = level[0], level[len(level)-1]
		this_left, this_right = level_t[0], level_t[len(prev_t)-1]
		print('prev_dr: ',prev_dr)
		print('\nprev level: ','\n'.join(prev_lev))
		print('level: ','\n'.join(level))
		if prev_dr in ['LR','UR','DR']:
			if compare(prev_right,this_left):
				break
		elif prev_dr in ['UL','UD_U']:
			if compare(prev_up,this_down,True):
				break
		elif prev_dr in ['DL','UD_D']:
			if compare(prev_down,this_up,True):
				break


	print('prev dr: ', prev_dr)
	return chunks[idx]

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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			level = sample_dir('LR',self.blackboard.prev,self.blackboard.dr)
			self.blackboard.prev = level
			self.blackboard.dr = 'LR'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			level = sample_dir('LR',self.blackboard.prev,self.blackboard.dr)
			self.blackboard.prev = level
			self.blackboard.dr = 'LR'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('UL',self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = 'UL'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('DL',self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = 'DL'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('DR',self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = 'DR'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('UR',self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = 'UR'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			level = sample_dir('UD',self.blackboard.prev,self.blackboard.dr)
			self.blackboard.prev = level
			self.blackboard.dr = 'UD_U'
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
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = sample_dir('UD',self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = 'UD_D'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y += 1
		return common.Status.SUCCESS
