from pathlib import Path
import re
import sys
import os
import argparse
import shutil


class Fore:
    RESET = '\x1b[0m'
    WHITE = '\x1b[37m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'


def print_colored(color, text, end='\n'):
    print(color + text + Fore.RESET, end=end)


def system_call(cmd):
    print("invoking '{cmd}'".format(cmd=cmd))
    if os.system(cmd) != 0:
        raise Exception('{cmd} failed executing'.format(cmd))


def exec_sys_script(cmd_arr):
    for cmd in cmd_arr:
        system_call(cmd)


def return_first_match(regex, text):
    try:
        result = re.findall(regex, text)[0]
    except IndexError:
        result = ''
    return result


class Lib():
    def __init__(self, name, src_path, dst_path, dir_regex):
        self.name = name
        self.src_path = src_path
        self.dst_path = dst_path
        self.dir_regex = dir_regex

    def git_reset_latest_master(self):
        git = "git --git-dir={dir}/.git --work-tree={dir} ".format(
            dir=os.path.dirname(self.src_path))
        sys_script = [
            "git submodule update {submodule}".format(
                submodule=os.path.dirname(self.src_path)),
            git + "fetch --all",
            git + "checkout master",
            git + "clean -fdx",
            git + "fetch",
            git + "pull"
        ]
        exec_sys_script(sys_script)

    # def update_library_manager:


parser = argparse.ArgumentParser(
    description='KiCad v6 (or v5) official libraries update script', epilog="example test: git restore tests/*; python kilibup.py --sym ./tests/sym-lib-table --fp ./tests/fp-lib-table")
parser.add_argument('-v', type=int, choices=[5, 6], default=6,
                    help='Your KiCad version to update. Version 6 by default')
parser.add_argument('--sym', type=str,
                    metavar="sym-lib-table", required=False, help='custom path to sym-lib-table (KiCad schematic symbols library manager file). If used, -v flag can be ingored')
parser.add_argument('--fp', type=str,
                    metavar="fp-lib-table", required=False, help='custom path to fp-lib-table (KiCad PCB footprint library manager file). If used, -v flag can be ingored')
parser.add_argument('-s', action='store_true',
                    help='do not update libraries repositories from remote')
args = parser.parse_args()

if not args.sym:
    if args.v == 5:
        args.sym = str(Path.home()) + "/AppData/Roaming/kicad/sym-lib-table"
    elif args.v == 6:
        args.sym = str(Path.home()) + \
            "/AppData/Roaming/kicad/6.0/sym-lib-table"

if not args.fp:
    if args.v == 5:
        args.fp = str(Path.home()) + "/AppData/Roaming/kicad/fp-lib-table"
    elif args.v == 6:
        args.fp = str(Path.home()) + "/AppData/Roaming/kicad/6.0/fp-lib-table"

libs = [
    Lib("PCB footprints", "kicad-footprints/fp-lib-table",
        args.fp, r'${KICAD6_FOOTPRINT_DIR}/'),
    Lib("schematic symbols", "kicad-symbols/sym-lib-table",
        args.sym, r'${KICAD6_SYMBOL_DIR}/'),
    # TODO: kicad-packages3D
    # TODO:kicad-templates
]

libs_updated_cnt = 0

for lib in libs:

    if lib.dst_path:

        print_colored(Fore.YELLOW, "updating {lib_name} library manager".format(
            lib_name=os.path.basename(lib.name)))

        if not args.s:
            print_colored(
                Fore.YELLOW, "making sure you have latest library repository...")
            lib.git_reset_latest_master()

        backup_path = lib.dst_path + "." + \
            os.path.basename(sys.argv[0]) + ".bak"
        print_colored(Fore.YELLOW, "backing up {backup_path}".format(
            backup_path=backup_path))
        shutil.copyfile(lib.dst_path, lib.dst_path + ".bak")

        with open(lib.src_path, 'r') as f:
            print_colored(Fore.YELLOW, "src_file: " + lib.src_path)
            src_lines = f.readlines()

        with open(lib.dst_path, 'r') as f:
            print_colored(Fore.YELLOW, "dst_file: " + lib.dst_path)
            dst_lines = f.readlines()

        updated_cnt = 0
        added_cnt = 0

        print_colored(Fore.YELLOW, "scanning libraries:")

        for src_line in src_lines:
            re_name = r'\(\s*name\s+"?(?P<name>[\w\-\.\+]+)"?\s*\)'
            lib_name = return_first_match(re_name, src_line)
            if lib_name:
                new_line = src_line.replace(
                    lib.dir_regex, (os.path.realpath(os.path.dirname(lib.src_path)) + '/').replace('\\', '/'))
                lib_already_present_in_dst = False
                dst_line_num = 0
                for dst_line in dst_lines:
                    if lib_name == return_first_match(re_name, dst_line):
                        if(new_line == dst_line):
                            print_colored(Fore.WHITE, lib_name, end=' ')
                        else:
                            print_colored(Fore.YELLOW, lib_name, end=' ')
                            dst_lines[dst_line_num] = new_line
                            updated_cnt += 1
                        lib_already_present_in_dst = True
                        break
                    dst_line_num += 1
                if not lib_already_present_in_dst:
                    print_colored(Fore.GREEN, lib_name, end=' ')
                    dst_lines.insert(1, new_line)
                    added_cnt += 1
        with open(lib.dst_path, "w") as f:
            dst_lines = "".join(dst_lines)
            f.write(dst_lines)
        print_colored(Fore.YELLOW, "\n{added_cnt} libraries added and {updated_cnt} libraries updated".format(
            added_cnt=added_cnt, updated_cnt=updated_cnt))

        libs_updated_cnt += 1

if not libs_updated_cnt:
    print_colored(
        Fore.YELLOW, "nothing to update. Please provide destination map file(s) - see help with '-h'")
else:
    print_colored(
        Fore.YELLOW, 'NOTE: do not delete kilibup repo because it contains the actual libraries that are linked to your KiCad')
    print_colored(Fore.GREEN, 'all done!')
