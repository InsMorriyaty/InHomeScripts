import sys 
import os

f1 = sys.argv[1] # pep fa 
f2 = sys.argv[2] # sp 

'''
cmd1 = f"/home/u80010049/software/phobius/phobius.pl {f1} > {f2}.phobius"
cmd2 = f"cat {f1} | /home/u80010049/software/tmhmm-2.0c/bin/tmhmm  > {f2}.tmhmm"
cmd3 = f"/home/u80010049/software/TMPred-master/build/TMPred {f1} -o {f2}.tmpred"

os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
'''

cmd4 = f"python3 ~/software/GetTMCounts.py ./ {f2} > {f2}.TMcount.stat"
cmd5 = f"python3 ~/software/FilterTM.py {f2}.TMcount.stat"
os.system(cmd4)
os.system(cmd5)
