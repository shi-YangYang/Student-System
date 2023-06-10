import queue
import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.tooltip import ToolTip
from PIL import Image
from PIL import ImageTk
import re
import Authme_operation as at
import random
import string
import threading
import loading


class Register_gui:#注册页面
    def __init__(self):
        #页面是否打开标志->【0】是未打开,【1】是已经打开
        self.flag = 0
##########################################################################
#页面设置部分
    def _gui_setting(self):#进入页面设置
        self.win = tk.Toplevel()
        self.win.title("注册页面")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        #页面尺寸设置
        self._size_setting()
        #变量设置
        self._variable_setting()
        #样式设置
        self._style_setting()
        #部件载入
        self._widget_setting()
        #图片载入
        self._load_photo()
        #验证码初始化
        self._initialize_captcha()
        #悬浮文字
        self._load_Tooltip()

        self.win.iconbitmap("stbu.ico")  # 设置窗口左上角图标

    def _variable_setting(self):#变量设置
        self.account = tk.StringVar()
        self.password_1 = tk.StringVar()
        self.password_2 = tk.StringVar()
        self.number = tk.StringVar()
        self.captcha = tk.StringVar()
        self.verify_captcha = tk.StringVar()
        #self.name = tk.StringVar()
        #self.academy = tk.StringVar()

    def _style_setting(self):#小部件样式设置
        self.style_button = ttk.Style()
        self.style_button.configure("success.TButton",font=("微软雅黑",25),foreground="black")

    def _widget_setting(self):#页面部件设置
        self.account_label = ttk.Label(self.win,text="账号:",font=("微软雅黑",20))
        self.account_label.place(relx=0.1,rely=0.3)

        self.password_1_label = ttk.Label(self.win,text="密码:",font=("微软雅黑",20))
        self.password_1_label.place(relx=0.1,rely=0.4)

        self.password_2_label = ttk.Label(self.win,text="确认密码:",font=("微软雅黑",20))
        self.password_2_label.place(relx=0.01,rely=0.5)

        self.number_label = ttk.Label(self.win,text="手机号:",font=("微软雅黑",20))
        self.number_label.place(relx=0.05,rely=0.6)

        self.captcha_label = ttk.Label(self.win,text="验证码:",font=("微软雅黑",20))
        self.captcha_label.place(relx=0.05,rely=0.7)

        self.confirm_button = ttk.Button(self.win,text="确认注册",bootstyle="success",command=self._check_information)
        self.confirm_button.place(relx=0.35,rely=0.9,width=200)


        self.account_entry = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.account)
        self.account_entry.place(relx=0.25,rely=0.3)

        self.password_1_entry = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.password_1)
        self.password_1_entry.place(relx=0.25,rely=0.4)

        self.password_2_entry = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.password_2)
        self.password_2_entry.place(relx=0.25,rely=0.5)

        self.number_entry = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.number)
        self.number_entry.place(relx=0.25,rely=0.6)

        self.captcha_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.captcha)
        self.captcha_entry.place(relx=0.25,rely=0.695,width=150,height=50)
        '''
        self.name_label = ttk.Label(self.win,text="姓名:",font=("微软雅黑",20))
        self.name_label.place(relx=0.1,rely=0.7)
        self.academy_label = ttk.Label(self.win,text="学院:",font=("微软雅黑",20))
        self.academy_label.place(relx=0.1,rely=0.8)
        self.name_entry = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.name)
        self.name_entry.place(relx=0.25,rely=0.7)
        self.academy_entry = tk.Entry(self.win,font=("微软雅黑",20),textvariable=self.academy)
        self.academy_entry.place(relx=0.25,rely=0.8)
        '''
    def _creation_captcha(self):#生成验证码函数
        # 定义包含大小写英文字母和数字的字符集
        characters = string.ascii_letters + string.digits
        # 使用 random.choices 从字符集中随机选择 4 个字符，组成一个列表
        random_chars = random.choices(characters, k=4)
        # 将列表中的字符拼接成字符串
        random_string = ''.join(random_chars)
        return random_string

    def _initialize_captcha(self,event=None):#初始化验证码
        self.verify_captcha.set(self._creation_captcha())

    def _size_setting(self):#页面尺寸设置
        #screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        height = (screenHeight - 800) / 2  # 获取屏-幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (600, 800, 1000, height))
##########################################################################

