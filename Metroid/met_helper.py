import sys, os
sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
from py_trees import *
from met_library import *
import random
from PIL import Image

def sample_met(d,dummy1,dummy2):
	if d == 'DR':
		d = 'UDR'
	if d == 'DLR':
		d = 'UDLR'
	if d == 'U':
		d = 'UD'
	levels = dirs[d]
	level = random.choice(levels)
	return chunks[level]