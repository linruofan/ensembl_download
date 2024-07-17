# fr0 24.7.17 version 2.0.0
# download seq from ensembl
# -*- coding: utf-8 -*-
import requests
import pandas as pd
import os
import re
import sys
import tkinter as t
import tkinter.filedialog
import time
from tkinter import ttk
class ground():
    file_path = ''

    def __init__(self):
        self.tdb = t.Tk()
        self.tdb.geometry("400x300")
        self.tdb.title('')
        d1 = t.Label(self.tdb, text='选择记录序列名的excel文件')
        d1.pack()
        self.b1 = t.Entry(self.tdb)
        self.b1.insert(0, self.file_path)
        self.b1.pack()
        choose_file_button = t.Button(self.tdb, text='选择文件', command=self.selectPath)
        choose_file_button.pack()
        self.com = ttk.Combobox()     # #创建下拉菜单
        self.com.pack()     # #将下拉菜单绑定到窗体
        self.com["value"] = ("","cds", "genomic", "protein")    # #给下拉菜单设定值
        self.com.current(0)    # #设定下拉菜单的默认值为第0个
        self.type = ''
        logs = t.Button(self.tdb, text='下载', command=self.upcount)
        logs.pack()
        self.progressbarOne = tkinter.ttk.Progressbar()
        self.progressbarOne.pack(pady=20)
        self.progressbarOne['maximum'] = 100# 进度值最大值
        self.progressbarOne['value'] = 0 # 进度值初始值
        self.download_notice =t.StringVar()
        self.download_notice.set('not downloading...')
        l = t.Label(self.tdb, textvariable = self.download_notice )
        l.pack()
        self.tdb.mainloop()
        
    def xFunc(self):
        self.type=self.com.get()
    
    def selectPath(self):
        #选择文件path_接收文件地址
        _path = tkinter.filedialog.askopenfilename()
        
        #_path=_path.replace("/","\\\\")
        self.file_path=_path
        self.b1.delete(0, t.END)
        self.b1.insert(0, self.file_path)
    
            
    def upcount(self):
        #/home/fr0/Documents/data/other/AtRLK.xlsx
        self.xFunc()
        self.file_path = self.b1.get()
        print(self.file_path)
        dir_path= os.path.dirname(self.file_path)
        excel = pd.read_excel( self.file_path)
        all_number = excel.shape[0]*excel.shape[1]
        i=0
        ls = excel.T.values
        server = "https://rest.ensembl.org"
        for l in ls:
            if not os.path.exists(os.path.join(dir_path,l[0])):
                os.mkdir(os.path.join(dir_path,l[0]))
            for id in l[1:]:
                if type(id) == str:
                    if re.search('\s',id):
                        continue
                    id = id.split(".cds")[0]
                    if len(self.type) >0:
                        ext = f"/sequence/id/{id}?type={self.type}"
                        _n = f'{id}.{self.type}.fasta'
                    else:
                        ext = f"/sequence/id/{id}?"
                        _n = f'{id}.fasta'
                    if not os.path.exists(os.path.join(dir_path,l[0],_n)):
                        r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
                        
                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()
                        
                        with open(os.path.join(dir_path,l[0],_n), 'w') as f:
                            f.write(r.text)
                        self.download_notice.set(f'{id}.{self.type}.fasta downloaded successfully.')
                        time.sleep(1)
                i+=1
                print(i)
                self.progressbarOne['value'] = i / all_number * 100
                self.tdb.update()
        print(all_number)

            
ground()
