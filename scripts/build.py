
import os
import re
from git import Repo

def GetWorkspacePath():
	path = os.environ.get("GITHUB_WORKSPACE")
	if path == None:
		print("Not run on Github Action.")
		os.sys.exit(1)

	return path		

def GetSlcPath():
	path = os.environ.get('SL_SLC_PATH')
	if path == None:
		print('Environment variable SL_SLC_PATH not set.')
		os.sys.exit(1)
	
	return path

def got_simplicity_sdk(slcp_file):
	slc_cli_Path = GetSlcPath()
	with open(slcp_file, "r") as f:
		for line in f:
			if line.find("id: simplicity_sdk") != -1:
				regex = re.findall(r"([\d\.]+)", line)
				if regex:
					simplicity_sdk_version = "v" + regex[0]
					# Check existing and clone
					sdk_dir = os.path.join(GetWorkspacePath(), "sisdk_", simplicity_sdk_version)
					if os.path.isdir(sdk_dir):
						repo = Repo.clone_from(
						'https://github.com/SiliconLabs/simplicity_sdk.git',
						'sisdk_' + str(simplicity_sdk_version) ,
						branch = str(simplicity_sdk_version)
						)
						os.system(slc_cli_Path + " configuration --sdk " + sdk_dir)
						os.system(slc_cli_Path + " signature trust --sdk " + sdk_dir)

					return simplicity_sdk_version

def got_board_id(slcp_file):
	with open(slcp_file, "r") as f:
		for line in f:
			if line.find("id: brd") != -1:
				regex = re.search(r"id:\s+(.*)", line)
				if regex:
					board_id = regex.group(1)
					board_id = board_id.replace("}", "")

					return board_id

def got_wiseconnect3_sdk(slcp_file):
	with open(slcp_file, "r") as f:
		for line in f:
			if line.find("id: wiseconnect3_sdk") != -1:
				regex = re.findall(r"([\d\.]+)", line)
				if regex:
					wiseconnect3_sdk_version = "v" + regex[1]
					
					if os.path.isdir(os.path.join(GetWorkspacePath(), "wiseconnect_" + str(wiseconnect3_sdk_version))) == False:
						repo = Repo.clone_from(
						'https://github.com/SiliconLabs/wiseconnect.git',
						'wiseconnect_' + str(wiseconnect3_sdk_version) ,
						branch = str(wiseconnect3_sdk_version)
						)
					return wiseconnect3_sdk_version

def got_matter_extension(slcp_file):
	with open(slcp_file, "r") as f:
		for line in f:
			if line.find("id: matter") != -1:
				regex = re.findall(r"([\d\.]+)", line)
				if regex:
					matter_ext_version = "v" + regex[0]
					
					if os.path.isdir(os.path.join(GetWorkspacePath(), "matter_extension_" + str(matter_ext_version))) == False:
						repo = Repo.clone_from(
						'https://github.com/SiliconLabsSoftware/matter_extension.git',
						'matter_extension_' + str(matter_ext_version) ,
						branch = str(matter_ext_version)
						)
					return matter_ext_version


def got_tphd_extension(slcp_file):
	with open(slcp_file, "r") as f:
		for line in f:
			if line.find("id: third_party_hw_drivers") != -1:
				regex = re.findall(r"([\d\.]+)", line)
				if regex:
					tphd_ext_version = "v" + regex[0]
					
					if os.path.isdir(os.path.join(GetWorkspacePath(), "tphd_extension_" + str(tphd_ext_version))) == False:
						repo = Repo.clone_from(
						'https://github.com/SiliconLabsSoftware/third_party_hw_drivers_extension.git',
						'tphd_extension_' + str(tphd_ext_version) ,
						branch = str(tphd_ext_version)
						)
					return tphd_ext_version

def got_aiml_extension(slcp_file):
	with open(slcp_file, "r") as f:
		for line in f:
			if line.find("id: aiml") != -1:
				regex = re.findall(r"([\d\.]+)", line)
				if regex:
					aiml_ext_version = "v" + regex[0]
					
					if os.path.isdir(os.path.join(GetWorkspacePath(), "aiml_extension_" + str(aiml_ext_version))) == False:
						repo = Repo.clone_from(
						'https://github.com/SiliconLabsSoftware/aiml-extension.git',
						'aiml_extension_' + str(aiml_ext_version) ,
						branch = str(aiml_ext_version)
						)
					# Initialize and update the submodules
					repo.git.submodule('update', '--init', '--recursive')

					return aiml_ext_version



def add_sdk_extension(sdk_dir, extension , extension_version):
	slc_path = GetSlcPath()
	# Check extension folder existing in sdk folder or not
	extension_folder = extension + "_" + str(extension_version)
	sdk_extension_dir = os.path.join(sdk_dir, "extension", extension_folder)
	if os.path.isdir(sdk_extension_dir) == False:
		os.system(slc_path + " configuration --sdk " + sdk_dir)
		os.system("mkdir -p " + os.path.join(sdk_dir, "extension"))
		os.system("cp -R " + os.path.join(GetWorkspacePath(), extension_folder) + " " + os.path.join(sdk_dir, "extension"))
		os.system(slc_path + " signature trust -extpath " + sdk_extension_dir)






