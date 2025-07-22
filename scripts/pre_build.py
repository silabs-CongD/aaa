import os
import sys

# Scan .slcp file path
file = open(os.path.join(os.environ.get('GITHUB_WORKSPACE'), "git_diff.txt"), "r")
slcp_project_path_list = []
for line in file:
	if line.find(".slcp") != -1:
		slcp_project_path = os.path.join(os.environ.get('GITHUB_WORKSPACE'), line.strip())
		slcp_project_path_list.append(slcp_project_path)


# Add Makefile into project folder
def replace_in_file(filename, old_string, new_string):
	# Open the file for reading
	with open(filename, 'r') as file:
		filedata = file.read()
	
	# Replace the target string
	filedata = filedata.replace(old_string, new_string)
	
	# Write the file out again
	with open(filename, 'w') as file:
		file.write(filedata)

for slcp_file in slcp_project_path_list:
	project_dir = os.path.dirname(slcp_project_path)
	project_name = os.path.basename(project_dir)

	pre_build_makefile_path = os.path.join(os.environ.get('GITHUB_WORKSPACE'), "scripts/Makefile")
	replace_in_file(pre_build_makefile_path, 'project_name', str(project_name))
	os.system("cp " + pre_build_makefile_path + " " + project_dir)
	if not os.path.isfile(os.path.join(project_dir, "Makefile")):
		print("Error: Not found Makefile in project folder:", project_dir)
		sys.exit(1)

	# Update root Makefile
	file_path = os.path.join(os.environ.get('GITHUB_WORKSPACE') ,'Makefile')
	string_to_add = "\t${MAKE} -C " + project_dir + " ${TARGET} TYPE=${TYPE}\n"

	with open(file_path, "a") as file:
		file.write(string_to_add)

	# replace_in_file(os.path.join(os.environ.get('GITHUB_WORKSPACE') ,'Makefile'), 'project_dir', str(project_dir))
