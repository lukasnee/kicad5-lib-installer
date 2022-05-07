# Kilibup

Script tool that downloads and links all [official KiCad libraries](https://gitlab.com/kicad/libraries) to your local KiCad installation (library configuration files `*-lib-table`). ATM only the schematic symbol and PCB footprint libararies installation are supported.

## Motivation
I found it very tedious to do this manually using library manager GUI and I couldn't find any help on the internet to speed up this process. So I made this tool. Cheers! 

PS: It's my very first python application. lol.

# Dependencies

- [KiCad](https://www.kicad.org/) v5
- [git](https://git-scm.com/)
- [python](https://www.python.org/downloads/) v3.8.10 or higher

# Usage

```
python kilibup.py -h
usage: kilibup.py [-h] [--sym sym-lib-table] [--fp fp-lib-table] [-s]

kiCad v5 official library unofficial installer

optional arguments:
  -h, --help           show this help message and exit
  --sym sym-lib-table  path to sym-lib-table (KiCad schematic symbols library manager file)
  --fp fp-lib-table    path to fp-lib-table (KiCad PCB footprint library manager file)
  -s                   do not update libraries from remote repository. use local.

example test: python kilibup.py --sym ./tests/sym-lib-table --fp ./tests/fp-lib-table
```

## Example

Windows:
```
python .\kilibup.py --sym C:\Users\Lukas\AppData\Roaming\kicad\sym-lib-table --fp C:\Users\Lukas\AppData\Roaming\kicad\fp-lib-table
```