import argparse
import os
import subprocess
import typing

def do_it(wd:str,
          command:str|typing.Iterable[str],
          depth:int|None=1):
    
    if depth is not None and depth <= 0:
        return
    curwd = os.getcwd()
    os.chdir(wd)
    try: 
        for root, dirs, files in os.walk('.', topdown=True):
            for dir in dirs:
                try:
                    os.chdir(os.path.join(root, dir))
                except: continue
                try:
                    print(os.getcwd())
                    if isinstance(command, str):
                        os.system(command)
                    else:
                        subprocess.run(list(command), shell=True)
                    if depth is None or 1 < depth:
                        do_it(wd=os.getcwd(),
                            command=command,
                            depth=None if depth is None else depth - 1)
                finally:
                    os.chdir('..')
    finally:
        os.chdir(curwd)

def main():

    ap = argparse.ArgumentParser(description='Run command on directories recursively',
                                 formatter_class=argparse.RawTextHelpFormatter)
    class A:
        WD = 'wd'
        DEPTH = 'depth'
        NO_DEPTH = 'no-depth'
        COMMAND = 'cmd'
    class Defaults:
        DEPTH = 1
    ap.add_argument(f'--{A.WD}', 
                    help='working directory')
    depth_args = ap.add_mutually_exclusive_group()
    depth_args.add_argument(f'--{A.DEPTH}','-d',
                            type=int,
                            help=f'maximum recursion depth\nDefault: {repr(Defaults.DEPTH)}',
                            default=Defaults.DEPTH)
    depth_args.add_argument(f'--{A.NO_DEPTH}',
                            help='no recursion depth limit',
                            action='store_true')
    ap.add_argument(f'{A.COMMAND}', 
                    nargs=argparse.REMAINDER,
                    help='command to run on each directory')
    get = ap.parse_args().__getattribute__
    wd      :str  = get(A.WD) if get(A.WD) is not None else os.getcwd()
    command :typing.Iterable[str] = get(A.COMMAND)
    no_depth:bool = get(A.NO_DEPTH.replace('-','_'))
    depth   :int  = get(A.DEPTH)
    do_it(wd     =wd,
          command=command,
          depth  =depth if not no_depth else None)

if __name__ == '__main__': main()