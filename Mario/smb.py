import sys, os
sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
import py_trees
from smb_library import *
from smb_helper import *

def select_pp_se():
	root = py_trees.composites.Selector('PP or SE')
	check_pp = py_trees.composites.Sequence('Check PP')
	do_pp = MarioCheckNode('Do Path-Pipe?','pp_prob')
	pp1 = MarioSegmentNode('Paths and Pipes', ['P','|'])
	pp2 = MarioSegmentNode('Paths and Pipes', ['P','|'])
	check_pp.add_child(do_pp)
	check_pp.add_child(pp1)
	check_pp.add_child(pp2)
	se = py_trees.composites.Sequence('SE')
	se1 = MarioSegmentNode('Stairs and Enemies', ['S','E'])
	se2 = MarioSegmentNode('Stairs and Enemies', ['S','E'])
	se.add_child(se1)
	se.add_child(se2)
	root.add_child(check_pp)
	root.add_child(se)
	return root

def select_gap_valley():
	root = py_trees.composites.Selector('G or V')
	check_gap = py_trees.composites.Sequence('Check Gap')
	val = py_trees.composites.Sequence('Valleys')
	do_gap = MarioCheckNode('Do Gap?', 'gap_prob')
	g1 = MarioSegmentNode('Gaps',['G'])
	g2 = MarioSegmentNode('Gaps',['G'])
	val1 = MarioSegmentNode('Valleys', ['V'])
	val2 = MarioSegmentNode('Valleys', ['V'])
	check_gap.add_child(do_gap)
	check_gap.add_child(g1)
	check_gap.add_child(g2)
	val.add_child(val1)
	val.add_child(val2)
	root.add_child(check_gap)
	root.add_child(val)
	return root

def get_generator_root():
	root = py_trees.composites.Sequence(name='SMB Level')
	init = MarioSegmentNode('Initial', ['I'])
	pp_se = select_pp_se()
	root.add_child(init)
	root.add_child(pp_se)
	gv = select_gap_valley()
	root.add_child(gv)
	return root

def generate(pp_prob=0.5, gap_prob=0.5, name='smb_level'):
	root = get_generator_root()
	bt = py_trees.trees.BehaviourTree(root)
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='pp_prob',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='gap_prob',access=py_trees.common.Access.WRITE)
	blackboard.pp_prob = pp_prob
	blackboard.gap_prob = gap_prob
	blackboard.x, blackboard.y = 0, 0
	blackboard.level = {}
	root.tick_once()
	level_to_image(blackboard.level, name, 'smb')
	py_trees.display.render_dot_tree(root, name=name + '_tree')

if __name__ == '__main__':
	generate()