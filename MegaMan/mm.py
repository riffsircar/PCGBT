import sys
sys.path.append('..')
import py_trees
from mm_library import *
from mm_helper import *

def upward_section():
	print('Inside upward section')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	root = py_trees.composites.Sequence('Upward')
	ul = MegaManSegmentNode('UpLeft','UL')
	ud = MegaManSection('UpDown','UD_U',random.randint(2,4))
	dr = MegaManSegmentNode('DownRight','DR')
	root.add_child(ul)
	root.add_child(ud)
	root.add_child(dr)
	return root

def downward_section():
	print('Inside downward section')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	root = py_trees.composites.Sequence('Downward')
	dl = MegaManSegmentNode('DownLeft','DL')
	ud = MegaManSection('UpDown','UD_D',random.randint(2,4))
	ur = MegaManSegmentNode('UpRight','UR')
	root.add_child(dl)
	root.add_child(ud)
	root.add_child(ur)
	return root

def select_ud():
	print('in ud')
	root = py_trees.composites.Selector('Vertical')
	check = py_trees.composites.Sequence('Check')
	do_up = MegaManCheckNode('Do Upward?', 'up_prob')
	u = upward_section()
	d = downward_section()
	check.add_child(do_up)
	check.add_child(u)
	root.add_child(check)
	root.add_child(d)
	return root

def select_hv():
	print('in hv')
	root = py_trees.composites.Selector('Horizontal or Vertical')
	check = py_trees.composites.Sequence('Check')
	do_h = MegaManCheckNode('Do Horizontal?', 'h_prob')
	h = MegaManSection('Horizontal','LR',random.randint(2,4))
	ud = select_ud()
	check.add_child(do_h)
	check.add_child(h)
	root.add_child(check)
	root.add_child(ud)
	return root

def create_root_generator():
	root = py_trees.composites.Sequence('MM Level')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	h1 = MegaManSection('Horizontal','LR',random.randint(2,4))
	print('h1 done')
	root.add_child(h1)
	hv = select_hv()
	h2 = MegaManSection('Middle Horizontal','LR',random.randint(2,4))
	print('h2 done')
	ud = select_ud()
	h3 = MegaManSection('Final Horizontal','LR',random.randint(2,4))
	print('h3 done')
	root.add_child(hv)
	root.add_child(h2)
	root.add_child(ud)
	root.add_child(h3)
	return root


if __name__ == '__main__':
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
