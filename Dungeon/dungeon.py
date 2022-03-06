import sys
sys.path.append('..')
from py_trees import *
from PIL import Image
import random, sys
from dungeon_helper import *
from Metroid import *

CLOSED, OPEN, DOOR = 'closed','open', 'door'
NORTH, SOUTH, EAST, WEST = 'north','south','east','west'
DIRS = [NORTH, SOUTH, EAST, WEST]
N = 5
GAME = 'zelda' # zelda, met
dims = (15,16) if GAME == 'met' else (11,16)

def neighbor(cell, dr):
	if dr == NORTH:
		return (cell[0], cell[1] - 1)
	elif dr == SOUTH:
		return (cell[0], cell[1] + 1)
	elif dr == EAST:
		return (cell[0] + 1, cell[1])
	elif dr == WEST:
		return (cell[0] - 1, cell[1])
	else:
		raise RuntimeError('invalid direction')

def opposite(dr):
	if dr == NORTH:
		return SOUTH
	elif dr == SOUTH:
		return NORTH
	elif dr == EAST:
		return WEST
	elif dr == WEST:
		return EAST
	else:
		raise RuntimeError('invalid direction')

class StartRoom(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name="Start")
		self.blackboard.register_key(key='cell',access=common.Access.WRITE)
		self.blackboard.register_key(key='dir',access=common.Access.WRITE)
		self.blackboard.register_key(key='layout',access=common.Access.WRITE)
		self.blackboard.register_key(key='started',access=common.Access.WRITE)
	def update(self):
		d = random.choice(DIRS)
		self.blackboard.layout[self.blackboard.cell] = {}
		for dir in DIRS:
			self.blackboard.layout[self.blackboard.cell][dir] = CLOSED
		self.blackboard.started = True
		return common.Status.SUCCESS

class PlaceRoom(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='cell',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='layout',access=common.Access.WRITE)
		self.blackboard.register_key(key='generated',access=common.Access.WRITE)
		
	def update(self):
		cells = list(self.blackboard.layout.keys())
		options = []
		for cell in cells:
			for dr in DIRS:
				nbr = neighbor(cell, dr)
				print(cell)
				if self.blackboard.layout[cell][dr] == CLOSED:
					if nbr not in self.blackboard.layout:
						options.append((cell,dr))
		self.blackboard.cell, self.blackboard.dr = random.choice(options)
		self.blackboard.generated += 1
		print('incremented generated', self.blackboard.generated)
		return common.Status.SUCCESS

class ConnectRoom(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='cell',access=common.Access.WRITE)
		self.blackboard.register_key(key='dr',access=common.Access.WRITE)
		self.blackboard.register_key(key='layout',access=common.Access.WRITE)
		
		
	def update(self):
		nbr = neighbor(self.blackboard.cell,self.blackboard.dr)
		opp = opposite(self.blackboard.dr)

		self.blackboard.layout[self.blackboard.cell][self.blackboard.dr] = OPEN

		if nbr not in self.blackboard.layout:
			self.blackboard.layout[nbr] = {}
			for dr in DIRS:
				self.blackboard.layout[nbr][dr] = CLOSED
		
		self.blackboard.layout[nbr][opp] = OPEN
		return common.Status.SUCCESS

class CheckNumRooms(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='n',access=common.Access.READ)
		self.blackboard.register_key(key='generated',access=common.Access.READ)
		
	def update(self):
		print('Generated: ', self.blackboard.generated)
		print('N: ', self.blackboard.n)
		if self.blackboard.generated < self.blackboard.n:
			print('generating more')
			return common.Status.FAILURE
		print('stopping generation')
		return common.Status.SUCCESS

class CheckStart(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='started',access=common.Access.READ)
		
	def update(self):
		if self.blackboard.started:
			return common.Status.SUCCESS
		return common.Status.FAILURE

class SetNumRooms(behaviour.Behaviour):
	def __init__(self,name):
		super().__init__(name=name)
		self.blackboard = self.attach_blackboard_client(name=name)
		self.blackboard.register_key(key='n',access=common.Access.WRITE)
		
	def update(self):
		self.blackboard.n = random.randint(5,10)
		print('N: ', self.blackboard.n)
		return common.Status.SUCCESS
		
def generate_more():
	root = composites.Selector('Generate More?')
	check = CheckNumRooms('CheckNumRooms')
	gr = generate_room()
	root.add_child(check)
	root.add_child(gr)
	return root

def is_start():
	root = composites.Selector('Started?')
	check = CheckStart('CheckStart')
	start = StartRoom('Generate Start Room')
	root.add_child(check)
	root.add_child(start)
	return root

