import os, sys

chunks = {}
patterns = {}
chunk_pats = {}

folder = 'smb_chunks_all/'
for file_name in os.listdir(folder):
	level = open(folder + file_name,'r').read().splitlines()
	idx = file_name[file_name.index('_')+1:]
	idx = int(idx[:idx.index('_')])
	pats = file_name[file_name.index('_',7)+1:file_name.index('.')].split('_')
	for pat in pats:
		if pat not in patterns:
			patterns[pat] = []
		patterns[pat].append(idx)
	chunks[idx] = level
	chunk_pats[idx] = pats