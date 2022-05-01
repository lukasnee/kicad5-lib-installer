# kicad 5.x library installer from official repositories.
from pathlib import Path
import re
import sys
import os
import colorama
from colorama import Fore


# HELPERS ######################################################################


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    WHITE = '\033[1m'
    UNDERLINE = '\033[4m'


def printc(color, text, end='\n'):
    print(color + text + Fore.RESET, end=end)


def system(cmd):
    printc(Fore.CYAN, cmd)
    return (0 == os.system(cmd))


def sys_exit_error(text=""):
    sys.exit(Fore.RED + "error: " + text + Fore.RESET)


def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


class Lib():
    def __init__(self, dir, listfn, pathVar):
        self.dir = dir
        self.listfn = listfn
        self.pathVar = pathVar


def return_first_match(regex, text):
    try:
        result = re.findall(regex, text)[0]
    except IndexError:
        result = ''
    return result

# CONFIG #######################################################################


libs = [
    Lib("kicad-footprints", "fp-lib-table", r'${KICAD6_FOOTPRINT_DIR}'),
    Lib("kicad-symbols", "sym-lib-table", r'${KICAD6_SYMBOL_DIR}'),
    # Lib("kicad-packages3D", ""),
    # Lib("kicad-templates", "")
]

reName = r'\(name "?(\w+)"?\)*'
test = False

# SCRIPT #######################################################################
kiCadDir = str(Path.home()) + "\AppData\Roaming\kicad"
if test:
    kiCadDir = "..\\tests"

try:
    if not system("git submodule update --init --recursive"):
        sys_exit_error()

    for lib in libs:
        prevdir = os.getcwd()
        os.chdir(lib.dir)
        printc(Fore.YELLOW, "updating %s manager from" % lib.dir, end=" ")
        printc(Fore.WHITE, os.getcwd())
        if not system("git fetch -all"):
            sys_exit_error()
        if not system("git checkout master"):
            sys_exit_error()
        if not system("git clean -fdx"):
            sys_exit_error()
        if not system("git fetch"):
            sys_exit_error()
        if not system("git pull"):
            sys_exit_error()
        else:
            with open(lib.listfn, 'r') as srcf:
                srcPath = os.path.realpath(srcf.name)
                libPath = os.path.split(srcPath)[0] + '\\'
                printc(Fore.YELLOW, "src:", end=" ")
                printc(Fore.WHITE, srcPath)
                dstPath = kiCadDir + "\\" + lib.listfn
                with open(dstPath, 'r') as dstf:
                    printc(Fore.YELLOW, "dst:", end=" ")
                    printc(Fore.WHITE, os.path.realpath(dstf.name))
                    dstlines = dstf.readlines()
                    for srcline in srcf.readlines():
                        libName = return_first_match(reName, srcline)
                        if libName != "":
                            libNotPresentInList = True
                            dstLineNum = 0
                            for dstline in dstlines:
                                if libName == return_first_match(reName, dstline):
                                    srcline = srcline.replace(
                                        lib.pathVar, libPath)
                                    # update same
                                    dstlines[dstLineNum] = srcline
                                    libNotPresentInList = False
                                    break
                                dstLineNum += 1
                            if libNotPresentInList:
                                srcline = srcline.replace(lib.pathVar, libPath)
                                # insert in top of list
                                dstlines.insert(1, srcline)
                    with open(dstPath, "w") as f:
                        dstlines = "".join(dstlines)
                        f.write(dstlines)
        os.chdir(prevdir)

except Exception as e:
    print(e)
    sys_exit_error()

printc(Fore.GREEN, 'great success!')
