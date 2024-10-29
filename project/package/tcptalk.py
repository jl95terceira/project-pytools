import socket
import datetime
import time

def do_it(ip_addr:str,
          port   :int,
          auto   :bool=False):

    port = int(port) if isinstance(port,str) else port
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def send(msg:str):

        msg = (msg+'\n').encode()
        print(f'{datetime.datetime.now().isoformat()} :: {':'.join(map(str,s.getsockname()))}->{':'.join(map(str,s.getpeername()))} :: {msg}')
        s.sendall(msg)

    s.connect((ip_addr,port,))
    empty_count = 0
    if not auto:

        while True:

            if empty_count == 2: break
            if empty_count == 1:

                print('Enter an empty message again to break')

            msg = input(f'>>> ')
            if not msg:

                empty_count += 1
                continue

            empty_count = 0
            send(msg)
    
    else:

        msg = 'Hello, server!'
        print(f'auto = {auto}')
        while True:

            send(msg)
            time.sleep(1)

if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(description='Listen on a given network address and print to the console incoming data')
    p.add_argument('a',
                   help  =f'network address to talk to, in the form {{IP address}}:{{TCP port}}')
    p.add_argument('--auto',
                   help  =f'send messages automatically - useful if the intention is simply to observe at the server-side whether the server is receiving messages (and, thus, functioning)',
                   action='store_true')
    args         = p.parse_args()
    ip_addr,port = args.a.split(':')
    do_it(ip_addr=ip_addr,
          port   =port,
          auto   =args.auto)
