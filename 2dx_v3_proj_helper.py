# coding=utf-8

import sys
import os
import shutil

def CleanDir(Dir):
	if os.path.isdir(Dir):
		paths = os.listdir(Dir)
		for path in paths:
			filePath = os.path.join(Dir, path)
			if os.path.isfile(filePath):
				try:
					os.remove(filePath)
				except os.error:
					autoRun.exception("remove %s error." % filePath) #引入logging

			elif os.path.isdir( filePath ):
				if filePath[-4:].lower() == ".svn".lower():
					continue
				shutil.rmtree(filePath, True)
	return True

def RmDir(Dir):
	CleanDir(Dir)
	os.rmdir(Dir)

#def recursion_dir(file_path):

	#if os.path.isdir(file_path):
		
		#file_list = os.listdir(file_path)
		#for i in file_list:
			#dir_path = os.path.join(file_path, i)
			#recursion_dir(dir_path)
	#else:
		#print file_path

if __name__ == "__main__":

	cocos2dx_root =  raw_input("请输入2dx v3的路径:\n")
	project_root = raw_input("请输入目标项目的路径:\n")
	
	cocos2dx_root = cocos2dx_root.replace("\\", "/")
	project_root = project_root.replace("\\", "/")
	
	#test
	#cocos2dx_root = "D:/root/Temp/cocos2d-x-3.2"
	#project_root = "D:/root/Temp/MyGame"

	os.system(os.path.join(cocos2dx_root, "tools/cocos2d-console/bin/cocos new MyGame -p com.your_company.mygame -l cpp -d TEMP_DIR"))	
	shutil.copytree("./TEMP_DIR/MyGame/cocos2d", os.path.join(project_root, "cocos2d"))
	RmDir("./TEMP_DIR")

	print "Finish!"
