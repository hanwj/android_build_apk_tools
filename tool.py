#!/usr/bin
#coding=utf-8
import os
import sys
import re
import argparse
import subprocess
import datetime

androidRoot = "/data/work/yoyo/android_new/"  #项目根目录
urlFilePath = "app/src/main/java/com/xcyo/yoyo/server/ServerRegister.java"
#androidResPath = os.path.join(androidRoot,"app/src/main/res")   #资源目录  
gradleFilePath = os.path.join(androidRoot,"build.gradle")  #项目build.gradle文件路径
appGradleFilePath = os.path.join(androidRoot,"build.gradle")  #项目主build.gradle路径
configPath = os.path.dirname(os.path.abspath(sys.argv[0]))  #配置目录
versionConfigPath = os.path.join(configPath,"version.config")  #各个版本配置文件路径

def executeCmd(cmd):
	print "executeCmd cmd: " + cmd
	os.system(cmd)

def showErrorAndExit(msg):
	print "[error] " + msg
	exit()

def replaceLines(fileName,src,rep):
	print "replace file: " + fileName
	executeCmd("sed -i '' 's/%s/%s/g' %s" % (src,rep,fileName))

#获取当前分支
def getCurrentBranch(path):
	cmd = "cd %s && git branch | awk '{if($1==\"*\") print $2}'" %path
	output = subprocess.check_output(cmd,shell = True)
	return output.rstrip("\n")

#获取所有tag
def getTags(path):
	executeCmd("cd %s && git fetch" %path)
	output = subprocess.check_output("cd %s && git tag" %path,shell = True)
	ret = output.split(os.linesep)
	return ret
#打tag
def createTag(path):
	branch = getCurrentBranch(path)
	now  = datetime.datetime.now()
	today = now.strftime('%y%m%d')
	tags = getTags(path)
	maxIndex = 0
	for tag in tags:
		r = re.match(branch + "\." + today + "\.(\d+)",tag)
		if r:
			temp = int(r.group(1))
			if maxIndex < temp:
				maxIndex = temp
	maxIndex = str('%02d' %(maxIndex + 1))
	tag = "%s.%s.%s" %(branch,today,maxIndex)
	executeCmd("cd %s && git tag -a %s -m 'auto create tag' && git push origin %s" %(path,tag,tag))
	return tag

#切换到对应的tag
def handleGit(path,tag):
	executeCmd("cd %s && git fetch && git checkout -f %s" %(path,tag));

#获取该版本号对应的配置
def getVersionConfig(versionCode):	
	fp = open(versionConfigPath,"r")
	for line in fp.readlines():
		splitArrs = line.split()
		if splitArrs[0] == versionCode:
			fp.close()
			return splitArrs	
	fp.close()

#打包
def buildApk(args):
	versionCode = ""
	versionName = ""
	srcTag = ""
	#resTag = ""
	if args.versionCode:
		versionCode = args.versionCode
	else:
		showErrorAndExit("versionCode must be pass")

	#获取版本配置
	versionConfig = getVersionConfig(str(args.versionCode))

	if versionConfig :
		print "versionConfig : " + " ".join(versionConfig)
		versionName = versionConfig[1]
		srcTag = versionConfig[2]
		#resTag = versionConfig[3]
	else:
		showErrorAndExit("miss versionCode[%s]'s config" %args.versionCode)

	#备份下app下面的build.gradle文件（已废弃）
	# executeCmd("cp %s %s" %(appGradleFilePath,configPath))	
	#处理srctag、restag
	handleGit(androidRoot,srcTag)
	#handleGit(androidResPath,resTag)
	#替换app下面的build.gradle文件
	executeCmd("cp %s %s" %(os.path.join(configPath,"build.gradle"),androidRoot))	
	#修改versionCode
	replaceLines(gradleFilePath, "\(.*\)versionCode \(.*\)", "    versionCode = " + str(args.versionCode))
	#修改versionName
	replaceLines(gradleFilePath, "\(.*\)versionName \(.*\)", "    versionName = \"" + str(versionName) + "\"")
	#修改url
	replaceLines(os.path.join(androidRoot,urlFilePath),"http:\\/\\/\(.*\)\\/app","http:\\/\\/www.xcyo.com\\/app")
	#打包
	executeCmd("cd %s && gradle clean && gradle assembleRelease" %androidRoot)
	#更新安装包

parser = argparse.ArgumentParser()
parser.add_argument("action",choices=["apk","tag"],help="action")
parser.add_argument("-vc","--versionCode",type=int,help="versionCode")
parser.add_argument("-vn","--versionName",help="versionName")
args = parser.parse_args()
if args.action == "apk":
	buildApk(args)
elif args.action == "tag":
	srcTag = createTag(androidRoot)
	#resTag = createTag(androidResPath)
	print "srcTag : " + srcTag