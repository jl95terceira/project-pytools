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

    ap = argparse.ArgumentParser(description='Run command on directories recursively')
    class A:
        WD = 'wd'
        DEPTH = 'depth'
        COMMAND = 'cmd'
    ap.add_argument(f'--{A.WD}', 
                    help='working directory')
    ap.add_argument(f'--{A.DEPTH}', 
                    type=int,
                    help='maximum recursion depth',
                    default=None)
    ap.add_argument(f'{A.COMMAND}', 
                    nargs=argparse.REMAINDER,
                    help='command to run on each directory')
    get = ap.parse_args().__getattribute__
    wd     :str = get(A.WD) if get(A.WD) is not None else os.getcwd()
    command:typing.Iterable[str] = get(A.COMMAND)
    depth  :int|None = get(A.DEPTH)
    do_it(wd=wd,
          command=command,
          depth=depth)

if __name__ == '__main__': main()