##########################################################################
#图片载入和悬浮文字部分
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

    def _load_photo(self):#加载图片
        self.top_photo = self._photo("photo/reg_top.png",600,200)
        self.top_label = ttk.Label(self.win,image=self.top_photo)
        self.top_label.place(x=0,y=0)

        self.account_photo = self._photo("photo/wenhao.png",40,40)
        self.account_photo_label = ttk.Label(self.win,image=self.account_photo)
        self.account_photo_label.place(relx=0.82,rely=0.3)

        self.password_1_photo = self._photo("photo/wenhao.png",40,40)
        self.password_1_photo_label = ttk.Label(self.win,image=self.password_1_photo)
        self.password_1_photo_label.place(relx=0.82,rely=0.4)

        self.password_2_photo = self._photo("photo/wenhao.png",40,40)
        self.password_2_photo_label = ttk.Label(self.win,image=self.password_2_photo)
        self.password_2_photo_label.place(relx=0.82,rely=0.5)

        self.number_photo = self._photo("photo/wenhao.png",40,40)
        self.number_photo_label = ttk.Label(self.win,image=self.number_photo)
        self.number_photo_label.place(relx=0.82,rely=0.6)

        self.captcha_photo = self._photo("photo/reg-captcha.png",200,50)
        self.captcha_photo_label = ttk.Label(self.win,image=self.captcha_photo,textvariable=self.verify_captcha,
                                             foreground="red",compound="center",font=("微软雅黑",20))
        self.captcha_photo_label.bind("<Button-1>",self._initialize_captcha)
        self.captcha_photo_label.place(relx=0.5,rely=0.693)

        '''
        self.name_photo = self._photo("photo/wenhao.png",40,40)
        self.name_photo_label = ttk.Label(self.win,image=self.name_photo)
        self.name_photo_label.place(relx=0.82,rely=0.7)

        self.academy_photo = self._photo("photo/wenhao.png",40,40)
        self.academy_photo_label = ttk.Label(self.win,image=self.academy_photo)
        self.academy_photo_label.place(relx=0.82,rely=0.8)
        '''

    def _load_Tooltip(self):#导入图片上悬浮文字
        self.account_text = "账号长度请保持在4-16长度之间.\n账号仅支持数字和字母."
        ToolTip(self.account_photo_label,text=self.account_text)

        self.password_1_text = "密码长度请保持在4-16之间.\n密码仅支持字母和数字."
        ToolTip(self.password_1_photo_label,text=self.password_1_text)
        self.password_2_text = "请再输入一次密码,请确保两次密码一致."
        ToolTip(self.password_2_photo_label,text=self.password_2_text)

        self.number_text = "请输入合法的11位长度中国大陆手机号."
        ToolTip(self.number_photo_label,text=self.number_text)

        self.captcha_text = "点击刷新."
        ToolTip(self.captcha_photo_label,text=self.captcha_text)

        '''
        self.name_text = "请输入您的真实姓名.\n姓名只能是中文."
        ToolTip(self.name_photo_label,text=self.name_text)

        self.academy_text = "请输入您所在的学院.\n学院名只能是中文."
        ToolTip(self.academy_photo_label,text=self.academy_text)
        '''
##########################################################################

