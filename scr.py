import os
import sys

for i in range(1,31):
    os.system("nohup python3 bs.py "+sys.argv[1]+" 1 200 "+str(i)+" &")
