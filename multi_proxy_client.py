""" All code in this file obtained from lab.
Zoe Riell, CMPUT 404 Lab 2, Remote Synchronous Lab, 2021-09-15, Public Domain
"""

#!/usr/bin/env python3

import socket
from multiprocessing import Pool

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024


payload = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

def connect(addr):
  try:
    #create socket, connect, send and receive then shutdown
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(payload.encode())
    s.shutdown(socket.SHUT_WR)

    full_data = s.recv(BUFFER_SIZE)
    print(full_data)

  except Exception as e:
    print(e)

  finally:
    #remember to close
    s.close()

def main():
  address = [(HOST, PORT)]
  #establish 10 different connections
  with Pool() as p:
    p.map(connect, address * 10)

if __name__ == "__main__":
  main()