#!/usr/bin
# coding=utf-8
# @Author:caixiaoxiao
# @Time:20200508
# @FileName:apksign.py
# @Desc:apk重新签名；使用VasDolly批量打渠道包

import os
import sys
import getopt
import subprocess
import re

aapt = "/Applications/android/sdk/build-tools/28.0.2/aapt" #aapt路径
signPath = "/data/work/android/sign" #签名文件目录
vasDollyPath = "/data/work/android/VasDolly/command/jar/VasDolly.jar" #多渠道命令路径
apkSignCmdFormat = "jarsigner -verbose -keystore {} -storepass {} -signedjar {} {} {}"
keystoreFilePath = os.path.join(signPath,"build.properties") #签名文件配置
outputPath = os.path.join(signPath,"output") #默认输出目录
apk_prefix = "virgo_aph" #apk前缀

#执行cmd
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

#获取apk版本号
def getApkVersionName(apkFile):
	cmd = "%s dump badging %s | grep 'versionName'" %(aapt,apkFile)
	output = subprocess.check_output(cmd,shell=True)
	print"output:" + output
	pattern = re.compile(r" versionName=\'([0-9.]+)\'")
	result = pattern.search(output)
	if result:
		return result.group(1)
	else:
		return 'x.x.x'

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

apkVersionName = getApkVersionName(intputfile)
apkBaseName = "%s_%s" %(apk_prefix,apkVersionName)
print "apk's name : %s" %(apkBaseName)

#重新签名
keystoreConfig = getKeystoreConfig(keystoreFilePath)
signApkPath = os.path.join(outputPath,apkBaseName + "_signed.apk")
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
	#重命名[app名称_版本号_渠道号]
	channelList = channels.split(",")
	for channel in channelList:
		outputApkName = channel + "-" + apkBaseName + "_signed.apk"
		modifiedtyApkName = apkBaseName + "_" + channel + ".apk"
		executeCmd("mv %s %s" %(os.path.join(outputPath,outputApkName),os.path.join(outputPath,modifiedtyApkName)))

#打开输出目录
print "=========================="
print "output:" + outputPath
if platform.startswith("win32"):
	executeCmd("start %s" %outputPath)
else:
	executeCmd("open %s" %outputPath)