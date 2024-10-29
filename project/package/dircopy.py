import os.path
import shutil

from batteries import *

def main(src:str,
         dst:str):
    
    shutil.copytree(src=src,dst=dst)

if __name__ == '__main__':

    import argparse
    
    class A:

        SOURCE      = 's'
        DESTINATION = 'd'

    p = argparse.ArgumentParser(description='Copy a directory')
    p.add_argument(f'{A.SOURCE}',
                   help='source directory')
    p.add_argument(f'{A.DESTINATION}',
                   help='destination directory')
    get = agetter(p.parse_args())
    main(src=get(A.SOURCE),
         dst=get(A.DESTINATION))
