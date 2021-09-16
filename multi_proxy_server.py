""" Code in this file adapted from template obtained in lab.
Zoe Riell, CMPUT 404 Lab 2, Remote Synchronous Lab, 2021-09-15, Public Domain
"""

#!/usr/bin/env python3
from echo_server import BUFFER_SIZE
import socket, time, sys
from multiprocessing import Process

# get IP
def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()
    return remote_ip

# handle a single client request
def handle_request(addr, client, target):
  full_data = client.recv(BUFFER_SIZE)
  print(f"Sending received data {full_data} to google")
  target.sendall(full_data)

  data = target.recv(BUFFER_SIZE)
  print(f"Sending received data {data} to client")
  client.send(data)

  target.shutdown(socket.SHUT_RDWR)
  target.close()

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
  extern_host = "www.google.com"
  extern_port = 80

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    # bind, and set to listening mode
    proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_start.bind((HOST, PORT))
    proxy_start.listen(2)

    while True:
      # accept incoming connections from proxy_start, print information about connection
      conn, addr = proxy_start.accept()
      print("Connected by", addr)

      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        # get remote IP of google, connect proxy_end to it
        remote_ip = get_remote_ip(extern_host)
        proxy_end.connect((remote_ip, extern_port))
        
        # now for the multiprocessing
        # allow for multiple connections with a Process daemon
        # make sure to set target = handle_request when creating the Process
 
        p = Process(target=handle_request, args=(addr, conn, proxy_end))
        p.daemon = True
        p.start()
        print("Started process", p)
      
      # close the connection!
      conn.close()

if __name__ == "__main__":
  main()
