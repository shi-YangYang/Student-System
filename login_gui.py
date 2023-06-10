import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.tooltip import ToolTip
import Authme_operation as at
from PIL import Image
from PIL import ImageTk
import main_gui
import register_gui
import queue
import threading
import loading
import sys
import os,signal

class Login_gui:#登陆界面
    def __init__(self):#初始化
        self.win = tk.Tk()
        self.style = ttk.Style("litera")
        self.win.title("学籍管理系统V2.0")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        #部件样式设置
        self._style_setting()
        #变量设置
        self._variable_setting()
        #页面尺寸设置
        self._size_setting()
        #基本设置
        self._base_setting()
        #图片载入
        self._load_photo()
        #悬浮文字
        self._load_Tooltip()
        # 进入主页面实例
        self.maingui = main_gui.Main_Gui()
        #进入注册页面实例
        self.reg = register_gui.Register_gui()
        #加载中实例
        self.loading_instance = None
        # 设置窗口左上角图标
        self.win.iconbitmap("stbu.ico")

##########################################################################
#页面设置部分
    def _variable_setting(self):#变量设置
        self.account = tk.StringVar()
        self.password = tk.StringVar()

    def _size_setting(self):#尺寸设置
        screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        left = (screenWidth - 1000) / 2  # 获取屏幕左方大小
        height = (screenHeight - 700) / 2  # 获取屏幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (1000, 700, left, height))

    def _base_setting(self):#基础设置
        self.mainlabel_1 = ttk.Label(self.win, text="账号:", font=("微软雅黑", 20))# 用户
        self.mainlabel_1.place(relx=0.65,rely=0.4)

        self.mainlabel_2 = ttk.Label(self.win, text="密码:", font=("微软雅黑", 20))  # 密码
        self.mainlabel_2.place(relx=0.65,rely=0.5)

        self.bt1 = ttk.Button(self.win, text='注册账号',command=self._switch_reg_gui,style="my.TButton")  # 注册按钮
        self.bt1.place(relx=0.74,rely=0.7)

        self.bt2 = ttk.Button(self.win, text='登录账号',command=self._login,style="my.TButton")  # 登录按钮
        self.bt2.place(relx=0.74,rely=0.6)

        self.et1 = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.account)  # 用户账号
        self.et1.place(relx=0.72,rely=0.405,height=33,width=200)

        self.et2 = tk.Entry(self.win,font=("微软雅黑",20),show="*",textvariable=self.password)  # 用户密码
        self.et2.place(relx=0.72,rely=0.505,height=33,width=200)

    def _style_setting(self):#部件样式设置
        self.style_button = ttk.Style()
        self.style_button.configure("my.TButton",font=('微软雅黑',20))
##########################################################################

##########################################################################
#功能实现部分
    def _login(self):#登录函数
        account = self.account.get()
        password = self.password.get()

        def chekck_empty(account,password):
            if account == "":
                tk.messagebox.showinfo("失败", "账号名不能为空.",parent=self.win)
                return 0
            else:
                if password == "":
                    tk.messagebox.showinfo("失败", "密码不能为空.",parent=self.win)
                    return 0
                else:
                    return 1

        def check_legal_account(account):#判断账号是否合法
            if not 4 <= len(account) <= 16:
                messagebox.showinfo("长度有误", "账号长度只能在4~16之间",parent=self.win)
                return 0
            for i in account:
                if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    messagebox.showinfo("非法字符", "账号名只能是英文字母和阿拉伯数字",parent=self.win)
                    return 0
            return 1

        def check_legal_password(password):#判断密码是否合法
            if not 4 <= len(password) <= 16:
                messagebox.showinfo("长度有误", "密码长度只能在4~16之间",parent=self.win)
                return 0
            for i in password:
                if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    messagebox.showinfo("非法字符", "密码只能是英文字母和阿拉伯数字",parent=self.win)
                    return 0
            return 1

        if chekck_empty(account,password):
            if check_legal_account(account) and check_legal_password(password):
                #隐藏页面
                self.win.withdraw()
                #开启加载中动画页面函数
                self._start_loading()
                #验证账号密码是否正确
                self._verify_threading(account,password)

    def _switch_reg_gui(self):#跳转到注册页面
        self.reg._start()

##########################################################################
# 图片加载与悬浮文字部分
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

    def _load_photo(self):#图片放置
        self.left_photo = self._photo("photo/login_left.png",600,700)
        self.left_label = ttk.Label(self.win,image=self.left_photo)
        self.left_label.place(x=0,y=0)

        self.top_photo = self._photo("photo/top_login.png",400,200)
        self.top_label = ttk.Label(self.win,image=self.top_photo)
        self.top_label.place(x=602,y=0)

        self.account_photo = self._photo("photo/wenhao.png",40,40)
        self.account_label = ttk.Label(self.win,image=self.account_photo)
        self.account_label.place(relx=0.93,rely=0.4)

        self.password_photo = self._photo("photo/wenhao.png",40,40)
        self.password_label = ttk.Label(self.win,image=self.password_photo)
        self.password_label.place(relx=0.93,rely=0.49)

    def _load_Tooltip(self):#载入图片上悬浮文字
        self.account_text = "若没有账号,请先注册账号."
        ToolTip(self.account_label,text=self.account_text)

        self.password_text="若忘记密码,可以点击找回密码."
        ToolTip(self.password_label,text=self.password_text)
##########################################################################

##########################################################################
#加载中页面部分[多线程部分]
    def _verify_threading(self,account,password):#多线程函数
        def th(account,password):#判断信息是否正确
            result = at.authme(account, password)
            q.put(result)
            # 循环等待上面的【t1】线程结束
            for i in range(100):
                # 每次循环休息1秒
                time.sleep(1)
                if not q.empty():
                    id = q.get()
                    if id == 'connect is error':  # 网络错误:
                        tk.messagebox.showerror("网络异常", "请检查你的网络连接后,重新尝试.", parent=self.win)
                        # 关闭加载中页面
                        self.loading_instance._exit()
                        #继续下一步操作->根据验证结果给出相应答复
                        self._continue(id)
                        break
                    elif id != 0:
                        #继续下一步操作->根据验证结果给出相应答复
                        self._continue(id)
                        break
                    else:
                        tk.messagebox.showinfo("失败", "用户名或密码错误.", parent=self.win)
                        #继续下一步操作->根据验证结果给出相应答复
                        self._continue(id)
                        break
        #创建一个队列->存储登陆成功与否标志
        q = queue.Queue()
        #创建一个多线程->判断信息是否正确
        t1 = threading.Thread(target=th,args=(account,password))
        t1.start()

    def _start_loading(self):#启动加载中页面
        # 创建加载中页面实例
        self.loading_instance = loading.Create_Loading("photo/login-load.gif", 400, 400)
        def th():
            #启动这个实例
            self.loading_instance._run()

        t = threading.Thread(target=th)
        #将该线程设置为守护线程
        t.daemon = True
        t.start()

    def _continue(self,id):
        if id == 'connect is error':
            #网络错误，重新显示登陆页面
            self.win.deiconify()
            '''
            强制杀死进程模式，【待修改为更好的方法】
            process = 'taskkill /f /pid %s' %os.getpid()
            os.system(process)
            '''
        elif id != 0:
            # 登陆成功，进入主页面
            self.maingui._start(self.loading_instance,id)
        else:
            # 关闭加载中页面
            self.loading_instance._exit()
            # 登陆失败，重新显示登陆页面
            self.win.deiconify()
##########################################################################
    def _exit(self):#退出页面
        self.win.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = Login_gui()
    root.win.mainloop()