#coding=utf-8
import re
import sys

#默认替换字符串
mstr2='''
class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
'''
mstr1='''class Ui_MainWindow(object):'''

# 开始执行替换
if len(sys.argv)==2:
    mf=open(sys.argv[1],'r',-1,'utf8')
    try:
        mstr=mf.read()
        # 针对有些窗口是从Dialog继承下来的做出的对应
        if mstr.find(mstr1)==-1:
            mstr1=mstr1.replace("MainWindow","Dialog")
            mstr2=mstr2.replace("MainWindow","Dialog")
        mstr=mstr.replace(mstr1,mstr2)
    finally:
        mf.close()
    mf=open(sys.argv[1],'w',-1,'utf8')
    try:
        mf.write(mstr)
    finally:
        mf.close()
else:
    print('故障解析:文件名错误')
