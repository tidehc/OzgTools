# coding=utf-8

import os
import sys
import wx
import cfg

from threading import Thread  

class OzgMainFrame(wx.Frame):
	
	def __init__(self):
		wx.Frame.__init__(self, None, -1, cfg.STRINGS_NAME, size = (435, 185), style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		mainPanel = wx.Panel(self, -1)
		
		#后缀名部分
		wx.StaticText(mainPanel, -1, cfg.STRINGS_STATIC_TEXT1, pos = (10, 23))
		self.filesFilterTextCtrl = wx.TextCtrl(mainPanel, -1, cfg.STRINGS_TEXT_FILES_FILTER, pos = (110, 17), size = (200, 22))
		
		#选择文件夹部分
		wx.StaticText(mainPanel, -1, cfg.STRINGS_STATIC_TEXT2, pos = (10, 63))
		self.dirTextCtrl = wx.TextCtrl(mainPanel, -1, u"", pos = (110, 57), size = (200, 22))
		
		#选择文件夹的按钮
		self.selectDirButton = wx.Button(mainPanel, cfg.WXID_BTN_SELECTED_DIR, cfg.STRINGS_BTN_SELECTED_DIR_TEXT, pos = (320, 55), size = (100, 25))
		self.Bind(wx.EVT_BUTTON, self.BtnOnClick, self.selectDirButton)
		self.selectDirButton.SetDefault()
		
		#选择编码
		wx.StaticText(mainPanel, -1, cfg.STRINGS_STATIC_TEXT3, pos = (46, 93))
		self.encodeUTF8Radio = wx.RadioButton(mainPanel, cfg.WXID_RADIO_ENCODE_UTF8, cfg.STRINGS_ENCODE_UTF8_TEXT, pos = (110, 90), size = (60, 22), name = cfg.STRINGS_ENCODE_RADIO)
		self.encodeUTF8Radio.SetValue(True)
		self.encodeGBKRadio = wx.RadioButton(mainPanel, cfg.WXID_RADIO_ENCODE_GBK, cfg.STRINGS_ENCODE_GBK_TEXT, pos = (180, 90), size = (60, 22), name = cfg.STRINGS_ENCODE_RADIO)

		#执行按钮
		self.runButton = wx.Button(mainPanel, cfg.WXID_BTN_RUN, cfg.STRINGS_BTN_RUN, pos = (175, 120), size = (80, 25))
		self.Bind(wx.EVT_BUTTON, self.BtnOnClick, self.runButton)
		self.runButton.SetDefault()
	
	def BtnOnClick(self, event):
		"""
		按钮点击的事件
		"""

		if event.GetEventObject().GetId() == cfg.WXID_BTN_SELECTED_DIR:
			filesSelectDialog = wx.DirDialog(None, cfg.STRINGS_SELECTED_DIR_TEXT, style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

			#选定文件夹后触发
			if filesSelectDialog.ShowModal() == wx.ID_OK:
				self.dirTextCtrl.SetValue(filesSelectDialog.GetPath())
		elif event.GetEventObject().GetId() == cfg.WXID_BTN_RUN:			
			#if self.encodeUTF8Radio.GetValue():
				#print "1"
			#elif self.encodeGBKRadio.GetValue():
				#print "2"

			alert = wx.MessageDialog(None, cfg.STRINGS_DIALOG_MSG1, cfg.STRINGS_DIALOG_TITLE, style = wx.OK | wx.CANCEL, pos = (100, 100))
			if alert.ShowModal() == wx.ID_OK:
				if self.filesFilterTextCtrl.GetValue().strip() == u"":
					#需要处理的文件为空
					alert = wx.MessageDialog(None, cfg.STRINGS_DIALOG_MSG2, cfg.STRINGS_DIALOG_TITLE, style = wx.OK, pos = (100, 100))
					alert.ShowModal()
					return
				elif self.dirTextCtrl.GetValue().strip() == u"":
					#待处理的文件夹为空
					alert = wx.MessageDialog(None, cfg.STRINGS_DIALOG_MSG3, cfg.STRINGS_DIALOG_TITLE, style = wx.OK, pos = (100, 100))
					alert.ShowModal()
					return
				else:
					#启动子线程来执行转换编码的工作
					self.childThread = Thread(target = self.EncodeChangeThread, args = ())
					self.childThread.start()

	def EncodeChangeThread(self):
		"""
		子线程执行转换编码的逻辑
		"""

		wx.CallAfter(self.EnableUI, False)
		self.EncodeChange(self.dirTextCtrl.GetValue())
		wx.CallAfter(self.FinishChange)
		
	def EncodeChange(self, dirPath):
		"""
		历遍目录来执行转换编码，这个是递归方法
		"""

		files = os.listdir(dirPath)
		for f in files:
			filePath = os.path.join(dirPath, f)
			if os.path.isdir(filePath):
				#是文件夹的话则继续执行本方法
				self.EncodeChange(filePath)
			else:
				#是文件的话则执行转换编码的流程

				#判断是否为需要处理的文件
				isExec = False
				filesFilter = self.filesFilterTextCtrl.GetValue().split(u";")
				for i in filesFilter:
					if i == filePath[filePath.rfind("."):]:
						isExec = True
						break
				
				#不是的话则跳过
				if not isExec:
					print u"%s %s" % (filePath, cfg.STRINGS_RUNNING_MSG2)
					continue

				#读取文件部分
				fileContent = None
				fileObject = open(filePath)
				try:
					fileContent = fileObject.read()
				finally:
					fileObject.close()
				#print fileContent
				
				#转换编码部分
				if self.encodeUTF8Radio.GetValue():
					#GBK转换为UTF-8
					try:
						fileContent = fileContent.decode("GBK").encode("UTF-8")
					except UnicodeDecodeError, e:
						msg = "%s %s" % (filePath, cfg.STRINGS_DIALOG_MSG5)
						alert = wx.MessageDialog(None, msg, cfg.STRINGS_DIALOG_TITLE, style = wx.OK, pos = (100, 100))
						alert.ShowModal()
						continue

				elif self.encodeGBKRadio.GetValue():
					#UTF-8转换为GBK
					try:
						fileContent = fileContent.decode("UTF-8").encode("GBK")
					except UnicodeDecodeError, e:
						msg = "%s %s" % (filePath, cfg.STRINGS_DIALOG_MSG5)
						alert = wx.MessageDialog(None, msg, cfg.STRINGS_DIALOG_TITLE, style = wx.OK, pos = (100, 100))
						alert.ShowModal()
						continue
				
				#写入文件部分
				fileObject = open(filePath, "w")
				fileObject.write(fileContent)
				fileObject.close()

				print u"%s %s" % (filePath, cfg.STRINGS_RUNNING_MSG1)
	
	def EnableUI(self, isEnable):
		"""
		是否启用窗口上面的控件
		"""

		self.filesFilterTextCtrl.Enable(isEnable)
		self.dirTextCtrl.Enable(isEnable)
		self.encodeUTF8Radio.Enable(isEnable)
		self.encodeGBKRadio.Enable(isEnable)
		self.selectDirButton.Enable(isEnable)
		self.runButton.Enable(isEnable)

	def FinishChange(self):
		"""
		完成操作流程后执行
		"""

		alert = wx.MessageDialog(None, cfg.STRINGS_DIALOG_MSG4, cfg.STRINGS_DIALOG_TITLE, style = wx.OK, pos = (100, 100))
		alert.ShowModal()
		self.EnableUI(True)

if __name__ == "__main__":
	app = wx.App()
	frame = OzgMainFrame()
	frame.Show(True)
	app.MainLoop()
