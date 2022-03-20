import sys, os
sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
import py_trees
from mm_library import *
from mm_helper import *

def upward_section():
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

def create_generator_root():
	root = py_trees.composites.Sequence('MM Level')
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='num_nodes',access=py_trees.common.Access.WRITE)
	h1 = MegaManSection('Horizontal','LR',random.randint(2,4))
	root.add_child(h1)
	hv = select_hv()
	h2 = MegaManSection('Middle Horizontal','LR',random.randint(2,4))
	ud = select_ud()
	h3 = MegaManSection('Final Horizontal','LR',random.randint(2,4))
	root.add_child(hv)
	root.add_child(h2)
	root.add_child(ud)
	root.add_child(h3)
	return root


def generate(h_prob=0.5, up_prob=0.5, name='mm_level'):
	root = create_generator_root()
	bt = py_trees.trees.BehaviourTree(root)
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='h_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='up_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='prev',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='dir',access=py_trees.common.Access.WRITE)
	blackboard.h_prob = h_prob
	blackboard.up_prob = up_prob
	blackboard.x, blackboard.y = 0, 0
	blackboard.prev = None
	blackboard.dir = 'LR'
	blackboard.level = {}
	root.tick_once()
	level_to_image(blackboard.level, name, 'mm')
	py_trees.display.render_dot_tree(root, name=name + '_tree')

if __name__ == '__main__':
	generate()