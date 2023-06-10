import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter.filedialog import *
from ttkbootstrap.tooltip import ToolTip
from sql import MySQL
from PIL import Image
from PIL import ImageTk
import pandas as pd
import threading
import queue
import os
import re


class Excel_Gui:#excel操作类
    def __init__(self,instance,win,id):
        #页面是否打开标志->【False】是未打开,【True】是已经打开
        self.flag = False
        #用户id
        self.user_id = id
        #父窗体
        self.original_gui = win
        #学生管理页面实例->更新数据
        self.student_instance = instance

##########################################################################
# 页面设置部分
    def _gui_setting(self):#页面设置
        self.win = ttk.Toplevel(self.original_gui)
        self.win.title("批量处理")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        #页面尺寸设置
        self._size_setting()
        #图片载入
        self._load_photo()
        #页面基本设置
        self._base_setting()
        #悬浮文字载入
        self._load_tooltip()

        #上传Excel文件页面实例
        self.upload_instance = Excel_Upload(self.student_instance,self.user_id)
        #下载Excel文件页面实例
        self.download_instance = Excel_Download(self.user_id)

        self.win.iconbitmap("stbu.ico")  # 设置窗口左上角图标

    def _size_setting(self):#页面尺寸设置
        screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        width = (screenWidth - 600) / 2#获取屏幕宽度
        height = (screenHeight - 400) / 2  # 获取屏幕高度大小
        self.win.geometry('%dx%d+%d+%d' % (600, 400,width,height))

    def _load_photo(self):#图片载入
        self.upload_photo = self._photo("photo/excel_upload.png", 200, 200)
        self.download_photo = self._photo("photo/excel_download.png",200,200)

    def _base_setting(self):#基本设置
        #label标签
        self.upload_label = ttk.Label(self.win,text="上传",foreground='purple',font=("微软雅黑",20))
        self.upload_label.place(relx=0.19,rely=0.06)

        self.download_label = ttk.Label(self.win,text="下载",foreground='red',font=("微软雅黑",20))
        self.download_label.place(relx=0.73,rely=0.06)

        #Button按钮
        self.upload_button = ttk.Button(self.win,image=self.upload_photo,bootstyle="light",command=self._open_upload_gui)
        self.upload_button.place(relx=0.05,rely=0.2)

        self.download_button = ttk.Button(self.win,image=self.download_photo,bootstyle="light",command=self._open_download_gui)
        self.download_button.place(relx=0.6,rely=0.2)

    def _load_tooltip(self):#悬浮文字载入
        self.upload_text = "点击进入Excel批量载入."
        ToolTip(self.upload_button,text=self.upload_text)

        self.download_text = "点击进入Excel批量下载."
        ToolTip(self.download_button,text=self.download_text)
##########################################################################

