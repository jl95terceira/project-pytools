import datetime
import socketserver

class ConsoleRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):

        while True:
            
            msg = self.rfile.readline()
            if not msg: break
            print(f'{datetime.datetime.now().isoformat()} :: {':'.join(map(str,self.request.getpeername()))}->{':'.join(map(str,self.request.getsockname()))} :: {msg}')

def do_it(ip_addr:str,
          port   :int):

    port = int(port) if isinstance(port,str) else port
    with socketserver.TCPServer((ip_addr,port,), ConsoleRequestHandler) as server:

        server.serve_forever()

if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(description='Listen on a given network address and print to the console incoming data')
    p.add_argument('a',
                   help  =f'network address to listen on, in the form {{IP address}}:{{TCP port}}')
    args         = p.parse_args()
    ip_addr,port = args.a.split(':')
    do_it(ip_addr=ip_addr,port=port)
