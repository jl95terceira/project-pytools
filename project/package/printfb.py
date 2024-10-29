if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                description    =f'Print the contents of a file (binary / no encoding)\nThis tool is especially useful to find pesky carriage returns ({repr('\r')}).')
    p.add_argument('f',
                   help='file name')
    args = p.parse_args()
    # do it
    with open(args.f, 'rb') as f:

        print(f.read())    

