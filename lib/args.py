# Date: 08/24/2018
# Author: Pure-L0G1C
# Description: Arguments

from re import match 
from socket import gethostbyname
from argparse import ArgumentParser
try:from urllib.parse import urlparse
except:from urlparse import urlparse 

class Args(object):

 def __init__(self):
  self.ip = None
  self.url = None 
  self.port = None
  self.threads = None

 def __repr__(self):
  return str({ 'ip': self.ip, 'url': self.url, 'port': self.port, 'threads': self.threads })  
  
 def error(self, error):
  print('Error: {}'.format(error))

 def get_ip(self, url):
  try:
   _url = urlparse(url).netloc
   return gethostbyname(_url)
  except:
   self.error('unable to contact the site `{}`'.format(url))
  
 def get_args(self): 
  parser = ArgumentParser()

  parser.add_argument('-i',
                     '--ip',
                     help='the targeted ip. \
                      Example: -i 127.0.0.1')

  parser.add_argument('-u',
                     '--url',
                     help='the targeted site. \
                      Example: -u https://google.com')

  parser.add_argument('-p',
                     '--ports',     
                     action='append', 
                     help='the targetd ports. \
                      Example: -p \"21, 80, 443\"')

  parser.add_argument('-t',                      
                     '--threads',                     
                     help='number of threads to use by default it is set to 5000')  
  return parser.parse_args()

 def set_args(self):
  args = self.get_args()

  self.ip = args.ip 
  self.url = args.url 
  self.port = args.ports
  self.threads = args.threads 

  if all([not self.ip, not self.url]):
   self.error('Please specify an ip or a url')
   return False

  if all([self.ip, self.url]):
   self.error('Please user an ip or a url, but not both')  
   return False

  if any([not self.valid_ip, not self.valid_port, not self.valid_threads]):
   return False

  if self.url:
   ip = self.get_ip(self.url)
   if not ip:
    return False
   self.ip = ip 

  if not self.port:
   self.port = range(1, 65536)
  if not self.threads:
   self.threads = 5000
  return True 

 @property 
 def valid_threads(self):
  if not self.threads:return True

  if not self.threads.isdigit():
   self.error('Threads must be an integer')
   return False

  if int(self.threads) <= 0:
   self.error('Threads must not be less than 1')
   return False

  self.threads = int(self.threads)
  return True 

 @property 
 def valid_ip(self):
  if not self.ip:return True
  if not match(r'^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$', self.ip):
   self.error('Invalid IP address')
   return False 
  return True

 @property 
 def valid_port(self):
  ports = []
  if not self.port:return True
  for port in self.port[0].split(','):
   _port = str(port).strip()
      
   if not len(_port): 
    return False
   else:
    #  check if number
    for item in _port:
     if not item.isdigit():
      return False    

    # check if number starts with a zero
    if int(_port[0]) == 0:
     return False 

    # check if number is larger than 65535
    if int(_port) > 65535:
     return False 
    ports.append(int(port))
  self.port = ports
  return True