import os.path

TOKENS                       = ('jl95terceira','pytools',)
PROJECT_PATH                 = os.path.split(__file__)[0]
MODULE_PATH                  = os.path.join(PROJECT_PATH, 'project', 'package')
SCRIPTS_INSTALLATION_RELPATH = '-'.join(TOKENS)
PACKAGE                      = '.'.join(TOKENS)

def relpath(path:str):

    return os.path.relpath(path=path, start=PROJECT_PATH)
