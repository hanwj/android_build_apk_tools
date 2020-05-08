#!/usr/bin
#coding=utf-8
import os
import sys
import getopt

signPath = "C:\\Users\\caixiaoxiao\\Desktop\\xxxxx\\sign"
vasDollyPath = "F:\\project\\VasDolly\\command\\jar\\VasDolly.jar"
apkSignCmdFormat = "jarsigner -verbose -keystore {} -storepass {} -signedjar {} {} {}"
keystoreFilePath = os.path.join(signPath,"build.properties")
outputPath = os.path.join(signPath,"output")


def executeCmd(cmd):
	print "executeCmd: " + cmd
	os.system(cmd)
	# processId = os.spawnv(os.P_WAIT,cmd,[])
	# print "processId:" + processId

#读取properties文件
def getKeystoreConfig(path):
	file = open(path,'r')
	properties = {}
	for line in file.readlines():
		if line.find("=") > 0:
			strs = line.replace("\n","").split("=")
			properties[strs[0]] = strs[1]
	file.close()
	print properties
	return properties


try:
	opts,args = getopt.getopt(sys.argv[1:],"hi:o:c:")	
except Exception as e:
	print "apksign.py -i <intputfile> -o <outputPath> -c <channels>"
	sys.exit()

intputfile = ""
channels = ""
platform = sys.platform
print "cur system:" + platform

for opt,value in opts:
	if opt == '-h':
		print "apksign.py -i <intputfile> -o <outputPath> -c <channels>"
		sys.exit()
	elif opt == '-i':
		intputfile = value
		print "iutputfile:" + value
	elif opt == '-o':
		outputPath = value
		print "outputPath:" + value
	elif opt == "-c":
		channels = value
		print"channels:" + channels

if not intputfile:
	print "apksign.py -i <intputfile> -o <outputPath> -c <channels>"
	sys.exit()

#检查输入目录是否存在，不存在则创建
if not os.path.isdir(outputPath):
	print "makedir:%s" %outputPath
	os.makedirs(outputPath)

apkName = os.path.basename(intputfile)
print "apk's name : " + apkName	

#重新签名
keystoreConfig = getKeystoreConfig(keystoreFilePath)
signApkPath = os.path.join(outputPath,"sign-" + apkName)
signCmd = apkSignCmdFormat.format(os.path.join(signPath,keystoreConfig["key.store"]),
	keystoreConfig["key.store.password"],
	signApkPath,
	intputfile,
	keystoreConfig["key.alias"])
executeCmd("cd %s && %s" %(signPath,signCmd))

#打渠道号标记
if channels:
	print"channels:" + channels
	executeCmd("java -jar %s put -c \"%s\" -f %s %s" %(vasDollyPath,channels,signApkPath,outputPath))

#打开输出目录
print "=========================="
print "output:" + outputPath
if platform.startswith("win32"):
	executeCmd("start %s" %outputPath)
else:
	executeCmd("open %s" %outputPath)