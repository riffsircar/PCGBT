import os, sys

chunks = {}
dirs = {}
chunk_dir = {}
path = os.path.dirname(__file__)
folder = path + '/met_chunks_all/'
for i, file_name in enumerate(os.listdir(folder)):
	level = open(folder + file_name,'r').read().splitlines()
	sub1 = file_name[file_name.index('_')+1:]
	sub2 = sub1[sub1.index('_')+1:]
	sub3 = sub2[sub2.index('_')+1:]
	idx = int(sub3[:sub3.index('_')])
	d = sub3[sub3.index('_')+1:sub3.index('.')]
	if d not in dirs:
		dirs[d] = []
	dirs[d].append(i)
	chunks[i] = level
	chunk_dir[i] = d


print(dirs.keys())