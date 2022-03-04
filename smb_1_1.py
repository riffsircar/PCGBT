import py_trees
from smb_library import *
from smb_helper import *
import json
from PIL import Image

LEVEL = {}
X, Y = 0, 0
verbatim = False

class Initial_Segment(py_trees.behaviour.Behaviour):
	def update(self):
		global LEVEL, X, Y
		#print('init segment')
		LEVEL[(X,Y)] = chunks[0] if verbatim else sample_pattern('I')
		X += 1
		print(LEVEL)
		return py_trees.common.Status.SUCCESS

class Pipes_One(py_trees.behaviour.Behaviour):
	def update(self):
		print('pipes one')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[1] if verbatim else sample_pattern('VP')
		X += 1
		return py_trees.common.Status.SUCCESS

class Pipes_Two(py_trees.behaviour.Behaviour):
	def update(self):
		print('pipes two')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[2] if verbatim else sample_pattern('VP')
		X += 1
		return py_trees.common.Status.SUCCESS

class Pipes_Three(py_trees.behaviour.Behaviour):
	def update(self):
		print('pipes three')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[3] if verbatim else sample_pattern('VP')
		X += 1
		return py_trees.common.Status.SUCCESS

class Risk_Reward(py_trees.behaviour.Behaviour):
	def update(self):
		print('risks reward') 
		global LEVEL, X, Y 
		LEVEL[(X,Y)] = chunks[4] if verbatim else sample_pattern('RR')
		X += 1
		return py_trees.common.Status.SUCCESS

class Enemy_Horde(py_trees.behaviour.Behaviour):
	def update(self):
		print('risks reward')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[5] if verbatim else sample_pattern('E')
		X += 1
		return py_trees.common.Status.SUCCESS

class Triangle(py_trees.behaviour.Behaviour):
	def update(self):
		print('triangle')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[6] if verbatim else sample_pattern('P3')
		X += 1
		return py_trees.common.Status.SUCCESS

class Enemies_Three_Path(py_trees.behaviour.Behaviour):
	def update(self):
		print('enemies 3 path') 
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[7] if verbatim else sample_pattern('E')
		X += 1
		return py_trees.common.Status.SUCCESS

class Stair_Valley(py_trees.behaviour.Behaviour):
	def update(self):
		print('stair valley')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[8] if verbatim else sample_pattern('SV')
		X += 1
		return py_trees.common.Status.SUCCESS

class Stair_Valley_Gap(py_trees.behaviour.Behaviour):
	def update(self):
		print('stair valley gap')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[9] if verbatim else sample_pattern('SVG')
		X += 1
		return py_trees.common.Status.SUCCESS
class Enemies_Two_Path(py_trees.behaviour.Behaviour):
	def update(self):
		print('enemies 2 path')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[10] if verbatim else sample_pattern('P2')
		X += 1
		return py_trees.common.Status.SUCCESS

class Stair_Up(py_trees.behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Stair up")
		self.blackboard.register_key(key='x_cur',access=py_trees.common.Access.WRITE)
		
	def update(self):
		# self.blackboard.x_cur += 1
		print('stair up')
		global LEVEL, X, Y
		LEVEL[(X,Y)] = chunks[11] if verbatim else sample_pattern('SU')
		X += 1
		return py_trees.common.Status.SUCCESS


def create_root_m11():
	root = py_trees.composites.Sequence('Mario 1-1')
	init_and_pipes = py_trees.composites.Sequence('Initial and Pipes')
	multi_paths = py_trees.composites.Sequence('Multiple Paths')
	stairs_and_end = py_trees.composites.Sequence('Ending Stairs')
	initial_segment = Initial_Segment(name="Initial Segment")
	p1 = Pipes_One(name='Pipes 1')
	p2 = Pipes_Two(name='Pipes 2')
	p3 = Pipes_Three(name='Pipes 3')

	rr = Risk_Reward(name='Risk Reward')
	eh = Enemy_Horde(name='Enemy Horde')
	tr = Triangle(name='Triangle')
	ep3 = Enemies_Three_Path(name='Enemies 3-Path')
	#gs = GapSegment(name='Gap Segment')
	pipes_section = py_trees.composites.Sequence('Pipes Section')
	pipes_section.add_child(p1)
	pipes_section.add_child(p2)
	pipes_section.add_child(p3)
	init_and_pipes.add_child(initial_segment)
	init_and_pipes.add_child(pipes_section)
	multi_paths.add_child(rr)
	multi_paths.add_child(eh)
	multi_paths.add_child(tr)
	multi_paths.add_child(ep3)
	#multi_paths.add_child(gs)

	sv = Stair_Valley(name='Stair Valley')
	svg = Stair_Valley_Gap(name='Stair Valley Gap')
	e2p = Enemies_Two_Path(name='Enemies 2 Path')
	su = Stair_Up(name='Stair Up')
	
	stairs_and_end.add_child(sv)
	stairs_and_end.add_child(svg)
	stairs_and_end.add_child(e2p)
	stairs_and_end.add_child(su)
	
	root.add_child(init_and_pipes)
	root.add_child(multi_paths)
	root.add_child(stairs_and_end)
	return root