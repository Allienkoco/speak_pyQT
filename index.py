# -*- coding: utf-8 -*-

import os
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtWidgets
from Ui_index import Ui_MainWindow
from gettoken import fetch_token
from getsounds import getsounds
from pydub import AudioSegment


class MainWindow(QMainWindow, Ui_MainWindow):

    textecoding = ''
    filepath = ''
    soundspath = ''
    treads = []

    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.textecoding = 'utf-8'
        self.filepath = os.getcwd()
        self.soundspath = os.getcwd()

    def btn_open(self):
        filename = QFileDialog.getOpenFileName(
            self, '选择文件', str(os.getcwd()), "Text Files (*.txt)")
        print(filename[0])
        if filename[0] == '':
            self.textBrowser_2.append(time.strftime(
                "%H:%M:%S", time.localtime())+"你没有选择路径...")
        else:
            self.filepath = filename[0]
            self.textBrowser_2.append(time.strftime(
                "%H:%M:%S", time.localtime())+"打开文件"+self.filepath)
            with open(self.filepath, 'r') as f:
                my_text = f.read()
            f.close()
            self.plainTextEdit.clear()
            self.plainTextEdit.setPlainText(my_text)

    def btn_save(self):
        if os.getcwd() == self.filepath:
            filename = QFileDialog.getSaveFileName(
                self, '保存文件', str(os.getcwd()), 'Text Files (*.txt)')
            print(filename[0])
            if filename[0] != '':
                self.filepath = filename[0]
                self.btn_save()
            else:
                self.textBrowser_2.append(time.strftime(
                    "%H:%M:%S", time.localtime())+"你没有选择路径...")
        else:
            my_text = str(self.plainTextEdit.toPlainText())
            with open(self.filepath, 'w') as f:
                f.write(my_text)
            f.close()
            self.textBrowser_2.append(time.strftime(
                "%H:%M:%S", time.localtime())+"保存文件成功,路径"+self.filepath)
    
    def pinjie(self,path,counts):
        print('=========pinjie-=====('+str(counts))
        self.textBrowser_2.append(time.strftime(
                    "%H:%M:%S", time.localtime())+'完成'+str((counts-1)/(counts+2)))
        for i in range(1,counts):
            print(self.soundspath+str(i)+".mp3"+'---------'+path)
            result=AudioSegment.from_mp3(path)
            end = AudioSegment.from_mp3(self.soundspath+str(i)+".mp3")
            result = result + end
            result.export(path, format="mp3")
        print(path+'-------------('+str(len(result)))
        self.textBrowser_2.append(time.strftime(
                    "%H:%M:%S", time.localtime())+'完成'+str((counts+2)/(counts+2))+'文件路径为：'+path)
        os.system(path)


    def get_sounds(self,token):
        lines=[]
        for strline in str(self.plainTextEdit.toPlainText()).split('\n'):
                if strline != '':
                    lines.append(strline)

        for i in range(len(lines)):
            if i == 0:
                ipath=self.soundspath+'result'
            else:
                ipath=self.soundspath+str(i)
            #一行请求一次
            getsounds(filepath=ipath,token=token,TEXT=lines[i],PER=self.lcdNumber_3.intValue(),SPD=self.lcdNumber_2.intValue(),PIT=self.lcdNumber.intValue(),VOL=self.lcdNumber_4.intValue()).mainmsg()
            self.textBrowser_2.append(time.strftime(
                    "%H:%M:%S", time.localtime())+'完成'+str(i/(len(lines)+2)))
        
        self.pinjie(path=self.soundspath+'result.mp3',counts=len(lines))

    
        
    
    # 音频的获取
    def save_sounds(self):
        token = fetch_token()
        self.textBrowser_2.append(time.strftime(
                    "%H:%M:%S", time.localtime())+'获取请求')
        if os.getcwd() == self.soundspath:
            filename = QFileDialog.getExistingDirectory(
                self, '选择音频保存位置', self.filepath)
            print(filename)
            if filename != '':
                self.soundspath = filename + os.sep
                self.save_sounds()
            else:
                self.textBrowser_2.append(time.strftime(
                    "%H:%M:%S", time.localtime())+"你没有选择路径...")
        else:
            self.get_sounds(token)

    

    @pyqtSlot()
    def on_action123_triggered(self):
        """
        Slot documentation goes here.
        """
        # 打开文件
        self.btn_open()

    @pyqtSlot()
    def on_action123_3_triggered(self):
        """
        Slot documentation goes here.
        """
        # 保存
        self.btn_save()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        # 主页的测试按钮
        # print("主页的测试按钮")
        self.textBrowser_2.append(time.strftime(
            "%H:%M:%S", time.localtime())+"测试按钮")

        path=getsounds(os.getcwd()+os.sep+'text.txt',fetch_token(),'欢迎使用koco语音助手',4,6,9,5).mainmsg()
        os.system(path)
        
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        # 主页开始按钮
        # print("主页开始按钮")
        self.textBrowser_2.append(time.strftime(
            "%H:%M:%S", time.localtime())+"开始按钮")
        self.save_sounds()


# main方法
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
