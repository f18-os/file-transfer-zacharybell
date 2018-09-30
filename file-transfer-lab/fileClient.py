import socket

FILE_PATH = 'foo.txt'
ADDR      = ('127.0.0.1', 1234)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect(ADDR)
        with open(FILE_PATH, 'rb') as f:
            soc.sendfile(f)
except:
    print('Something bad happened! Terminating gracefully..')