##########################################################################
#功能实现部分
    def _check_information(self):#检查注册内容是否合法

        def judgement_empty(account, password_1, password_2, number,captcha):
            if account == "":
                tk.messagebox.showinfo("账号为空", "账号不能为空",parent=self.win)
                return 0
            if password_1 == "":
                tk.messagebox.showinfo("密码为空", "密码不能为空",parent=self.win)
                return 0
            if password_2 == "":
                tk.messagebox.showinfo("确认密码为空", "确认密码不能为空",parent=self.win)
                return 0
            if number == "":
                tk.messagebox.showinfo("手机号为空", "手机号不能为空",parent=self.win)
                return 0
            if captcha == "":
                tk.messagebox.showinfo("验证码为空", "验证码不能为空",parent=self.win)
                return 0
            '''
            if name == "":
                tk.messagebox.showinfo("姓名为空", "姓名不能为空",parent=self.win)
                return 0
            if academy == "":
                tk.messagebox.showinfo("学院为空", "学院不能为空",parent=self.win)
                return 0
            '''
            return 1

        def j_account(account):  # 判断账号是否合法
            if not 4 <= len(account) <= 16:
                messagebox.showinfo("长度有误", "账号长度只能在4~16之间",parent=self.win)
                return 0
            for i in account:
                if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    messagebox.showinfo("非法字符", "账号名只能是英文字母和阿拉伯数字",parent=self.win)
                    return 0
            return 1

        def j_password_1(password_1):  # 判断密码是否合法
            if not 4 <= len(password_1) <= 16:
                messagebox.showinfo("长度有误", "密码长度只能在4~16之间",parent=self.win)
                return 0
            for i in password_1:
                if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    messagebox.showinfo("非法字符", "密码只能是英文字母和阿拉伯数字",parent=self.win)
                    return 0
            return 1

        def j_password_2(password_1, password_2):  # 判断确认密码是否合法
            if password_1 != password_2:
                messagebox.showinfo("密码错误", "两次密码不一致",parent=self.win)
                return 0
            return 1

        def j_number(number):  # 判断手机号是否合法
            if len(number) != 11:
                messagebox.showinfo("手机号长度有误", "手机号必须是11位合法手机号",parent=self.win)
                return 0
            for i in number:
                if i not in "0123456789":
                    messagebox.showinfo("手机号非法", "手机号必须是阿拉伯数字！",parent=self.win)
                    return 0
            return 1

        def j_captcha(captcha):  # 判断手机号是否合法
            if captcha != self.verify_captcha.get():
                messagebox.showinfo("验证码错误", "验证码错误,请重试或刷新验证码", parent=self.win)
                return 0
            return 1

        '''
        def j_name(name):  # 判断姓名是否合法
            flag = re.findall('[^\u4e00-\u9fa5]',name)
            if len(flag) != 0:
                messagebox.showinfo("非法字符", "姓名只能是中文",parent=self.win)
                return 0
            if not 1 <= len(name) <= 6:
                messagebox.showinfo("长度有误", "姓名长度只能在1~6之间",parent=self.win)
                return 0
            return 1

        def j_academy(academy):#判断学院是否合法
            flag = re.findall('[^\u4e00-\u9fa5]', academy)
            if len(flag) != 0:
                messagebox.showinfo("非法字符", "学院名只能是中文",parent=self.win)
                return 0
            if not 1 <= len(name) <= 16:
                messagebox.showinfo("长度有误", "学院名长度只能在1~16之间",parent=self.win)
                return 0
            return 1
            
        name = self.name.get()
        academy = self.academy.get()
        '''
        account = self.account.get()
        password_1 = self.password_1.get()
        password_2 = self.password_2.get()
        number = self.number.get()
        captcha = self.captcha.get()

        if judgement_empty(account,password_1,password_2,number,captcha):
            if j_account(account) and j_password_1(password_1) and j_password_2(password_1,password_2) and j_number(number) and j_captcha(captcha):
                #启动加载中页面
                self._loading_threading()
                #启动多线程函数验证注册操作
                self._threading(account, password_1, number)

##########################################################################
#多线程部分
    def _threading(self,account, password_1, number):
        def th(account, password_1, number):
            flag = at.register(account, password_1, number)
            q.put(flag)
            #遍历线程是否结束
            for i in range(100):
                time.sleep(1)
                if not q.empty():
                    v = q.get()
                    if v == 0:
                        messagebox.showinfo("账号已存在", "注册失败,账号已经存在，请尝试更换账号.", parent=self.win)
                        #关闭加载中页面
                        self.loading._exit()
                        break
                    elif v == 1:
                        messagebox.showinfo("注册失败", "请检查您的网络,并稍后再试,若多次提示,请尝试与管理员联系.", parent=self.win)
                        #关闭加载中页面
                        self.loading._exit()
                        break
                    elif v == 2:
                        messagebox.showinfo("注册成功", "恭喜,注册成功,快去登陆吧.", parent=self.win)
                        #关闭加载中页面
                        self.loading._exit()
                        #关闭注册页面
                        self._exit()
                        break
                    elif v == 'connect is error':
                        messagebox.showinfo("网络异常", "请检查网络后重试.", parent=self.win)
                        #关闭加载中页面
                        self.loading._exit()
        q = queue.Queue()
        t = threading.Thread(target=th,args=(account, password_1, number))
        t.start()

    def _loading_threading(self):#加载中页面函数
        self.loading = loading.Create_Loading("photo/login-load.gif", 400, 400)
        def th():
            self.loading._run()
        t=threading.Thread(target=th)
        t.start()
##########################################################################

##########################################################################
#页面进入与关闭部分
    def _start(self):#页面进入
        if self.flag == 0:
            self.flag = 1
            #进入页面设置
            self._gui_setting()
        else:
            messagebox.showwarning("错误","你已经打开注册页面了.")

    def _exit(self):#页面退出
        #重新设置页面打开变量为0
        self.flag = 0
        self.win.destroy()
##########################################################################