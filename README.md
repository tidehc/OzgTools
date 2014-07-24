目录详解

files_encode_change 将指定文件夹的文本文件在UTF-8和GBK之间转换（注意备份将要转换的文件），运行在python2.7, wxPython3.0.0.0（目前还没有在windows以外的OS运行过）。

images 批量将HD图片缩小和批量添加-hd后缀。运行在mac平台。

plist_to_images 将cocos2d的plist的各个帧转换回单个图片，只支持png。Resources/plist_image/里面存放需要转换的plist和已合并的png，Libraries/存放cocos2d-iphone v3.0的文件。只能运行在iOS模拟器，IntroScene.m里面的保存路径需要按照实际情况修改。

2dx_v3_proj_helper.py 只对应2dx v3，平时为了节省空间删除了2dx的公用文件夹{project_name}/cocos2d，到需要使用的时候执行这个文件将已删除的文件夹复制回对应位置。
