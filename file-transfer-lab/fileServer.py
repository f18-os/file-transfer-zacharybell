import os, socket, sys, re

STORE = 'client_uploads'
ADDR  = ('127.0.0.1', 1234)

def extract_number(file_name, inc_reg=r'_(\d+)\.txt'):
    match = re.search(inc_reg, file_name)
    if match:
        return int(match)
    return -1

try:
    # creates a directory to store the client uploads if one doesn't exist
    if not os.path.exists(STORE):
        os.makedirs(STORE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsoc: 
        lsoc.bind(ADDR)
        lsoc.listen(5)
        
        while True:
            soc, addr = lsoc.accept()

            if not os.fork():
                print('new child', addr)
                client_id    = "{0}:{1}".format(addr[0], addr[1])

                # creates a list of all the file numbers for a particular client (i.e. IP:PORT from client)
                max_upload = [ extract_number(f) for f in os.listdir(STORE) if re.match(client_id, f) ]
                
                # gets the maximum file number for the client so that the uploads don't overwrite
                max_file_number = -1 
                if max_upload:
                    max_file_number = max(max_upload)

                file_name = '{}_{}.txt'.format(client_id, max_file_number+1)

                # writes the payload from tcp 
                with open(os.path.join(STORE, file_name), 'wb') as f:
                    while True:
                        payload = soc.recv(1024)
                        if not payload:
                            sys.exit(0)
                        f.write(payload)

except:
    print('Something bad happened! Terminating gracefully..')