def build_slcp_project(slcp_file):
	print(100*"*")
	print("Building for:", slcp_file)
	print("Project Build ENV:")

	slc_cli_Path = GetSlcPath()
	simplicity_sdk_version = got_simplicity_sdk(slcp_file)
	if simplicity_sdk_version == None:
		print("Error: Could not found sdk version on {}.slcp project".format(slcp_file))
		os.sys.exit(1)
	print("simplicity_sdk version is:", simplicity_sdk_version)
	
	sdk_dir = os.path.join(GetWorkspacePath(), "sisdk_", simplicity_sdk_version)

	wiseconnect3_sdk_version = got_wiseconnect3_sdk(slcp_file)
	if wiseconnect3_sdk_version:
		add_sdk_extension(sdk_dir, "wiseconnect" , wiseconnect3_sdk_version)
		print("wiseconnect3_sdk version is:", wiseconnect3_sdk_version)
	
	matter_ext_version = got_matter_extension(slcp_file)
	if matter_ext_version:
		add_sdk_extension(sdk_dir, "matter_extension" , matter_ext_version)
		print("matter_extension version is:", matter_ext_version)

	tphd_ext_version = got_tphd_extension(slcp_file)
	if tphd_ext_version:
		add_sdk_extension(sdk_dir, "tphd_extension" , tphd_ext_version)
		print("tphd_extension version is:", tphd_ext_version)

	aiml_ext_version = got_aiml_extension(slcp_file)
	if aiml_ext_version:
		add_sdk_extension(sdk_dir, "aiml_extension" , aiml_ext_version)
		print("aiml_extension version is:", aiml_ext_version)

	board_id = got_board_id(slcp_file)
	print("board_id is:", board_id)
	print("\n\n")


	workspace = os.path.join(GetWorkspacePath(), "ws")
	project_name = os.path.basename(slcp_file).replace(".slcp", "")

	if (wiseconnect3_sdk_version != None):
		os.system(slc_cli_Path + " generate --force " + slcp_file + " -cp -np -d " + workspace + " -name={}".format(project_name) + " --with " + '"{};wiseconnect3_sdk"'.format(board_id))
	else:				
		os.system(slc_cli_Path + " generate --force " + slcp_file + " -cp -np -d " + workspace + " -name={}".format(project_name) + " --with=" + board_id)	

	project_mak = workspace + '/{}.Makefile'.format(project_name)
	os.system("cd " + workspace + " && make -f " + project_mak)


###################
def test():
	# slcp_file = "D:/aaa/will_del/fork_aaa/projects/bluetooth/bluetooth_applications/gw/wifi/wifi_ble_gateway/wifi_ble_gateway.slcp"
	slcp_file = "C:/Users/codo/SimplicityStudio/v6_workspace_130/empty/empty.slcp"
	simplicity_sdk_version = got_simplicity_sdk(slcp_file)
	if simplicity_sdk_version == None:
		print("Error: Could not found sdk version on {}.slcp project".format(slcp_file))
		os.sys.exit(1)
	print("simplicity_sdk version is:", simplicity_sdk_version)	
	
	wiseconnect3_sdk_version = got_wiseconnect3_sdk(slcp_file)
	if wiseconnect3_sdk_version:
		# add_sdk_extension(sdk_dir, "wiseconnect" , wiseconnect3_sdk_version)
		print("wiseconnect3_sdk version is:", wiseconnect3_sdk_version)	
	aiml_ext_version = got_aiml_extension(slcp_file)
	if aiml_ext_version:
		# add_sdk_extension(sdk_dir, "aiml_extension" , aiml_ext_version)
		print("aiml_extension version is:", aiml_ext_version)

	matter_ext_version = got_matter_extension(slcp_file)
	if matter_ext_version:
		# add_sdk_extension(sdk_dir, "matter_extension" , matter_ext_version)
		print("matter_extension version is:", matter_ext_version)

	board_id = got_board_id(slcp_file)
	print("board_id is:", board_id)
	print("\n\n")

if __name__ == "__main__":
	# Scan .slcp project file in git change log
	file = open(
		os.path.join(os.environ.get("GITHUB_WORKSPACE"), "solution_list.txt"), "r"
	)
	slcp_project_path_list = []
	for line in file:
		if line.find(".slcp") != -1:
			slcp_project = os.path.join(
				os.environ.get("GITHUB_WORKSPACE"), line.strip()
			)
			slcp_project_path_list.append(slcp_project)

	for slcp_file in slcp_project_path_list:
		build_slcp_project(slcp_file)
