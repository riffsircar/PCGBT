import py_trees
import random
from MegaMan import mm_helper
from Metroid import met_helper
from tile_images import *

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
		self.blackboard.register_key(key='dir',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='game',access=py_trees.common.Access.READ)
		self.dir = dir
		self.num_nodes = num_nodes

	def update(self):
		sample_dir = mm_helper.sample_dir if self.blackboard.game == 'mm' else met_helper.sample_met
		for _ in range(self.num_nodes):
			level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dir)
			if level is None:
				return py_trees.common.Status.FAILURE
			self.blackboard.prev = level
			self.blackboard.dir = self.dir
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
			if self.dir in ['LR','DR']:
				self.blackboard.x += 1
			elif self.dir in ['UD_U','UL','UR']:
				self.blackboard.y -= 1
			elif self.dir in ['UD_D','DL']:
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
		self.blackboard.register_key(key='dir',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='game',access=py_trees.common.Access.READ)
		self.dir = dir

	def update(self):
		sample_dir = mm_helper.sample_dir if self.blackboard.game == 'mm' else met_helper.sample_met
		level = sample_dir(self.dir[:2],self.blackboard.prev,self.blackboard.dir)
		if level is None:
			return py_trees.common.Status.FAILURE
		self.blackboard.prev = level
		self.blackboard.dir = self.dir
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		if self.dir in ['LR','DR']:
			self.blackboard.x += 1
		elif self.dir in ['UL','UD_U','UR']:
			self.blackboard.y -= 1
		elif self.dir in ['DL','UD_D']:
			self.blackboard.y += 1
		return py_trees.common.Status.SUCCESS

class GenerateGenericSegment(py_trees.behaviour.Behaviour):
	def __init__(self, name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='dir',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='generated',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='started',access=py_trees.common.Access.WRITE)
		self.blackboard.register_key(key='game',access=py_trees.common.Access.READ)
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
		sample_dir = mm_helper.sample_dir if self.blackboard.game == 'mm' else met_helper.sample_met
		level = sample_dir(self.this_dir[:2],self.blackboard.prev,self.blackboard.dir)
		if level is None:
			# fine for loop since same segment is just resampled on next tick
			print(self.this_dir)
			print('NONE\n')
			return py_trees.common.Status.FAILURE
			
		self.blackboard.prev = level
		self.blackboard.dir = self.this_dir
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		print(self.this_dir, self.blackboard.x, self.blackboard.y)
		print('\n'.join(level))
		print('\n')
		if self.this_dir in ['LR','DR','UR']:
			self.blackboard.x += 1
		elif self.this_dir in ['UD_U','UL']:
			self.blackboard.y -= 1
		elif self.this_dir in ['UD_D','DL']:
			self.blackboard.y += 1
		self.blackboard.generated += 1
		if not self.blackboard.started:
			self.blackboard.started = True
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

def select_hv(h_size):
	root = py_trees.composites.Selector('Horizontal or Vertical')
	check = py_trees.composites.Sequence('Check')
	do_h = CheckNode('Do Horizontal','h_prob')
	h = GenericSection('Horizontal', 'LR', h_size)
	ud = select_ud()
	check.add_child(do_h)
	check.add_child(h)
	root.add_child(check)
	root.add_child(ud)
	return root

def is_start():
	root = py_trees.composites.Selector('Started?')
	check = mm_helper.CheckStart('CheckStart')
	start = GenerateGenericSegment('Start')
	root.add_child(check)
	root.add_child(start)
	return root

def generate_more():
	root = py_trees.composites.Selector('Generate More?')
	check = mm_helper.CheckNumSegments('CheckNumSegments')
	segment = GenerateGenericSegment('Generate Segment')
	root.add_child(check)
	root.add_child(segment)
	return root

def generate_loop(game, num=10, name='generic_loop'):
	root = py_trees.composites.Sequence('Generic Level')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='dir',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='generated',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='num_segments',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='started',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='game',access=py_trees.common.Access.WRITE)
	blackboard.started = False
	blackboard.prev = None
	blackboard.generated = 0
	blackboard.game = game
	blackboard.num_segments = num
	blackboard.x, blackboard.y = 0, 0
	blackboard.level = {}
	blackboard.dir = 'LR'
	start = is_start()
	more = generate_more()
	root.add_child(start)
	root.add_child(more)
	while blackboard.generated < blackboard.num_segments:
		root.tick_once()
	level_to_image(blackboard.level, 'generic_' + game, game)
	py_trees.display.render_dot_tree(root, name=name + '_tree')

def create_generator_root(h_size):
	root = py_trees.composites.Sequence('Generic Level')
	hv = select_hv(h_size)
	h2 = GenericSection('Horizontal','LR', h_size)
	ud = select_ud()
	root.add_child(hv)
	root.add_child(h2)
	root.add_child(ud)
	return root

def generate(game='met', h_prob=0.5, up_prob=0.5, h_size=3, name='generic_level'):
	root = create_generator_root(h_size)
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='h_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='up_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='dr',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='game',access=py_trees.common.Access.WRITE)
	blackboard.h_prob = h_prob
	blackboard.up_prob = up_prob
	blackboard.game = game
	blackboard.x, blackboard.y = 0, 0
	blackboard.prev = None
	blackboard.dr = 'LR'
	blackboard.level = {}
	root.tick_once()
	level_to_image(blackboard.level, 'generic_' + game, game)
	py_trees.display.render_dot_tree(root, name=name + '_tree')

if __name__ == "__main__":
	generate_loop('mm')