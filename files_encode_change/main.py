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
					#filesFilter = self.filesFilterTextCtrl.GetValue().split(u";")
					#print filesFilter
										
					self.childThread = Thread(target = self.EncodeChangeThread, args = ())
					self.childThread.start()

	def EncodeChangeThread(self):
		wx.CallAfter(self.EnableUI, False)
		self.EncodeChange(self.dirTextCtrl.GetValue())
		wx.CallAfter(self.FinishChange)
		
	def EncodeChange(self, dirPath):
		files = os.listdir(dirPath)
		for f in files:
			filePath = os.path.join(dirPath, f)
			if os.path.isdir(filePath):
				self.EncodeChange(filePath)
			else:
				print u"%s %s" % (filePath, cfg.STRINGS_RUNNING_MSG)
	
	def EnableUI(self, isEnable):
		self.filesFilterTextCtrl.Enable(isEnable)
		self.dirTextCtrl.Enable(isEnable)
		self.encodeGBKRadio.Enable(isEnable)
		self.selectDirButton.Enable(isEnable)
		self.runButton.Enable(isEnable)

	def FinishChange(self):
		alert = wx.MessageDialog(None, cfg.STRINGS_DIALOG_MSG4, cfg.STRINGS_DIALOG_TITLE, style = wx.OK, pos = (100, 100))
		alert.ShowModal()
		self.EnableUI(True)

if __name__ == "__main__":
	app = wx.App()
	frame = OzgMainFrame()
	frame.Show(True)
	app.MainLoop()
