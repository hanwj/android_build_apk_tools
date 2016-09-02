#!/usr/bin/
#coding=utf-8

import os
import sys

apkDir = "/data/work/yoyo/android_new/app/build/outputs/apk/"
serverApkDir = "/home/yoyo/yoyo/www/web/apk/"
apks = ["龙珠悠悠-wandoujia-2.0.4.apk",
	"龙珠悠悠-anzhi-2.0.4.apk",
	"龙珠悠悠-baidu-2.0.4.apk",
	"龙珠悠悠-kuchuan-2.0.4.apk",
	"龙珠悠悠-xiaomi-2.0.4.apk"]

server = "yoyo@admin.xcyo.com"
def executeCmd(cmd):
	print "cmd: " + cmd;
	os.system(cmd)

for apk in apks:
	apkFile = os.path.join(apkDir,apk)
	cmd = "scp %s %s:%s" %(apkFile,server,serverApkDir)
	# executeCmd(cmd)

zsyncCmd = "ssh %s && cd /home/yoyo/yoyo/www/" %server	
for apk in apks:
	apkFile = os.path.join(serverApkDir,apk)
	zsyncCmd = "%s && zsync web/apk/%s" %(zsyncCmd,apk)
executeCmd(zsyncCmd)
	