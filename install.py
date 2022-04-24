# kicad 5.x library installer from official repositories.

# HELPERS ######################################################################

import os
import sys

from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    WHITE = '\033[1m'
    UNDERLINE = '\033[4m'

def printc(bcolor, text, end='\n'):
    print(bcolor + text + bcolors.ENDC, end=end)
    
def system(cmd):
    printc(bcolors.OKCYAN, cmd)
    return (0 == os.system(cmd))

def sys_exit_error(text = ""):
    sys.exit(bcolors.FAIL + "error: " + text + bcolors.ENDC)

def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)
        
class Lib():
    def __init__(self, dir, listfn):
        self.dir = dir
        self.listfn = listfn

# CONFIG #######################################################################

libs = [
    Lib("kicad-footprints", "fp-lib-table"),
    Lib("kicad-symbols", "sym-lib-table"),
    # Lib("kicad-packages3D", ""),
    # Lib("kicad-templates", "")
]

# SCRIPT #######################################################################
kiCadDir = str(Path.home()) + "\AppData\Roaming\kicad"

try:
    if not system("git submodule update --init --recursive"):
        sys_exit_error()

    for lib in libs:
        prevdir = os.getcwd()
        os.chdir(lib.dir)
        printc(bcolors.OKBLUE, "opening ", end ="")
        printc(bcolors.WHITE, os.getcwd())
        if not system("git checkout master"):
            sys_exit_error()
        if not system("git clean -fdx"):
            sys_exit_error()
        else:
            with open(lib.listfn, 'r') as srcf:
                printc(bcolors.OKBLUE, os.path.realpath(srcf.name))
                # print(srcf.read())
                srcfLines = srcf.readlines()
                for srcfLinesl in srcfLines:
                    pass
                with open(kiCadDir + "\\" + lib.listfn) as dstf:
                    printc(bcolors.OKBLUE, os.path.realpath(dstf.name))
                    # print(dstf.read())
                    dstfLines = dstf.readlines()
                    for dstfLinesl in dstfLines:
                        pass
                    
        os.chdir(prevdir)

except Exception as e: 
    print(e)
    sys_exit_error()

printc(bcolors.OKGREEN, 'great success!')