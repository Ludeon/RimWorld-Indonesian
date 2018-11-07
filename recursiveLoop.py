import os
import sys

walk_dir = sys.argv[1]

print('walk_dir = ' + walk_dir)

def list_files(startpath):
	txt = ""
	for root, dirs, files in os.walk(startpath):
		level = root.replace(startpath, '').count(os.sep)
		indent = ' ' * 2 * (level)
		printout = ('{}- [ ] {}/'.format(indent, os.path.basename(root)))
		print(printout)
		txt += printout + '\n'
		subindent = ' ' * 2 * (level + 1)
		for f in files:
			printout = ('{}- [ ] {}'.format(subindent, f))
			print(printout)
			txt += printout + '\n'
	
	f = open("directory.txt", "w")
	f.write(txt)
	
list_files(walk_dir)