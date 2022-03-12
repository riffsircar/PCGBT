import py_trees
from PIL import Image
import random
from MegaMan import mm_library
from Metroid import met_library
from tile_images import *

GAME = 'met'

chunks = mm_library.chunks if GAME == 'mm' else met_library.chunks
dirs = mm_library.dirs if GAME == 'mm' else met_library.dirs
chunk_dir = mm_library.chunk_dir if GAME == 'mm' else met_library.chunk_dir
images = mm_images if GAME == 'mm' else met_images

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
	level_img.save('generic_' + GAME + '.png')

def compare(s1,s2,vert=False):
	print('in compare')
	for a,b in zip(s1,s2):
		if a == '-' and b == '-':
			return True
		if vert:
			if a in ['|','-'] and b in ['|','-']:
				return True
	return False

def sample_mm(dr,prev_lev, prev_dr):
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
		#print('prev_dr: ',prev_dr)
		#print('\nprev level: ','\n'.join(prev_lev))
		#print('level: ','\n'.join(level))
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

def sample_met(d,dummy1,dummy2):
	if d == 'DR':
		d = 'UDR'
	if d == 'DLR':
		d = 'UDLR'
	if d == 'U':
		d = 'UD'
	levels = dirs[d]
	level = random.choice(levels)
	return chunks[level]

sample_dir = sample_mm if GAME == 'mm' else sample_met

class CheckNode(py_trees.behaviour.Behaviour):
	def __init__(self,name,node_key):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key=node_key,access=py_trees.common.Access.READ)
		self.node_key = node_key

	def update(self):
		key_val = self.blackboard.get(self.node_key)
		if random.random() < key_val:
			return py_trees.common.Status.SUCCESS
		return py_trees.common.Status.FAILURE

class GenericSection(py_trees.behaviour.Behaviour):
	def __init__(self,name,dir,num_nodes):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=py_trees.common.Access.WRITE)
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
		return py_trees.common.Status.SUCCESS

class GenericSegmentNode(py_trees.behaviour.Behaviour):
	def __init__(self,name,dir):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=py_trees.common.Access.WRITE)
		self.dir = dir

	def update(self):
		level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dr)
		self.blackboard.prev = level
		self.blackboard.dr = self.dir
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		if self.dir in ['LR','DR']:
			self.blackboard.x += 1
		elif self.dir in ['UL','UD_U','UD_D','UR']:
			self.blackboard.y -= 1
		elif self.dir in ['DL']:
			self.blackboard.y += 1
		return py_trees.common.Status.SUCCESS

def upward_section():
	root = py_trees.composites.Sequence('Upward')
	ul = GenericSegmentNode('UpLeft','UL')
	ud = GenericSegmentNode('UpDown','UD')
	dr = GenericSegmentNode('Down Right','DR')
	root.add_child(ul)
	root.add_child(ud)
	root.add_child(dr)
	return root

def downward_section():
	print('Inside downward section')
	root = py_trees.composites.Sequence('Downward')
	dl = GenericSegmentNode('Down Left','DL')
	ud = GenericSegmentNode('UpDown','UD')
	ur = GenericSegmentNode('Up Right', 'UR')
	root.add_child(dl)
	root.add_child(ud)
	root.add_child(ur)
	return root

def select_ud():
	root = py_trees.composites.Selector('Vertical')
	check = py_trees.composites.Sequence('Check')
	do_up = CheckNode('Do Upward?','up_prob')
	u = upward_section()
	d = downward_section()
	check.add_child(do_up)
	check.add_child(u)
	root.add_child(check)
	root.add_child(d)
	return root

def select_hv():
	root = py_trees.composites.Selector('Horizontal or Vertical')
	check = py_trees.composites.Sequence('Check')
	do_h = CheckNode('Do Horizontal','h_prob')
	h = GenericSection('Horizontal', 'LR',random.randint(2,4))
	ud = select_ud()
	check.add_child(do_h)
	check.add_child(h)
	root.add_child(check)
	root.add_child(ud)
	return root

def create_root_generator():
	root = py_trees.composites.Sequence('Generic Level')
	hv = select_hv()
	h2 = GenericSection('Horizontal','LR',random.randint(2,4))
	#ud = select_ud()  # TODO: fix vertical MM infinite-sampling bug
	root.add_child(hv)
	root.add_child(h2)
	#root.add_child(ud)
	return root

def generate(h_prob=0.5, up_prob=0.5):
	root = create_root_generator()
	bt = py_trees.trees.BehaviourTree(root)
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='h_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='up_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='dr',access=py_trees.common.Access.WRITE)
	blackboard.h_prob, up_prob = h_prob, up_prob
	blackboard.x, blackboard.y = 0, 0
	blackboard.prev = None
	blackboard.dr = 'LR'
	blackboard.level = {}
	root.tick_once()
	level_to_image(blackboard.level)
	py_trees.display.render_dot_tree(root)

if __name__ == "__main__":
	generate()