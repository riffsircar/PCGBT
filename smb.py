import py_trees
from smb_library import *
from smb_helper import *
import json
from PIL import Image

LEVEL = {}
X, Y = 0, 0
verbatim = False

def level_to_image(level):
	width, height = 0, 0
	xs = [x for (x,y) in level]
	ys = [y for (x,y) in level]
	width, height = max(xs), max(ys)
	level_img = Image.new('RGB',((width+1)*(16*16), 15*16))
	print(level_img.size)
	for x,y in level:
		print(x,y)
		lev = level[(x,y)]
		img = Image.new('RGB',(16*16,15*16))
		for row, seq in enumerate(lev):
			for col, tile in enumerate(seq):
				img.paste(images[tile],(col*16,row*16))
		level_img.paste(img,(x*256,y*240))
	level_img.save('test.png')


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

def create_stairs():
	root = py_trees.composites.Sequence('Stairs')
	stairup = StairUpSegment('Stair Up')
	stairvalley = StairValleySegment('Stair Valley')
	root.add_child(stairup)
	root.add_child(stairvalley)
	return root

def create_pipes():
	root = py_trees.composites.Sequence('Pipes')
	pv1 = PipeValleySegment('Pipe Valley')
	pv2 = PipeValleySegment('Pipe Valley')
	pv3 = PipeValleySegment('Pipe Valley')
	root.add_child(pv1)
	root.add_child(pv2)
	root.add_child(pv3)
	return root

def create_stairs_pipes():
	root = py_trees.composites.Sequence('Stairs and Pipes')
	stairs = create_stairs()
	pipes = create_pipes()
	root.add_child(stairs)
	root.add_child(pipes)
	return root

def create_stairs_pipes_enemies():
	root = py_trees.composites.Sequence('Stairs Pipes and Enemy Horde')
	sp = create_stairs_pipes()
	eh = EnemyHordeSegment('Enemy Horde')
	root.add_child(sp)
	root.add_child(eh)
	return root

def multi_path():
	root = py_trees.composites.Sequence('Multiple Paths')
	rr = RiskRewardSegment('Risk Reward')
	ewp = EnemyWithPathsSegment('Enemy with Paths')
	root.add_child(rr)
	root.add_child(ewp)
	return root

def mp_stairs_pipes():
	root = py_trees.composites.Sequence('Paths Stairs and Pipes')
	mp = multi_path()
	sp = create_stairs_pipes()
	root.add_child(mp)
	root.add_child(sp)
	return root

def select_pp_se():
	root = py_trees.composites.Selector('PP or SE')
	check_pp = py_trees.composites.Sequence('Check PP')
	do_pp = DoPathPipe('Do Path-Pipe?')
	pp1 = PathsPipesSegment('Paths and Pipes')
	pp2 = PathsPipesSegment('Paths and Pipes')
	se = py_trees.composites.Sequence('SE')
	se1 = StairsEnemiesSegment('Stairs and Enemies')
	se2 = StairsEnemiesSegment('Stairs and Enemies')
	check_pp.add_child(do_pp)
	check_pp.add_child(pp1)
	check_pp.add_child(pp2)
	se.add_child(se1)
	se.add_child(se2)
	root.add_child(check_pp)
	root.add_child(se)
	return root

def select_gap_valley():
	root = py_trees.composites.Selector('G or V')
	return root

def create_root_generator():
	root = py_trees.composites.Sequence('Level')
	init = InitSegment('Initial')
	pp_se = select_pp_se()
	root.add_child(init)
	root.add_child(pp_se)
	gv = select_gap_valley()
	root.add_child(gv)
	return root

if __name__ == '__main__':
	# root = create_root_m11()
	#root = create_stairs_pipes_enemies()
	root = create_root_generator()
	bt = py_trees.trees.BehaviourTree(root)
	blackboard = py_trees.blackboard.Client()
	blackboard.register_key(key='x',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='y',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='level',access=py_trees.common.Access.WRITE)
	blackboard.register_key(key='pp_prob',access=py_trees.common.Access.WRITE)
	blackboard.pp_prob = 0.5
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
