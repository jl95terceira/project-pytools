import ssl

import websockets.sync.client

def do_it(url     :str,
          use_ssl :bool=False,
          auto_ssl:bool=False,
          protocol:ssl._SSLMethod=None):

    if auto_ssl:
        
        use_ssl = url.startswith('wss')

    with websockets.sync.client.connect(url)                                                                                                 if not use_ssl else \
         websockets.sync.client.connect(url,ssl_context=ssl.SSLContext(protocol=protocol if protocol is not None else ssl.PROTOCOL_TLSv1_2)) as websocket:

        while (True):
            
            message = websocket.recv()
            print(f"Received: {message}")

if __name__ == '__main__':

    import argparse

    SSL_PROTOCOL_VERSION_DICT = {

        **{v:ssl.PROTOCOL_TLSv1 for v in ('1',
                                          '1.0')},
        '1.1' :ssl.PROTOCOL_TLSv1_1,
        '1.2' :ssl.PROTOCOL_TLSv1_2,
    }
    SSL_PROTOCOL_VERSION_DEFAULT = object()
    
    p = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                description    ='Connect to a websocket server')
    p.add_argument('addr', 
                   help='websocket server network address')
    p.add_argument('--ssl', 
                   help   ='force assume SSL and, if a value is given, assume the value as the SSL protocol version (default = \'1.2\')\nThis option is mutually exclusive with option \'--nossl\'.',
                   nargs  ='?',
                   default=None,
                   const  =SSL_PROTOCOL_VERSION_DEFAULT)
    p.add_argument('--nossl',
                   help  ='force assume no SSL\nThis option is mutually exclusive with option \'--ssl\'.',
                   action='store_true')
    args = p.parse_args()
    if args.ssl is not None and args.nossl:

        emsg = 'options --ssl and --nossl are mutually exclusive'
        raise Exception(emsg)

    do_it(url     =args.addr,
          protocol=None if args.ssl is None else SSL_PROTOCOL_VERSION_DICT[args.ssl] if args.ssl is not SSL_PROTOCOL_VERSION_DEFAULT else None,
          auto_ssl=args.ssl is     None and not args.nossl,
          use_ssl =args.ssl is not None or  not args.nossl)
