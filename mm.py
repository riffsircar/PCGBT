import py_trees
from mm_library import *
from mm_helper import *
import json
from PIL import Image

verbatim = False

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

class LR1(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[12] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR2(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[13] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR3(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[14] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR4(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[15] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR6(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[17] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class UL1(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[18] if verbatim else sample_dir('UL')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y -= 1
		return py_trees.common.Status.SUCCESS

class UD1(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[11] if verbatim else sample_dir('UD')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y -= 1
		return py_trees.common.Status.SUCCESS

class UD2(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[4] if verbatim else sample_dir('UD')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.y -= 1
		return py_trees.common.Status.SUCCESS

class DR1(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[5] if verbatim else sample_dir('DR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class DR2(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[0] if verbatim else sample_dir('DR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR7(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[6] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR9(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[9] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR10(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[1] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR11(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[2] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

class LR12(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="H1")
		self.blackboard.register_key(key='x',access=common.Access.WRITE)
		self.blackboard.register_key(key='y',access=common.Access.WRITE)
		self.blackboard.register_key(key='level',access=common.Access.WRITE)
		
	def update(self):
		level = chunks[3] if verbatim else sample_dir('LR')
		self.blackboard.level[(self.blackboard.x,self.blackboard.y)] = level
		self.blackboard.x += 1
		return py_trees.common.Status.SUCCESS

def create_root_m11():
	root = py_trees.composites.Sequence('MM 1-1')
	h1 = py_trees.composites.Sequence('Horizontal')
	u1 = py_trees.composites.Sequence('Upward')
	h2 = py_trees.composites.Sequence('Horizontal')
	u2 = py_trees.composites.Sequence('Upward')
	h3 = py_trees.composites.Sequence('Horizontal')

	lr1 = LR1('LR 1')
	lr2 = LR2('LR 2')
	lr3 = LR3('LR 3')
	lr4 = LR4('LR 4')
	lr5 = LR4('LR 5')
	lr6 = LR6('LR 6')
	h1.add_child(lr1)
	h1.add_child(lr2)
	h1.add_child(lr3)
	h1.add_child(lr4)
	h1.add_child(lr5)
	h1.add_child(lr6)

	ul1 = UL1('UL 1')
	ud1 = UD1('UD 1')
	dr1 = DR1('DR 1')
	u1.add_child(ul1)
	u1.add_child(ud1)
	u1.add_child(dr1)

	lr7 = LR7('LR 7')
	lr8 = LR4('LR 8')
	lr9 = LR9('LR 9')
	h2.add_child(lr7)
	h2.add_child(lr8)
	h2.add_child(lr9)

	ul2 = UL1('UL 2')
	ud2 = UD2('UD 2')
	dr2 = DR2('DR 2')
	u2.add_child(ul2)
	u2.add_child(ud2)
	u2.add_child(dr2)

	lr10 = LR10('LR10')
	lr11 = LR11('LR11')
	lr12 = LR12('LR12')
	h3.add_child(lr10)
	h3.add_child(lr11)
	h3.add_child(lr12)

	root.add_child(h1)
	root.add_child(u1)
	root.add_child(h2)
	root.add_child(u2)
	root.add_child(h3)
	return root

def upward_section():
	print('Inside upward section')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	root = py_trees.composites.Sequence('Upward')
	ul = UpLeftSegment('UL')
	blackboard.num_nodes = random.randint(2,4)
	print('Upward NN: ', blackboard.num_nodes)
	ud = UpwardSegment('UD')
	dr = DownRightSegment('DR')
	root.add_child(ul)
	root.add_child(ud)
	root.add_child(dr)
	return root

def downward_section():
	print('Inside downward section')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	root = py_trees.composites.Sequence('Downward')
	dl = DownLeftSegment('DL')
	blackboard.num_nodes = random.randint(2,4)
	print('Downward NN: ', blackboard.num_nodes)
	ud = DownwardSegment('UD')
	ur = UpRightSegment('UR')
	root.add_child(dl)
	root.add_child(ud)
	root.add_child(ur)
	return root

def select_ud():
	root = py_trees.composites.Selector('Vertical')
	check = py_trees.composites.Sequence('Check')
	do_up = DoUpward('Do Upward?')
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
	do_h = DoHorizontal('Do Horizontal?')
	h = HorizontalSection('Horizontal')
	ud = select_ud()
	check.add_child(do_h)
	check.add_child(h)
	root.add_child(check)
	root.add_child(ud)
	return root

def create_root_generator():
	root = py_trees.composites.Sequence('Level')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	blackboard.num_nodes = random.randint(2,4)
	print('NN: ',blackboard.num_nodes)
	h1 = HorizontalSection('Init Horizontal')
	root.add_child(h1)
	hv = select_hv()
	blackboard.num_nodes = random.randint(2,4)
	print('NN: ',blackboard.num_nodes)
	h2 = HorizontalSection('Middle Horizontal')
	ud = select_ud()
	blackboard.num_nodes = random.randint(2,4)
	print('NN: ',blackboard.num_nodes)
	h3 = HorizontalSection('Final Horizontal')
	root.add_child(hv)
	root.add_child(h2)
	root.add_child(ud)
	root.add_child(h3)
	return root


if __name__ == '__main__':
	#root = create_root_m11()
	#root = create_stairs_pipes_enemies()
	root = create_root_generator()
	bt = py_trees.trees.BehaviourTree(root)
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='h_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='up_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	blackboard.h_prob = 0.5
	blackboard.up_prob = 0.5
	blackboard.x = 0
	blackboard.y = 0
	blackboard.level = {}
	#print(blackboard)
	root.tick_once()
	#print(blackboard)
	#print(LEVEL)
	level_to_image(blackboard.level)
	#with open('level.json','w') as f:
	#	json.dump(LEVEL,f)
	py_trees.display.render_dot_tree(root)
