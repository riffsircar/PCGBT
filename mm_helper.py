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
	#print('in compare')
	for a,b in zip(s1,s2):
		if a == '-' and b == '-':
			return True
		if vert:
			if a in ['|','-','t'] and b in ['|','-','t']:
				return True
	return False

def sample_dir(this_dr, prev_lev, prev_dr):
	#print('dr: ', dr)
	levels = dirs[this_dr]
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
		#print('this_dr: ', dr, '\tprev_dr: ',prev_dr)
		# print('\nprev level:')
		# print('\n'.join(prev_lev))
		# print('level:')
		# print('\n'.join(level))
		if prev_dr in ['LR','UR','DR']:
			if compare(prev_right,this_left):
				break
		elif prev_dr in ['UL','UD_U']:
			if compare(prev_up,this_down,True):
				break
		elif prev_dr in ['DL','UD_D']:
			if compare(prev_down,this_up,True):
				break

	#print('prev dr: ', prev_dr)
	return chunks[idx]

class MegaManSegmentNode(behaviour.Behaviour):
	def __init__(self,name,dir):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.dir = dir
	
	def update(self):
		level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = self.dir
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		if self.dir == 'LR':
			self.blackboard.x += 1
		elif self.dir == 'UD_U':
			self.blackboard.y -= 1
		elif self.dir == 'UD_D':
			self.blackboard.y += 1
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
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.dir = dir
		self.num_nodes = num_nodes

	def update(self):
		for _ in range(self.num_nodes):
			level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dr)
			self.blackboard.prev = level
			self.blackboard.dr = self.dir
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
			if self.dir == 'LR':
				self.blackboard.x += 1
			elif self.dir == 'UD_U':
				self.blackboard.y -= 1
			elif self.dir == 'UD_D':
				self.blackboard.y += 1
		return common.Status.SUCCESS