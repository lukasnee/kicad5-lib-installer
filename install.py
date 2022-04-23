# kicad 5.x library installer from official repositories.

# HELPERS ######################################################################

import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: " , str(sys.argv))

def system(cmd):
    print(cmd)
    return (0 == os.system(cmd))

def print_colored(bcolor, text):
    print(bcolor + text + bcolors.ENDC)
    
# SCRIPT #######################################################################
    
    fn = sys.argv[1]
if os.path.exists(fn):
    print os.path.basename(fn)
    # file exists

kicad_lib_dirs = ["kicad-footprints", "kicad-packages3D", "kicad-symbols", "kicad-templates"]

if not system("git submodule update --init --recursive"):
    sys.exit()

print()
for lib_dir in kicad_lib_dirs:
    if not system("cd %s" % lib_dir):
        sys.exit()
    elif not system("git checkout master"):
        sys.exit()
    elif not system("cd .."):
        sys.exit()

print_colored(bcolors.OKGREEN, 'great success!')