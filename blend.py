from py_trees import *
from Mario import smb_helper
from MegaMan import mm_helper
from Metroid import met_helper
import random
from PIL import Image

class InitSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="init")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		level = smb_helper.sample_pattern_groups(['I'])
		self.blackboard.prev = level
		self.blackboard.dr = 'LR'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, 'smb']
		self.blackboard.x += 1
		return common.Status.SUCCESS

class PipeSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Valley")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		#level = chunks[11]
		print('Sampling pipes')
		level = smb_helper.sample_pattern_groups(['|'])
		self.blackboard.prev = level
		self.blackboard.dr = 'LR'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, 'smb']
		self.blackboard.x += 1
		return common.Status.SUCCESS

class StairsSegment(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Valley")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)

	def update(self):
		levels = []
		#level = chunks[11]
		print('Sampling stairs')
		level = smb_helper.sample_pattern_groups(['S'])
		self.blackboard.prev = level
		self.blackboard.dr = 'LR'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, 'smb']
		self.blackboard.x += 1
		return common.Status.SUCCESS

class HorizontalSection(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='num_nodes',access=common.Access.READ)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			if self.game == 'mm':
				level = mm_helper.sample_dir('LR',self.blackboard.prev,self.blackboard.dr)
			else:
				level = met_helper.sample_met('LR',None,None)
			self.blackboard.prev = level
			self.blackboard.dr = 'LR'
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
			self.blackboard.x += 1
		return common.Status.SUCCESS


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
		lev, game = level[(x,y)][0], level[(x,y)][1]
		print('\n'.join(lev), game)
		if game == 'smb':
			images = smb_helper.images
		elif game == 'mm':
			images = mm_helper.images
		else:
			images = met_helper.images
		img = Image.new('RGB',(16*16,15*16))
		for row, seq in enumerate(lev):
			for col, tile in enumerate(seq):
				img.paste(images[tile],(col*16,row*16))
		y_adj = y+abs(min_y)
		level_img.paste(img,(x*256,y_adj*240))
	level_img.save('blend level.png')

