#!/bin/python3

import sys
import socket
from datetime import datetime
import queue
import threading


Q = queue.Queue()
target = 'localhost'
thread_count = 20

class PortThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        process_queue()

def process_queue():
    global Q

    while True:
        try:
            port = Q.get(block=False)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((target, port))
                if result == 0:
                    print(f'{port} is open')
                s.close()
            except KeyboardInterrupt:
                print('exiting')
                sys.exit()
            except socket.gaierror:
                print('host name could not be resolved')
                sys.exit()
            except socket.error:
                print('connection to host could not be established')
                sys.exit()
        except queue.Empty:
            return

def main():
    global Q
    global target

    if len(sys.argv) == 2:
        target = socket.gethostbyname(sys.argv[1])
    else:
        print('invalid number of arguments')

    print(f'scanning target {target} - starting {datetime.now()} \n')
    print('#'*50,'\n')

    for port in range(65536):
        Q.put(port)

    threads = []
    for i in range(thread_count):
        threads.append(PortThread())

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__== '__main__':
    main()
