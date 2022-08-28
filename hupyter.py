import sys
import os
import re
import pathlib

arg1 = sys.argv[1]
arg2 = sys.argv[2]

if __name__ == '__main__':
	# make sure the file exists
	assert os.path.exists(arg1), f'The file of {arg1} does not exist'

	notebook_folder_name = re.findall(r'^.+?(?=\/)', arg1)[0] # e.g., 'notebooks'
	files_folder = re.sub('.ipynb', '_files', arg1) # the _files folder auto generated by nbconvert
	# https://stackoverflow.com/a/18710430
	files_folder_name = re.findall(f'^{notebook_folder_name}\/([^\s]+)', files_folder)[0]
	mdfile = re.sub('.ipynb', '.md', arg1) # markdown file name

	move_to = 'content/' + arg2 # where post is located
	static_folder = 'static/' + arg2
	target_static_folder = static_folder + '/' + files_folder_name # the target static folder

	# create path if not existing
	pathlib.Path(move_to).mkdir(parents=True, exist_ok=True) 
	pathlib.Path(target_static_folder).mkdir(parents=True, exist_ok=True) 

	# convert to md
	os.system(f"jupyter nbconvert --to markdown {arg1}")

	# solving mathjax problems
	f = open(mdfile, 'r')
	txt = f.read()
	txt = re.sub(r'\$([^$]*)\$', r'`$\1$`', txt)

	txt = re.sub(r'`\$\$`([^$]*)`\$\$`', r'`$$\1$$`', txt)

	# move files_folder to static folder
	os.system(f'cp -r {files_folder}/* {target_static_folder}')
	os.system(f'rm -rf {files_folder}')

	# https://stackoverflow.com/a/43828391
	md_image_links_raw = re.findall(r'!\[(.*?)\]\((.*?)\)', txt)
	md_image_links = [b for (a,b) in md_image_links_raw]

	for lk in md_image_links:
	    if files_folder_name not in lk:
	        image_folder_name = re.findall(r'^.+?(?=\/)', lk)[0]
	        txt = re.sub(f'{image_folder_name}/', f'/{arg2}/{files_folder_name}/', txt)
	        os.system(f'cp {notebook_folder_name}/{lk} {static_folder}/{files_folder_name}')      

	txt = re.sub(r'\!\[png\]\(', f'![png](/{arg2}/', txt)

	# write to file
	with open(mdfile, 'w') as f:
	    f.write(txt)
	os.system(f'mv {mdfile} {move_to}')