class UpLeftSegment(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UL")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		if self.game == 'mm':
			level = mm_helper.sample_dir('UL',self.blackboard.prev,self.blackboard.dr)
		else:
			level = met_helper.sample_met('UL',None,None)
		self.blackboard.prev = level
		self.blackboard.dr = 'UL'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
		self.blackboard.y -= 1
		return common.Status.SUCCESS

class DownLeftSegment(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="DL")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		if self.game == 'mm':
			level = mm_helper.sample_dir('DL',self.blackboard.prev,self.blackboard.dr)
		else:
			level = met_helper.sample_met('DL',None,None)
		self.blackboard.prev = level
		self.blackboard.dr = 'DL'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
		self.blackboard.y += 1
		return common.Status.SUCCESS

class DownRightSegment(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="DR")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		if self.game == 'mm':
			level = mm_helper.sample_dir('DR',self.blackboard.prev,self.blackboard.dr)
		else:
			level = met_helper.sample_met('DR',None,None)
		self.blackboard.prev = level
		self.blackboard.dr = 'DR'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
		self.blackboard.x += 1
		return common.Status.SUCCESS

class UpRightSegment(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UR")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		if self.game == 'mm':
			level = mm_helper.sample_dir('UR',self.blackboard.prev,self.blackboard.dr)
		else:
			level = met_helper.sample_met('UR',None,None)
		self.blackboard.prev = level
		self.blackboard.dr = 'UR'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
		self.blackboard.x += 1
		return common.Status.SUCCESS

class UpwardSegment(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UD")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='num_nodes',access=common.Access.READ)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		nn = self.blackboard.num_nodes
		for _ in range(nn):
			if self.game == 'mm':
				level = mm_helper.sample_dir('UD',self.blackboard.prev,self.blackboard.dr)
			else:
				level = met_helper.sample_met('UD',None,None)
			self.blackboard.prev = level
			self.blackboard.dr = 'UD_U'
			self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
			self.blackboard.y -= 1
		return common.Status.SUCCESS

class DownwardSegment(behaviour.Behaviour):
	def __init__(self,name,game):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="UD")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		self.blackboard.register_key(key='prev',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='game',access=common.Access.READ)
		self.game = game

	def update(self):
		levels = []
		if self.game == 'mm':
			level = mm_helper.sample_dir('UD',self.blackboard.prev,self.blackboard.dr)
		else:
			level = met_helper.sample_met('UD',None,None)
		self.blackboard.prev = level
		self.blackboard.dr = 'UD_D'
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = [level, self.game]
		self.blackboard.y += 1
		return common.Status.SUCCESS

def upward_section(game):
	print('Inside upward section')
	bbl = blackboard.Client()
	bbl.register_key(key='num_nodes',access=common.Access.WRITE)
	root = composites.Sequence('Upward')
	ul = UpLeftSegment('UpLeft',game)
	bbl.num_nodes = random.randint(2,4)
	ud = UpwardSegment('UpDown',game)
	dr = DownRightSegment('DownRight',game)
	root.add_child(ul)
	root.add_child(ud)
	root.add_child(dr)
	return root

def downward_section(game):
	print('Inside downward section')
	bbl = blackboard.Client()
	bbl.register_key(key='num_nodes',access=common.Access.WRITE)
	root = composites.Sequence('Downward')
	dl = DownLeftSegment('DownLeft',game)
	bbl.num_nodes = random.randint(2,4)
	ud = DownwardSegment('UpDown',game)
	ur = UpRightSegment('UpRight',game)
	root.add_child(dl)
	root.add_child(ud)
	root.add_child(ur)
	return root

def select_ud():
	root = composites.Selector('Vertical')
	check = composites.Sequence('Check')
	do_up = mm_helper.DoUpward('Do Upward?')
	u = upward_section('mm')
	d = downward_section('mm')
	check.add_child(do_up)
	check.add_child(u)
	root.add_child(check)
	root.add_child(d)
	return root

def create_mm():
	root = composites.Selector('Mega Man')
	bbl = blackboard.Client()
	bbl.register_key(key='num_nodes',access=common.Access.WRITE)
	#bbl.register_key(key='game',access=common.Access.WRITE)
	#bbl.game = 'mm'
	check = composites.Sequence('Check')
	do_h = mm_helper.DoHorizontal('Do Horizontal?')
	bbl.num_nodes = random.randint(2,4)
	h = HorizontalSection('Horizontal','mm')
	down = downward_section('mm')
	#ud = select_ud()
	check.add_child(do_h)
	check.add_child(h)
	root.add_child(check)
	root.add_child(down)
	return root
	return root

def create_met():
	root = composites.Sequence('Metroid')
	bbl = blackboard.Client()
	bbl.register_key(key='num_nodes',access=common.Access.WRITE)
	bbl.num_nodes = random.randint(2,4)
	h = HorizontalSection('Horizontal','met')
	u = upward_section('met')
	root.add_child(h)
	root.add_child(u)
	return root

def create_mario():
	root = composites.Sequence('Mario')
	init = InitSegment('Initial')
	pipes = PipeSegment('Pipes')
	stairs = StairsSegment('Stairs')
	root.add_child(init)
	root.add_child(pipes)
	root.add_child(stairs)
	return root

def create_root():
	root = composites.Sequence('Blend')
	bbl = blackboard.Client()
	bbl.register_key(key='game',access=common.Access.WRITE)
	bbl.game = 'smb'
	print('in root', bbl.game)
	mario = create_mario()
	bbl.game = 'mm'
	mm = create_mm()
	met = create_met()
	root.add_child(mario)
	root.add_child(mm)
	root.add_child(met)
	return root

if __name__ == '__main__':
	root = create_root()
	bt = trees.BehaviourTree(root)
	bbl = blackboard.Client()
	bbl.register_key(key='x',access=common.Access.WRITE)
	bbl.register_key(key='y',access=common.Access.WRITE)
	bbl.register_key(key='level',access=common.Access.WRITE)
	bbl.register_key(key='game',access=common.Access.WRITE)
	bbl.register_key(key='prev',access=common.Access.WRITE)
	bbl.register_key(key='dr',access=common.Access.WRITE)
	bbl.register_key(key='num_nodes',access=common.Access.WRITE)
	bbl.register_key(key='up_prob',access=common.Access.WRITE)
	bbl.register_key(key='h_prob',access=common.Access.WRITE)
	bbl.x = 0
	bbl.y = 0
	bbl.up_prob, bbl.h_prob = 0.5, 0.5
	bbl.prev, bbl.dr = None, None
	bbl.level = {}
	root.tick_once()
	print(bbl.level)
	level_to_image(bbl.level)
	display.render_dot_tree(root)