# kicad 5.x library installer from official repositories.
from pathlib import Path
import re
import sys
import os

test = False
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


def printc(bcolor, text, end='\n'):
    print(bcolor + text + bcolors.ENDC, end=end)


def system(cmd):
    printc(bcolors.OKCYAN, cmd)
    return (0 == os.system(cmd))


def sys_exit_error(text=""):
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


def return_first_match(regex, text):
    try:
        result = re.findall(regex, text)[0]
    except IndexError:
        result = ''
    return result

# CONFIG #######################################################################


libs = [
    Lib("kicad-footprints", "fp-lib-table"),
    Lib("kicad-symbols", "sym-lib-table"),
    # Lib("kicad-packages3D", ""),
    # Lib("kicad-templates", "")
]

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
        printc(bcolors.YELLOW, "updating %s manager from" % lib.dir, end=" ")
        printc(bcolors.WHITE, os.getcwd())
        if not system("git checkout master"):
            sys_exit_error()
        if not system("git clean -fdx"):
            sys_exit_error()
        else:
            with open(lib.listfn, 'r') as srcf:
                printc(bcolors.YELLOW, "src:", end=" ")
                printc(bcolors.WHITE, os.path.realpath(srcf.name))
                srclines = srcf.readlines()
                dstPath = kiCadDir + "\\" + lib.listfn
                with open(dstPath, 'r') as dstf:
                    printc(bcolors.YELLOW, "dst:", end=" ")
                    printc(bcolors.WHITE, os.path.realpath(dstf.name))
                    dstlines = dstf.readlines()
                    for srcline in srclines:
                        regexSrc = '\(name "?(\w+)"?\)*'
                        libName = return_first_match(regexSrc, srcline)
                        if libName:
                            regexDst = '\(name "?(' + libName + ')"?\)*'
                            isAlreadyPresent = False
                            for dstline in dstlines:
                                if bool(re.search(regexDst, dstline)):
                                    isAlreadyPresent = True
                            if not isAlreadyPresent:
                                dstlines.insert(1, srcline)
                    with open(dstPath, "w") as f:
                        dstlines = "".join(dstlines)
                        f.write(dstlines)
        os.chdir(prevdir)

except Exception as e:
    print(e)
    sys_exit_error()

printc(bcolors.OKGREEN, 'great success!')