def generate_dungeon():
	root = composites.Sequence('Generate Dungeon')
	n = SetNumRooms('Set Num Rooms')
	gr = generate_rooms()
	root.add_child(n)
	root.add_child(gr)
	return root

def generate_room():
	root = composites.Sequence('Generate Room')
	pr = PlaceRoom('Place Room')
	cr = ConnectRoom('Connect Room')
	root.add_child(pr)
	root.add_child(cr)
	return root

def generate_rooms():
	root = composites.Sequence('Generate Rooms')
	#n = SetNumRooms('Set Num Rooms')
	#bb.register_key(key='n',access=common.Access.READ)
	for _ in range(N):
		pr = PlaceRoom('Place Room')
		cr = ConnectRoom('Connect Room')
		root.add_child(pr)
		root.add_child(cr)
	return root

if __name__=='__main__':
	root = composites.Sequence('Dungeon')
	blackboard = blackboard.Client()
	blackboard.register_key(key='cell',access=common.Access.WRITE)
	blackboard.register_key(key='dr',access=common.Access.WRITE)
	blackboard.register_key(key='layout',access=common.Access.WRITE)
	blackboard.register_key(key='generated',access=common.Access.WRITE)
	blackboard.register_key(key='n',access=common.Access.WRITE)
	blackboard.register_key(key='started',access=common.Access.WRITE)
	blackboard.started = False
	blackboard.generated = 0
	blackboard.n = random.randint(10,15)
	blackboard.cell = (0,0)
	blackboard.layout = {}
	start = is_start()
	more = generate_more()
	#dung = generate_dungeon()
	root.add_child(start)
	root.add_child(more)
	display.render_dot_tree(root)
	while blackboard.generated < blackboard.n:
		print('Generated ',blackboard.generated)
		root.tick_once()
	#print(blackboard.layout)
	cells = list(blackboard.layout.keys())
	x_lo = min(cells)[0]
	x_hi = max(cells)[0]
	y_lo = min(cells, key=lambda x: x[1])[1]
	y_hi = max(cells, key=lambda x: x[1])[1]
	width, height = abs(x_lo - x_hi)+1, abs(y_hi - y_lo)+1
	x_adj, y_adj = abs(x_lo * 256 - 0), abs((y_lo * dims[0] * 16) - 0)
	print(width, height)
	#print(x_adj, y_adj)
	layout_img = Image.new('RGB',(width*256, height*(dims[0]*16)))

	for y in range(y_lo, y_hi + 1):
		line = ''
		for x in range(x_lo, x_hi + 1):
			cell = (x, y)
			if cell not in blackboard.layout:
				line += '   '
			else:
				line += '┌'
				if (blackboard.layout[cell][NORTH] == CLOSED):
					line += '─'
				elif (blackboard.layout[cell][NORTH] == DOOR):
					line += '.'
				else:
					line += ' '
				line += '┐'
		print(line)

		line = ''
		for x in range(x_lo, x_hi + 1):
			cell = (x, y)
			if cell not in blackboard.layout:
				line += '   '
			else:
				if (blackboard.layout[cell][WEST] == CLOSED):
					line += '│'
				elif (blackboard.layout[cell][WEST] == DOOR):
					line += '.'
				else:
					line += ' '
				line += ' '
				if (blackboard.layout[cell][EAST] == CLOSED):
					line += '│'
				elif (blackboard.layout[cell][EAST] == DOOR):
					line += '.'
				else:
					line += ' '
		print(line)

		line = ''
		for x in range(x_lo, x_hi + 1):
			cell = (x, y)
			if cell not in blackboard.layout:
				line += '   '
			else:
				line += '└'
				if (blackboard.layout[cell][SOUTH] == CLOSED):
					line += '─'
				elif (blackboard.layout[cell][SOUTH] == DOOR):
					line += '.'
				else:
					line += ' '
				line += '┘'
		print(line)
	layout = blackboard.layout
	sample = sample_met if GAME == 'metroid' else sample_dir
	images = met_images if GAME == 'metroid' else zelda_images
	for key in layout:
		x, y = key
		cell = layout[key]
		label = ''
		if cell['north'] in ['open','door']:
			label += 'U'
		if cell['south'] in ['open','door']:
			label += 'D'
		if cell['west'] in ['open','door']:
			label += 'L'
		if cell['east'] in ['open','door']:
			label += 'R'

		level = sample(label)
		img = Image.new('RGB',(16*16,dims[0]*16))
		for row, seq in enumerate(level):
			for col, tile in enumerate(seq):
				img.paste(images[tile],(col*16,row*16))
		x_pos, y_pos, x_del, y_del = (x*256)+x_adj, (y*dims[0]*16)+y_adj, 16*16, dims[0]*16
		layout_img.paste(img, (x_pos,y_pos))
		layout_img.save('dung_met.png')
