#!/usr/bin/python

import os
import sys
import re
pngquantpath = "/usr/local/pngquant/pngquant"
if pngquantpath == "":
    print("pngquant mube have value")
    os.exit()

outDir = sys.argv[2]
os.system("rm -rf " + outDir)
for dirpath,dirnames,filelist in os.walk(sys.argv[1]):
    if not dirpath.startswith("\."):
        for f in filelist:
            fPath = dirpath + os.sep + f
            outfPath = outDir + fPath
            if not os.path.isdir(outDir + dirpath):
                os.makedirs(outDir + dirpath)
            strArrs = re.split("\.",f)
            if strArrs[-1] == "png" or strArrs[-1] == "jpg":
                #print("handle file : " + fPath + "\n")
                cmdStr = pngquantpath + " --quality 1 --speed 1 --posterize RGBA4444 " + fPath + " --output " + outfPath
                os.system(cmdStr)
            else:
                os.system("cp " + fPath + " " + outfPath)

print("====================pngquant end======================")
