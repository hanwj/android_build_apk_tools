#!usr/bin
#coding=utf-8
# ********* flash文件批量导成lwf文件 *********
import os
import sys
import shutil

lwfToolsPath = "/Users/meibo-design/Desktop/lwf/lwfs-20141201-1830/lib/swf2lwf/swf2lwf.rb"
animFileDir = "/data/work/yoyo/秀场/美术/改版后手机礼物/礼物源文件2"   #动画目录
outputDir = "/data/work/yoyo/秀场/美术/改版后手机礼物/输出"  #输出目录
# outputDir = "/data/yoyolwf"  #输出目录
animList = []   #动画文件
warnMsg = "***********warning************\n"

def executeCmd(cmd):
	print "executeCmd cmd: " + cmd
	os.system(cmd)

def showErrorAndExit(msg):
	print "[error] " + msg
	exit()

def warn(msg):
	global warnMsg
	warnMsg += "[warning] " + msg + "\n"

def batchZip(fileDir):
	for i in os.listdir(fileDir):
		executeCmd("cd " + fileDir +" && zip -r -m " + i + ".zip " + i)

def getAnimList(animDir):
	for i in os.listdir(animDir):
		if os.path.isfile(os.path.join(animDir,i)) and i.endswith(".swf"):
			animName = i[:-4]
			#检测相应的fla文件是否存在
			if os.path.isfile(os.path.join(animDir,animName + ".fla")):
				animList.append(animName)
			else:
				warn("anim " + animName + " 's fla file is not exist")

#获取动画列表
getAnimList(animFileDir)

#清空输出目录并重新创建输出目录
if os.path.isdir(outputDir):
	shutil.rmtree(outputDir)
os.mkdir(outputDir)

for name in animList:
	#动画格式转换
	executeCmd("ruby " + lwfToolsPath + " " + os.path.join(animFileDir,name + ".swf"))
	outputLwf = os.path.join(animFileDir,name + ".lwfdata" + os.sep + name + ".lwf")
	animBitmapDir = os.path.join(animFileDir,name + ".bitmap")
	#判断lwf文件是否存在
	if os.path.isfile(outputLwf):
		#创建动画输出目录
		outputAnimDir = os.path.join(outputDir,name)
		if os.path.isdir(animBitmapDir):
			shutil.copytree(animBitmapDir,outputAnimDir,False)
		else:
			warn("anim " + name + "miss bitmap dir")

		if not os.path.isdir(outputAnimDir):
			os.mkdir(outputAnimDir)
		#移动lwf文件
		shutil.copy(outputLwf,outputAnimDir)
	else:
		warn("anim " + name + " miss lwf file")

#batchZip(outputDir)
executeCmd("open " + os.path.join(outputDir))
print warnMsg
print "end"

