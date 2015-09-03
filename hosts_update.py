# coding=utf-8

#github: https://github.com/ouzhigang/OzgTools/blob/master/hosts_update.py

#需要安装的库
#pip install tornado

#本程序不会删除原有的hosts内容
#第一次运行先备份原有的hosts文件
#然后打开hosts文件，在后面加入一行#ozg auto update，然后回车
#运行时需要管理员权限

import sys, os, time, re, platform
import xml.etree.ElementTree as ET
import tornado.httpclient;

#获取hosts的路径
def get_hosts_path():
	if platform.system() == "Windows":
		#windows
		return "C:/Windows/System32/drivers/etc/hosts"
	else:
		#linux or mac
		return "/etc/hosts"

if __name__ == "__main__":	

	#暂时只支持window
	if platform.system() != "Windows":
		print "Only Windows"
		exit()
	
	#处理逻辑
	#hosts数据的网址
	update_url = "http://laod.cn/hosts/2015-google-hosts.html"
	
	http_headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36" }
	hosts_path = get_hosts_path()
	
	http_client = tornado.httpclient.HTTPClient()
	http_client.headers = http_headers
	
	try:
		response = http_client.fetch(update_url)
		
		#解析逻辑
		node1 = re.search(r'<blockquote>.*</blockquote>', response.body).group(0)
		node1 = node1.replace("&nbsp;", "")
		tree = ET.ElementTree(ET.fromstring(node1))
		p_list = tree.findall('p')
		
		p_last = p_list[len(p_list) - 1]
		target_node = p_last.getchildren()[0].getchildren()[0]
		target_url = target_node.attrib["href"]
		
		#获取hosts数据
		http_client2 = tornado.httpclient.HTTPClient()
		http_client2.headers = http_headers
		try:
			response2 = http_client.fetch(target_url)
			
			hosts_file = open(hosts_path)
			hosts_tmp_list = hosts_file.readlines()
			
			save_file_list = []
			
			for line in hosts_tmp_list:
				save_file_list.append(line)
				if line == "#ozg auto update\n":	
					save_file_list.append("\r\n")
					break
			
			for line in response2.body.split("\n"):
				save_file_list.append(line)
			
			save_file = open(hosts_path, "w")
			for line in save_file_list:
				save_file.write(line)
			
			save_file.write("\r\n\r\n")
			save_file.write("#更新时间：" + time.strftime("%Y-%m-%d %H:%M:%S") + "\r\n")
			save_file.write("#更新版本：" + target_node.text + "\r\n")
			save_file.close()
			
		except tornado.httpclient.HTTPError as e:
			print("Error: " + str(e))
		except Exception as e:
			print("Error: " + str(e))
		http_client2.close()
		
	except tornado.httpclient.HTTPError as e:
		# HTTPError is raised for non-200 responses; the response
		# can be found in e.response.
		print("Error: " + str(e))
	except Exception as e:
		# Other errors are possible, such as IOError.
		print("Error: " + str(e))
	http_client.close()
	
	#处理逻辑 end
	
	print "Complete!"
