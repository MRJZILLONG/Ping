# Date: 08/24/2018
# Author: Pure-L0G1C
# Description: Scanner

import socket
from queue import Queue 
from time import time, sleep
from threading import Thread, RLock 

class Scanner(object):

 def __init__(self, ip, ports, threads):
  self.ip = ip
  self.lock = RLock()
  self.is_alive = True 
  self.threads = threads
  self.active_port_found = False 
  self.ports = self.get_ports(ports)

 def get_ports(self, ports):
  _ports = Queue()
  [_ports.put(_) for _ in ports]
  return _ports

 def close(self, sock):
  try:
   sock.shutdown(socket.SHUT_RDWR)
   sock.close()
  except:pass

 def connect(self, port):   
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  connected = False 
  try:
   sock.connect((self.ip, port))  
   connected = True
   self.close(sock)
  except:pass
  finally:
   return connected

 def active_port(self, port):
  if not self.active_port_found:
   print('\n# -----[ Active ports ]----- #\n')
   self.active_port_found = True 
  print('\t Port: {}'.format(port))

 def scan(self):
  while all([self.ports.qsize(), self.is_alive]):
   with self.lock:
    port = self.ports.get()

   try:
    active = self.connect(port)
    if active:
     with self.lock:
      self.active_port(port)
   except:
    pass
   
  if self.is_alive:
   with self.lock:
    self.stop()
    
 def start(self):
  self.start_time = time()
  for thread in range(self.threads):
   if any([not self.is_alive, not self.ports.qsize()]):break
   t = Thread(target=self.scan)
   t.daemon = True
   t.start()   
  
 def stop(self):
  if self.is_alive:
   self.is_alive = False
   print('\nTime-elapsed: {}'.format(time()-self.start_time))