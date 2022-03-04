import py_trees
from mm_library import *
from mm_helper import *
import json

def upward_section():
	print('Inside upward section')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	root = py_trees.composites.Sequence('Upward')
	ul = UpLeftSegment('UpLeft')
	blackboard.num_nodes = random.randint(2,4)
	print('Upward NN: ', blackboard.num_nodes)
	ud = UpwardSegment('UpDown')
	dr = DownRightSegment('DownRight')
	root.add_child(ul)
	root.add_child(ud)
	root.add_child(dr)
	return root

def downward_section():
	print('Inside downward section')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	root = py_trees.composites.Sequence('Downward')
	dl = DownLeftSegment('DownLeft')
	blackboard.num_nodes = random.randint(2,4)
	print('Downward NN: ', blackboard.num_nodes)
	ud = DownwardSegment('UpDown')
	ur = UpRightSegment('UpRight')
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
	blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='dr',access=py_trees.common.Access.WRITE)
	blackboard.h_prob = 0.5
	blackboard.up_prob = 0.5
	blackboard.x = 0
	blackboard.y = 0
	blackboard.prev = None
	blackboard.dr = 'LR'
	blackboard.level = {}
	#print(blackboard)
	root.tick_once()
	#print(blackboard)
	#print(LEVEL)
	level_to_image(blackboard.level)
	#with open('level.json','w') as f:
	#	json.dump(LEVEL,f)
	py_trees.display.render_dot_tree(root)
