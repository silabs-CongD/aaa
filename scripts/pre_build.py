import os
import sys


def replace_in_file(filename, old_string, new_string):
    # Open the file for reading
    with open(filename, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(old_string, new_string)
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)


def pre_build_cmake():
    # Scan .slcp project file path
    file = open(os.path.join(os.environ.get('GITHUB_WORKSPACE'),
                             "solution_list.txt"), "r")
    slcp_project_path_list = []
    for line in file:
        if line.find(".slcp") != -1:
            slcp_project = os.path.join(os.environ.get('GITHUB_WORKSPACE'),
                                             line.strip())
            slcp_project_path_list.append(slcp_project)

    for slcp_file in slcp_project_path_list:
        project_dir = os.path.dirname(slcp_file)
        project_name = os.path.basename(project_dir)

        pre_build_makefile = os.path.join(os.environ.get('GITHUB_WORKSPACE'),
                                               "scripts/Makefile")
        os.system("cp " + pre_build_makefile + " " + project_dir)
        project_make_path = os.path.join(project_dir, "Makefile")
        # If use Simplicity Studio v6
        if os.path.isdir(os.path.join(project_dir, "cmake_gcc")):
            replace_in_file(project_make_path,
                            'project_name_cmake',
                            str("cmake_gcc"))
        else:
            replace_in_file(project_make_path,
                            'project_name',
                            str(project_name))

        if not os.path.isfile(os.path.join(project_dir, "Makefile")):
            print("Error: Not found Makefile in project folder:", project_dir)
            sys.exit(1)

        # Update root Makefile
        file_path = os.path.join(os.environ.get('GITHUB_WORKSPACE'),
                                 'Makefile')
        string_to_add = "\t${MAKE} -C " + project_dir + \
                        " ${TARGET} TYPE=${TYPE}\n"

        with open(file_path, "a") as file:
            file.write(string_to_add)


if __name__ == "__main__":
    pre_build_cmake()
