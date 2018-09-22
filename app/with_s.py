import datetime,time
import os,sys
import sqlite3
# from pysqlcipher import dbapi2 as sqlite3

file_name=sys.path[0]+'/'+'rz.db'
# print(file_name)
# file_name='d:\pf_win10\server\rz.new\rz.db'

class project_data():
    def __init__(self,filename=file_name,password='ddd'):
        '''初始化'''
        self.filename=filename
        self.password=password
        if os.path.isfile(self.filename)==False:
            self.init_success=False
        if os.path.isfile(self.filename+'.lock')==True:
            self.init_success=False
        else:
            conn = sqlite3.connect(self.filename)
            # mstr= '"pragma key="' + self.password + 'testing"; pragma kdf_iter=64000;"'
            # db.executescript(mstr)
            self.init_success=True


    def testWrite(self,c_datetime,c_text):
        '''写入信息'''
        conn = sqlite3.connect(self.filename)
        # mstr= '"pragma key="' + self.password + 'testing"; pragma kdf_iter=64000;"'
        # db.executescript(mstr)
        # print(c_text)
        # print(c_datetime)
        mstr= str('INSERT INTO main VALUES(datetime("' + c_datetime + '"),"' + c_text + '")')
        # print(mstr)
        conn.execute(mstr)
        conn.commit()
