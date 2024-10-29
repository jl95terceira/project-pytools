import os
import os.path
import re
import typing
import paramiko

def do_it(path_src    :str,
          fn_filter   :typing.Callable[[str],bool],
          ssh_ip_addr :str,
          ssh_port    :int,
          ssh_username:str,
          ssh_password:str,
          path_dst    :str):
    
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    c.connect(hostname=ssh_ip_addr, port=ssh_port, username=ssh_username, password=ssh_password)
    fc = c.open_sftp()
    if os.path.isdir(path_src):

        for dp,rdnn,rfnn in os.walk(path_src):

            for rfn in rfnn:

                rfn_src = os.path.relpath(path=os.path.join(dp, rfn), start=path_src)
                if not fn_filter(rfn_src): continue
                fn_src  = os.path.join(path_src,rfn_src)
                pad     = ' '*(max((0,40-len(fn_src),)))
                fn_dst  = '/'.join(os.path.join(path_dst, rfn_src).split(os.path.sep))
                print(f'Copy from local {repr(fn_src)}{(pad)} to remote {repr(fn_dst)}', end='')
                fn_dst_tokens = fn_dst.split('/')
                for i in range(len(fn_dst_tokens)-1):

                    try: fc.mkdir('/'.join(fn_dst_tokens[:1+i]))
                    except: pass

                try:
                
                    fc.put(localpath=fn_src, remotepath=fn_dst)

                except Exception as e: print(f'{pad} - {e}')
                else:                  print('')
            
    else:

        pass

if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(description='Copy files to a remote directory via FTP / SSH')
    p.add_argument('spath',
                   help='source (local) path')
    p.add_argument('--fre',
                   help='source (local) file name regex, to filter files to copy')
    p.add_argument('daddr',
                   help='destination (remote) SSH address in form \'{ip address}:{port}\'')
    p.add_argument('duser',
                   help='destination (remote) user name')
    p.add_argument('dpass',
                   help='destination (remote) password')
    p.add_argument('dpath',
                   help='destination (remote) path')
    args = p.parse_args()
    # do it
    ip_addr,port = (lambda a,b: (a, int(b)))(*map(str.strip, args.daddr.split(':')))
    print([ip_addr, port])
    do_it(path_src    =args.spath,
         fn_filter   =lambda fn: (re.search(pattern=args.fre,string=fn)) if args.fre is not None else lambda fn: True,
         ssh_ip_addr =ip_addr,
         ssh_port    =port,
         ssh_username=args.duser,
         ssh_password=args.dpass,
         path_dst    =args.dpath)