##########################################################################
#图片设置部分
    def _resize(self, w, h, w_box, h_box, pill_image):
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        # 强制图片缩放后的宽度和高度比例与要放置的区域的宽度和高度比例一致
        factor = max([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pill_image.resize((width, height), resample=Image.LANCZOS)

    def _photo(self, path, w_box, h_box):  # 图片
        im = Image.open(path)
        w, h = im.size
        im = self._resize(w, h, w_box, h_box, im)
        photo_object = ImageTk.PhotoImage(im)
        return photo_object
##########################################################################

##########################################################################
#页面跳转与页面打开和关闭部分
    def _open_upload_gui(self):#打开上传页面
        self.upload_instance._start()

    def _open_download_gui(self):#打开下载页面
        self.download_instance._start()

    def _start(self):#页面进入
        if self.flag == False:
            self.flag = True
            #页面设置
            self._gui_setting()
        else:
            messagebox.showwarning("禁止重复打开","页面已打开,请仔细找找.",parent=self.win)

    def _exit(self):#页面退出
        self.flag = False
        self.win.destroy()
##########################################################################



class Excel_Upload:#Excel数据文件上传类
    def __init__(self,instance,id):
        # 页面是否打开标志->【False】是未打开,【True】是已经打开
        self.flag = False
        # 用户id
        self.user_id = id
        #连接池实例
        self.pool = MySQL()
        #判断任务是否结束的标志队列
        self.queue = queue.Queue()
        #学生管理页面实例->更新数据
        self.student_instance = instance

##########################################################################
# 页面跳转与页面打开和关闭部分
    def _gui_setting(self):#页面设置
        self.win = ttk.Toplevel()
        self.win.title("批量上传")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        #部件样式设置
        self._style_setting()
        #页面尺寸设置
        self._size_setting()
        #变量设置
        self._variable_setting()
        #页面基本设置
        self._base_setting()

        self.win.iconbitmap("stbu.ico")  # 设置窗口左上角图标

    def _style_setting(self):#部件样式设置
        #按钮样式
        self.style_button = ttk.Style()
        self.style_button.configure("TButton", font=("微软雅黑", 20), foreground="black")
        #进度条样式
        self.style = ttk.Style()
        # 设置进度条宽度
        self.style.configure("success.Horizontal.TProgressbar", thickness=20)

    def _size_setting(self):#页面尺寸设置
        screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        width = (screenWidth - 800) / 2#获取屏幕宽度
        height = (screenHeight - 400) / 2  # 获取屏幕高度大小
        self.win.geometry('%dx%d+%d+%d' % (800, 400,width,height))

    def _variable_setting(self):#变量设置
        #文件路径
        self.file_path = tk.StringVar()

    def _base_setting(self):#页面基本设置
        #label设置
        self.file_label = ttk.Label(self.win,text="文件:",foreground='black',font=("微软雅黑",20))
        self.file_label.place(relx=0.05,rely=0.1)

        #entry设置
        self.file_entry = ttk.Entry(self.win,textvariable=self.file_path,font=("微软雅黑",15),foreground='red')
        self.file_entry.place(relx=0.15,rely=0.1,width=500,height=40)

        #button设置
        self.file_button = ttk.Button(self.win,text="选择文件",command=self._select_file,bootstyle="success")
        self.file_button.place(relx=0.8,rely=0.09)

        self.confirm_button = ttk.Button(self.win,text="确认上传",command=self._confirm_operation,bootstyle='outline-danger')
        self.confirm_button.place(relx=0.4,rely=0.5)

        #进度条创建
        self.progress_bar = ttk.Progressbar(self.win,style="success.Horizontal.TProgressbar", length=700, mode="determinate")
        #最大值
        self.progress_bar['maximum'] = 100
        #初始值

        self.progress_bar['value'] = 0
        self.progress_bar.place(relx=0.05,rely=0.8)

##########################################################################

##########################################################################
#功能实现部分
    def _select_file(self):#选择文件函数
        self.file_path.set(askopenfilename())

    def _confirm_operation(self):#按钮确认操作
        #判断文件是否为空
        if self.file_path.get() == '':
            messagebox.showwarning("错误","你还没有上传文件.",parent=self.win)
            return
        #判断文件是否为xlsx文件
        path,file_name = os.path.splitext(self.file_path.get())
        if file_name.lower() != '.xlsx':
            messagebox.showerror("格式错误","请选择xlsx文件格式的文件！",parent=self.win)
            return
        #基于用户缓冲操作，是否确认上传.
        flag = messagebox.askyesno("警告","上传excel批量数据需要一定时间处理.\n同时,该操作无法撤回.\n请问是否继续?",parent=self.win)
        if flag == True:
            self._upload_excel()

    def _upload_excel(self):#给数据库上传数据函数
        #查询用户学生表中所有属性名
        sql_column = f'SHOW columns FROM student_{self.user_id}'
        temporary_result = self.pool._execute_excel(sql_column,method='sql_column')
        temporary_result = [item[0] for item in temporary_result]
        #除了id的所有属性名
        self.column = temporary_result[1:]
        #计算属性数量
        self.column_number = len(self.column)
        #读取路径里的excel文件
        self.pd_file = pd.read_excel(self.file_path.get())
        #令页面无法操作
        self.win.attributes("-disabled",1)
        #进入多线程
        self._threading_upload()
        #开始加载进度条
        self._progress_bar_show()

    def _threading_upload(self):#多线程上传
        def th():
            for index, row in self.pd_file.iterrows():
                # 存储每一行的值
                values = []
                #只遍历用户属性个数的列数->例如:用户属性为【5】个，则只遍历前5列
                for column in self.pd_file.columns[:self.column_number]:
                    value = row[column]
                    # 检查单元格是否为空
                    if pd.isnull(value):
                        # 将空值设置为空字符串
                        value = ''
                    values.append(value)
                #构建插入数据的SQL语句
                #map推导
                map = {'学号':'sno','姓名':'name','性别':'gender','专业':'subject','手机号':'num','家庭住址':'home'}
                #根据map推导获得columns
                columns = [map.get(x,x) for x in self.pd_file.columns[:self.column_number]]
                #将columns拼凑成【sql】语句的格式
                columns = ",".join(str(item) for item in columns[:self.column_number])
                # 创建相应数量的占位符
                placeholders = ",".join(["%s"] * self.column_number)
                #拼凑最终的【sql】语句
                sql = f"INSERT INTO student_{self.user_id} ({columns}) VALUES ({placeholders})"
                values = tuple(values)
                #执行数据库操作
                self.pool._execute_excel(sql,method='sql_add',elements=values)
            self.student_instance._update_data()#->更新学生页面数据
            #数据库操作完成,进入回调函数，扫尾工作
            self.queue.put('ok')

        t = threading.Thread(target=th)
        t.start()

    def _progress_bar_show(self):#进度条更新
        for i in range(100):
            #如果任务结束了，进度条立马满
            if not self.queue.empty():
                #将队列数据取出来
                v = self.queue.get()
                #执行扫尾函数
                self._finish()
                break
            #如果值为100了，则立马停止循环
            if self.progress_bar['value'] == 100:
                break
            #每次值+1
            self.progress_bar['value'] = i+1
            self.win.update()
            time.sleep(0.4)

    def _finish(self):#扫尾函数
        #令进度条值为100
        self.progress_bar['value'] = 100
        #弹窗提醒用户已经完成
        messagebox.showinfo("成功","数据已经成功提交",parent=self.win)
        #令进度条值归0
        self.progress_bar['value'] = 0
        #令页面可以操作
        self.win.attributes("-disabled",0)
        #清空输入框
        self.file_path.set('')

##########################################################################

##########################################################################
#页面打开和关闭
    def _start(self):#页面进入
        if self.flag == False:
            self.flag = True
            #页面设置
            self._gui_setting()
        else:
            messagebox.showwarning("禁止重复打开","页面已打开,请仔细找找.",parent=self.win)

    def _exit(self):#页面退出
        self.flag = False
        self.win.destroy()
##########################################################################





class Excel_Download:#Excel数据文件下载类
    def __init__(self,id):
        # 页面是否打开标志->【False】是未打开,【True】是已经打开
        self.flag = False
        # 用户id
        self.user_id = id
        #连接池实例
        self.pool = MySQL()
        #判断【sql】语句是否返回的队列
        self.queue_rt = queue.Queue()
        #判断任务是否结束的标志队列
        self.queue = queue.Queue()

##########################################################################
# 页面跳转与页面打开和关闭部分
    def _gui_setting(self):#页面设置
        self.win = ttk.Toplevel()
        self.win.title("批量上传")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        #部件样式设置
        self._style_setting()
        #页面尺寸设置
        self._size_setting()
        #变量设置
        self._variable_setting()
        #页面基本设置
        self._base_setting()

        self.win.iconbitmap("stbu.ico")  # 设置窗口左上角图标

    def _style_setting(self):#部件样式设置
        #按钮样式
        self.style_button = ttk.Style()
        self.style_button.configure("TButton", font=("微软雅黑", 20), foreground="black")
        #进度条样式
        self.style = ttk.Style()
        # 设置进度条宽度
        self.style.configure("success.Horizontal.TProgressbar", thickness=20)

    def _size_setting(self):#页面尺寸设置
        screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        width = (screenWidth - 800) / 2#获取屏幕宽度
        height = (screenHeight - 400) / 2  # 获取屏幕高度大小
        self.win.geometry('%dx%d+%d+%d' % (800, 400,width,height))

    def _variable_setting(self):#变量设置
        #文件保存路径
        self.file_save_path = tk.StringVar()
        #文件名
        self.file_name = tk.StringVar()

    def _base_setting(self):#页面基本设置
        #label设置
        self.file_label = ttk.Label(self.win,text="保存位置:",foreground='black',font=("微软雅黑",20))
        self.file_label.place(relx=0,rely=0.1)

        self.file_name_label = ttk.Label(self.win,text="保存名:",foreground='black',font=("微软雅黑",20))
        self.file_name_label.place(relx=0.02, rely=0.25)

        #entry设置
        self.file_entry = ttk.Entry(self.win,textvariable=self.file_save_path,font=("微软雅黑",15),foreground='red')
        self.file_entry.place(relx=0.15,rely=0.1,width=500,height=40)

        self.file_name_entry = ttk.Entry(self.win,textvariable=self.file_name,font=("微软雅黑",15),foreground='red')
        self.file_name_entry.place(relx=0.15,rely=0.25,width=500,height=40)

        #button设置
        self.file_button = ttk.Button(self.win,text="选择位置",command=self._select_file_path,bootstyle="success")
        self.file_button.place(relx=0.8,rely=0.09)

        self.confirm_button = ttk.Button(self.win,text="确认下载",command=self._confirm_operation,bootstyle='outline-danger')
        self.confirm_button.place(relx=0.4,rely=0.5)

        #进度条创建
        self.progress_bar = ttk.Progressbar(self.win,style="success.Horizontal.TProgressbar", length=700, mode="determinate")
        #最大值
        self.progress_bar['maximum'] = 100
        #初始值
        self.progress_bar['value'] = 0
        self.progress_bar.place(relx=0.05,rely=0.8)

##########################################################################

##########################################################################
#功能实现部分
    def _select_file_path(self):#选择文件路径函数
        self.file_save_path.set(askdirectory())

    def _confirm_operation(self):#按钮确认操作
        #判断文件是否为空
        if self.file_save_path.get() == '':
            messagebox.showwarning("错误","你还没有上传文件.",parent=self.win)
            return

        #判断文件名字是否为空
        if self.file_name.get() == '':
            messagebox.showwarning("错误","你还没有输入文件名字.",parent=self.win)
            return

        #判断是否为合法的路径格式
        dir = os.path.isdir(self.file_save_path.get())
        if dir == False:
            messagebox.showerror("格式错误","请选择正确的路径格式",parent=self.win)
            return

        #判断文件名是否合法
        # 匹配非单词字符和非空白字符
        pattern = r'[^\w\s]'
        result = re.search(pattern,self.file_name.get())
        if result is not None:
            messagebox.showerror("错误","文件名只能是数字,汉字,英文字符.\n不能包含特殊字符,空格,标点符号.",parent=self.win)
            return
        #基于用户缓冲操作，是否确认上传.
        flag = messagebox.askyesno("提示","下载excel批量数据需要一定时间处理.\请耐心等待,下载完成的提示!",parent=self.win)
        if flag == True:
            self._download_excel()

    def _download_excel(self):#给数据库上传数据函数
        #查询用户学生表中所有属性名
        sql_column = f'SHOW columns FROM student_{self.user_id}'
        temporary_result = self.pool._execute_excel(sql_column,method='sql_column')
        temporary_result = [item[0] for item in temporary_result]
        #除了id的所有属性名
        self.column = temporary_result[1:]
        # map推导
        map = {'sno': '学号', 'name': '姓名', 'gender': '性别', 'subject': '专业', 'num': '手机号', 'home': '家庭住址'}
        # 根据map推导获得column_extra
        self.column_extra = [map.get(x, x) for x in self.column]
        #令页面无法操作
        self.win.attributes("-disabled",1)
        #进入多线程
        self._threading_download()
        #开始加载进度条
        self._progress_bar_show()

    def _threading_download(self):#多线程上传
        def th():
            #拼凑临时的属性列
            temporary = ','.join(self.column)
            # 查询除了id列所有数据的【sql】语句
            sql_query = f'SELECT {temporary} FROM student_{self.user_id}'
            result = self.pool._execute_excel(sql_query,method='sql_query')
            self.queue_rt.put(result)
            #传递任务结束，进度条可以关闭的标志
            self.queue.put('ok!')

        t = threading.Thread(target=th)
        t.start()

    def _progress_bar_show(self):#进度条更新
        for i in range(100):
            #如果任务结束了，进度条立马满
            if not self.queue.empty():
                #将队列数据取出来
                v = self.queue.get()
                #执行保存文件函数
                self._save_operation()
                #执行扫尾函数
                self._finish()
                break
            #如果值为100了，则立马停止循环
            if self.progress_bar['value'] == 100:
                break
            #每次值+1
            self.progress_bar['value'] = i+1
            self.win.update()
            time.sleep(0.3)

    def _save_operation(self):#保存文件函数
        if not self.queue_rt.empty():
            result = self.queue_rt.get()
            #创建df迭代对象
            df = pd.DataFrame(result,columns=self.column_extra)
            df.to_excel(self.file_save_path.get() + '/' + self.file_name.get() + '.xlsx',index=False)

    def _finish(self):#扫尾函数
        #令进度条值为100
        self.progress_bar['value'] = 100
        #弹窗提醒用户已经完成
        messagebox.showinfo("成功","数据已经成功下载",parent=self.win)
        #令进度条值归0
        self.progress_bar['value'] = 0
        #令页面可以操作
        self.win.attributes("-disabled",0)

##########################################################################

##########################################################################
#页面打开和关闭
    def _start(self):#页面进入
        if self.flag == False:
            self.flag = True
            #页面设置
            self._gui_setting()
        else:
            messagebox.showwarning("禁止重复打开","页面已打开,请仔细找找.",parent=self.win)

    def _exit(self):#页面退出
        self.flag = False
        self.win.destroy()
##########################################################################


#测试
'''
a = tk.Tk()
b = Excel_Gui(a,12)
b._start()
a.mainloop()
'''