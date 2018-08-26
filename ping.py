# Date: 08/24/2018
# Author: Pure-L0G1C
# Description: Port scanner
 
from time import sleep
from lib.args import Args
from lib.scan import Scanner 

if __name__ == '__main__':
 args = Args()

 if args.set_args():
  scanner = Scanner(args.ip, args.port, args.threads)
  
  try:
   scanner.start()
  except KeyboardInterrupt:
   scanner.is_alive = False

  while scanner.is_alive:
   try:sleep(0.5)
   except KeyboardInterrupt:
    scanner.is_alive = False