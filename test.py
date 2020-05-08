#!/usr/bin
#coding=utf-8
import sys

def testStack():
	tip = "回文字符串检测\n输入需要检测的文字:"
	print tip.decode("utf-8")
	inputStr = raw_input(unicode(tip,"utf-8").encode("gbk"))
	length = len(inputStr)
	mid = length/2 - 1
	tmp = ""
	top = 0
	for i in xrange(0,mid + 1):
		tmp += inputStr[i]
		top = top + 1

	if length % 2 == 0:
		start = mid + 1
	else:
		start = mid + 2

	for i in xrange(start,length):
		# print "%d,%d" %(top-1,i)
		# print "%s,%s" %(tmp[top-1],inputStr[i])
		if tmp[top - 1] != inputStr[i]:
			break
		top = top - 1

	if top == 0:
		print True
	else:
		print False

testStack()

output = subprocess.check_output("ls")
print output
