import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import time
import operation_gui
import sql
from MySQL_config import config
import threading
import sys
import webbrowser
import os

class Main_Gui():
##########################################################################
#页面基础设置
    def _gui_setting(self, id):
        self.user_id = id
        self._pymysql()
        self.win = tk.Toplevel()
        self.win.title("学籍管理系统V2.0")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self._exit)  # 设置关闭该页面执行的操作
        #页面尺寸设置
        self._size_setting()
        #样式设置
        self._style_setting()
        #变量设置
        self._variable_setting()
        #页面基本设置
        self._base_setting()
        # 载入label
        self._load_label()
        # 调用分割线函数
        self._separator_operation()
        # 载入悬浮文字
        self._load_Tooltip()
        #学生管理页面实例
        self.student_gui = operation_gui.Student_Operation(self.user_id)
        #用户信息页面实例
        self.user_information_gui = User_Information(self.win,self.user_id)
        #执行定期保持数据库连接函数
        self.win.after(0,self._threading_keep)

        self.win.iconbitmap("stbu.ico")  # 设置窗口左上角图标

    def _base_setting(self):
        self.bt_1 = ttk.Button(self.win, text="学生管理",command=self._student_oprearion,bootstyle="primary")
        self.bt_1.place(rely=0.41, width=200,height=80)

        self.bt_2 = ttk.Button(self.win, text="其他管理",bootstyle='primary')
        self.bt_2.place(rely=0.56, width=200, height=80)

        self.bt_3 = ttk.Button(self.win, text="山商要闻",command=self._open_website,bootstyle='primary')
        self.bt_3.place(rely=0.71, width=200, height=80)

        self.bt_4 = ttk.Button(self.win, text="更新日志",command=self._update_records,bootstyle='primary')
        self.bt_4.place(rely=0.86, width=200, height=80)

        # 刷新按钮
        self.update_data_photo = self._photo("./photo/update.png",40,40)
        self.update_data = ttk.Button(self.win,image=self.update_data_photo,command=self._threading_load_variable,bootstyle="success-link")
        self.update_data.place(relx=0.94,rely=0.17)

        #山商欢迎图片
        self.photo = self._welcome_photo()
        self.photo_label = tk.Label(self.win, image=self.photo, width=130, height=130).place(x=30, y=10)  # 调用欢迎山商图片

        # 判断学生管理界面是否打开的标志
        self.win.student_flag = 0
        # 调用时间函数
        self._gettime()
        # 加载变量函数
        self._threading_load_variable()

    def _separator_operation(self):  # 分隔符函数
        self.win.separator_1 = ttk.Separator(self.win, bootstyle="primary")
        self.win.separator_1.place(rely=0.4, width=200)

        self.win.separator_2 = ttk.Separator(self.win, bootstyle="primary")
        self.win.separator_2.place(rely=0.55, width=200)

        self.win.separator_3 = ttk.Separator(self.win, bootstyle="primary")
        self.win.separator_3.place(rely=0.7, width=200)

        self.win.separator_4 = ttk.Separator(self.win, bootstyle="primary")
        self.win.separator_4.place(rely=0.85, width=200)

        self.win.separator_5 = ttk.Separator(self.win, bootstyle="primary")
        self.win.separator_5.place(rely=1, width=200)

        # 垂直分割线-1
        self.win.separator_6 = ttk.Label(self.win, text="", bootstyle="inverse-info")
        self.win.separator_6.place(relx=0.17, height=600,width=10)

        self.win.separator_7 = ttk.Label(self.win, text="", bootstyle="inverse-info")
        self.win.separator_7.place(relx=0.17, rely=0.26, height=10,width=1000)

    def _welcome_photo(self):  # 左上角山商图片
        im = Image.open("./photo/welcome_sdtbu.png")
        w, h = im.size
        im = self._resize(w, h, 130, 130, im)
        photo_object = ImageTk.PhotoImage(im)
        return photo_object

    def _gettime(self):  # 动态显示当前时间
        timestr = time.strftime("%H:%M:%S")
        timestr = "当日时间为:" + timestr
        self.time_value.set(timestr)
        self.win.after(1000, self._gettime)

    def _variable_setting(self):  #变量设置
        # 用户名字
        self.user_name = tk.StringVar()
        # 时间变量
        self.time_value = tk.StringVar()
        # 用书学生数量
        self.user_populations = tk.StringVar()
        # 用户学院
        self.user_academy = tk.StringVar()
        # 用户所在专业
        self.user_academy = tk.StringVar()

    def _load_label(self):#载入label
        self.name_label_photo = self._photo("./photo/main_gui_username.png",200,50)
        self.name_label = ttk.Label(self.win,textvariable=self.user_name,bootstyle="warning", font=("微软雅黑",20),
                                    image=self.name_label_photo,compound="top")
        self.name_label.place(rely=0.25, width=200, height=90)

        # 时间显示
        self.time_label = ttk.Label(self.win, textvariable=self.time_value, bootstyle="inverse-info", font=("微软雅黑", 20))
        self.time_label.place(relx=0.4, rely=0.9, width=260, height=60)

        # 年月日显示
        self.date_time = ttk.DateEntry()
        self.date_time.configure(state="readonly")
        self.date_time.place(relx=0.85, rely=0.95)

        # 所在院系显示
        self.user_academy_photo = self._photo("./photo/main_gui_academy.png",400,70)
        self.user_academy_label = ttk.Label(self.win, textvariable=self.user_academy, bootstyle="dark",font=("小宋", 20),
                                            image=self.user_academy_photo,compound="center")
        self.user_academy_label.place(relx=0.18, rely=0.01)

        # 入籍学生数量显示
        self.user_populations_photo = self._photo("./photo/main_gui_student.png", 400,70)
        self.school_populations_label = ttk.Label(self.win, textvariable=self.user_populations, bootstyle="dark",font=("小宋", 20),
                                                  image=self.user_populations_photo,compound="center")
        self.school_populations_label.place(relx=0.18, rely=0.14)

        #用户信息【label】型按钮
        self.user_information_photo = self._photo("photo/user_information.png",50,50)
        self.user_information_label = ttk.Label(self.win,image=self.user_information_photo)
        self.user_information_label.place(relx=0.945,rely=0.01)
        self.user_information_label.bind("<Button-1>",self._user_information)#->给这个label绑定点击事件


    def _size_setting(self):#页面尺寸设置
        self.screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        self.screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        self.left = (self.screenWidth - 1200) / 2  # 获取屏幕左方大小
        self.height = (self.screenHeight - 600) / 2  # 获取屏幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (1200, 600, self.left, self.height))

    def _style_setting(self):#部件样式设置
        #按钮样式设置
        self.style_button = ttk.Style()
        self.style_button.configure('primary.TButton', font='-size 30')

    def _pymysql(self):  # 连接数据库函数
        self.pool = sql.MySQL(**config)
##########################################################################

##########################################################################
#多线程和功能部分
    def _threading_load_variable(self):#对变量导入函数进行多线程
        def th():#给变量导入数据部分
            self.sql_1 = f"SELECT name,academy FROM authme WHERE id={self.user_id}"
            self.sql_2 = "SELECT COUNT(*) FROM student_{}".format(self.user_id)

            name,academy = self.pool._execute_main(self.sql_1,method='sql_1')#获取名字，学院#获取学生数量
            population = self.pool._execute_main(self.sql_2,method='sql_2')

            #若用户还没有填写相关信息,则置为空字符串
            if name == None:
                name = ''
            if academy == None:
                academy = ''

            name = "教师:" + name
            academy = "您的学院:" + academy
            population = "在籍学生数量:" + str(population)

            self.user_name.set(name)
            self.user_academy.set(academy)
            self.user_populations.set(population)
        try:
            t = threading.Thread(target=th)
            t.start()
        except Exception as e:
            raise e

    def _threading_keep(self):#保持数据库连接存在的多线程
        def th():
            sql = "SELECT 1"
            result = self.pool._keep_connection(sql)

        #三个线程->三个连接保持
        t_1 = threading.Thread(target=th)
        t_1.start()
        t_2 = threading.Thread(target=th)
        t_2.start()
        t_3 = threading.Thread(target=th)
        t_3.start()

        #每160s执行一次简单查询
        self.win.after(160000,self._threading_keep)

    def _open_website(self):#打开浏览器官网
        #填写网址即可
        try:
            webbrowser.open("https://www.sdtbu.edu.cn/",new=1)
        except Exception:
            messagebox.showerror("失败","打开浏览器失败\n请确认电脑上安装了浏览器\n若确定安装请重新启动后重试.",parent=self.win)

    def _update_records(self):#更新历史
        try:
            os.system("start others/学籍管理系统.docx")
        except Exception:
            messagebox.showerror("失败","打开记录失败.\n重启软件后重试.",parent=self.win)
##########################################################################

##########################################################################
#页面进入和退出以及页面切换部分
    def _start(self,instance,id):#进入gui
        #进入页面设置
        self._gui_setting(id)
        #关闭加载中页面
        instance._exit()

    def _exit(self):
        self.win.destroy()
        sys.exit(0)

    def _student_oprearion(self):  # 调用学生管理页面
        # 传入加载中动画实例，方便关闭
        self.student_gui._start()

    def _user_information(self,event=None):#用户信息打开
        self.user_information_gui._start()
##########################################################################

##########################################################################
#图片载入和悬浮文字部分
    def _resize(self, w, h, w_box, h_box, pill_image):#自动调节图片大小函数
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        # 强制图片缩放后的宽度和高度比例与要放置的区域的宽度和高度比例一致
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pill_image.resize((width, height), resample=Image.LANCZOS)

    def _photo(self, path, w_box, h_box):  # 图片
        im = Image.open(path)
        w, h = im.size
        im = self._resize(w, h, w_box, h_box, im)
        photo_object = ImageTk.PhotoImage(im)
        return photo_object

    def _load_Tooltip(self):#加载图片悬浮文字
        #更新按钮文本
        self.update_data_text = "点击刷新数据."
        ToolTip(self.update_data,text=self.update_data_text)

        #学生管理文本
        self.student_text = "点击进入【学生管理页面】."
        ToolTip(self.bt_1,text=self.student_text)

        #浏览器文本
        self.website_text = "点击进入学校官网【浏览器打开】."
        ToolTip(self.bt_3,text=self.website_text)

        #更新记录文本
        self.update_record_text=  "点击打开【更新记录】."
        ToolTip(self.bt_4,text=self.update_record_text)

        #用户信息文本
        self.user_information_text = "点击打开【个人信息】."
        ToolTip(self.user_information_label,text=self.user_information_text)
##########################################################################


class User_Information:#用户信息类
    def __init__(self,win,id):
        #父类窗口
        self.original_win = win
        #用户id
        self.user_id = id
        #创建连接池实例
        self.pool = sql.MySQL()

##########################################################################
#页面设置部分
    def _gui_setting(self):#页面设置
        self.win = ttk.Toplevel(self.original_win)
        self.win.title("用户信息")
        self.win.resizable(False, False)
        #页面尺寸设置
        self._size_setting()
        #样式设置
        self._style_setting()
        #变量设置
        self._variable_setting()
        #基本设置
        self._base_setting()

        self.win.iconbitmap("stbu.ico")  # 设置窗口左上角图标

    def _size_setting(self):#页面尺寸设置
        self.screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        self.screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        self.left = (self.screenWidth - 600) / 2  # 获取屏幕左方大小
        self.height = (self.screenHeight - 600) / 2  # 获取屏幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (600, 600, self.left, self.height))

    def _style_setting(self):#样式设置
        self.style = ttk.Style()
        self.style.configure("TRadiobutton",font=("微软雅黑",13))
        self.style.configure("Outline.TButton",font=("微软雅黑",20))

    def _variable_setting(self):#变量设置
        #姓名
        self.user_name = tk.StringVar()

        #学院
        self.user_academy = tk.StringVar()

        #手机号
        self.user_phone_number = tk.StringVar()

        #教师号
        self.user_teacher_number = tk.StringVar()

        #性别
        self.user_gender = tk.StringVar()

        #变量副本
        self.vv_name = None
        self.vv_academy = None
        self.vv_phone = None
        self.vv_number = None
        self.vv_gender = None

        #多线程给变量赋值
        self._threading(method='sql_read')

    def _base_setting(self):#基本设置
        #用户姓名
        self.user_name_photo = self._photo("photo/user_name.png",50,50)
        self.user_name_photo_label = ttk.Label(self.win,image=self.user_name_photo)
        self.user_name_photo_label.place(relx=0.05,rely=0.1)

        self.user_name_label = ttk.Label(self.win,text="姓名:",foreground="blue",font=("微软雅黑",25))
        self.user_name_label.place(relx=0.15,rely=0.1)

        self.user_name_entry = ttk.Entry(self.win,textvariable=self.user_name,font=("微软雅黑",15),
                                         state="readonly",foreground='purple')
        self.user_name_entry.place(relx=0.3,rely=0.11)

        self.user_name_button = ttk.Button(self.win,text="修改",style="outline-success",command=self._name_button)
        self.user_name_button.place(relx=0.8,rely=0.1)

        #用户学院
        self.user_academy_photo = self._photo("photo/user_academy.png",50,50)
        self.user_academy_photo_label = ttk.Label(self.win,image=self.user_academy_photo)
        self.user_academy_photo_label.place(relx=0.05,rely=0.25)

        self.user_academy_label = ttk.Label(self.win,text="学院:",foreground="blue",font=("微软雅黑",25))
        self.user_academy_label.place(relx=0.15,rely=0.25)

        self.user_academy_entry = ttk.Entry(self.win,textvariable=self.user_academy,font=("微软雅黑",15),
                                            state="readonly",foreground='purple')
        self.user_academy_entry.place(relx=0.3,rely=0.26)

        self.user_academy_button = ttk.Button(self.win,text="修改",bootstyle="outline-success",command=self._academy_button)
        self.user_academy_button.place(relx=0.8,rely=0.25)

        #用户手机号
        self.user_phone_number_photo = self._photo("photo/user_phone_number.png",50,50)
        self.user_phone_number_photo_label = ttk.Label(self.win,image=self.user_phone_number_photo)
        self.user_phone_number_photo_label.place(relx=0.05,rely=0.4)

        self.user_phone_number_label = ttk.Label(self.win,text="手机:",foreground="blue",font=("微软雅黑",25))
        self.user_phone_number_label.place(relx=0.15,rely=0.4)

        self.user_phone_number_entry = ttk.Entry(self.win,textvariable=self.user_phone_number,font=("微软雅黑",15),
                                                 state="readonly",foreground='purple')
        self.user_phone_number_entry.place(relx=0.3,rely=0.41)

        self.user_phone_number_button = ttk.Button(self.win,text="修改",bootstyle="outline-success",command=self._phone_button)
        self.user_phone_number_button.place(relx=0.8,rely=0.4)

        #用户教师号
        self.user_teacher_number_photo = self._photo("photo/user_sno.png",50,50)
        self.user_teacher_number_photo_label = ttk.Label(self.win,image=self.user_teacher_number_photo)
        self.user_teacher_number_photo_label.place(relx=0.05,rely=0.55)

        self.user_teacher_number_label = ttk.Label(self.win,text="教号:",foreground="blue",font=("微软雅黑",25))
        self.user_teacher_number_label.place(relx=0.15,rely=0.55)

        self.user_teacher_number_entry = ttk.Entry(self.win,textvariable=self.user_teacher_number,font=("微软雅黑",15),
                                                   state="readonly",foreground='purple')
        self.user_teacher_number_entry.place(relx=0.3,rely=0.56)

        self.user_teacher_number_button = ttk.Button(self.win,text="修改",bootstyle="outline-success",command=self._sno_button)
        self.user_teacher_number_button.place(relx=0.8,rely=0.55)

        #性别按钮
        self.user_gender_male_photo = self._photo("photo/male.png",100,100)
        self.user_gender_female_photo = self._photo("photo/female.png",100,100)
        self.user_gender_photo_label = ttk.Label(self.win)
        self.user_gender_photo_label.place(relx=0.78,rely=0.7)

        self.user_gender_label = ttk.Label(self.win,text="性别:",foreground='red',font=("微软雅黑",20))
        self.user_gender_label.place(relx=0.05,rely=0.7)

        self.user_gender_male_button = ttk.Radiobutton(self.win,text='男',value='男',variable=self.user_gender,command=self._switch_male)
        self.user_gender_male_button.place(relx=0.2,rely=0.72)

        self.user_gender_female_button = ttk.Radiobutton(self.win,text='女',value='女',variable=self.user_gender,command=self._switch_female)
        self.user_gender_female_button.place(relx=0.3,rely=0.72)

        #保存按钮
        self.saving_button = ttk.Button(self.win,text="保存",bootstyle="outline-danger",command=self._saving_button)
        self.saving_button.place(relx=0.4,rely=0.9)
##########################################################################

##########################################################################
 #功能函数部分
    def _name_button(self):#姓名按钮
        #将输入框设置为可写入
        self.user_name_entry.configure(state="normal")

    def _academy_button(self):#学院按钮
        self.user_academy_entry.configure(state="normal")

    def _phone_button(self):#电话按钮
        self.user_phone_number_entry.configure(state="normal")

    def _sno_button(self):#教师号按钮
        self.user_teacher_number_entry.configure(state="normal")

    def _saving_button(self):#保存按钮
        if (self.vv_name,self.vv_academy,self.vv_phone,self.vv_number,self.vv_gender) == (self.user_name.get(),self.user_academy.get(),
                                                                           self.user_phone_number.get(),self.user_teacher_number.get(),
                                                                            self.user_gender.get()):
            messagebox.showwarning("未修改","你都没有修改过任何数据.\n请修改后再尝试.")
            return
        self.temporary = (self.user_name.get(),self.user_academy.get(),self.user_phone_number.get(),
                          self.user_teacher_number.get(),self.user_gender.get())
        #多线程写
        self._threading(method='sql_write')

    def _identify_gender(self):#初始化页面判断性别，给出图片
        if self.user_gender.get() == '男':
            self.user_gender_photo_label.config(image=self.user_gender_male_photo)
        elif self.user_gender.get() == '女':
            self.user_gender_photo_label.config(image=self.user_gender_female_photo)

    def _switch_male(self):#照片换为男
        self.user_gender_photo_label.config(image=self.user_gender_male_photo)

    def _switch_female(self):#照片换为女
        self.user_gender_photo_label.config(image=self.user_gender_female_photo)
##########################################################################

##########################################################################
#多线程部分->数据库操作
    def _threading(self,method=None,ele=None):#多线程函数
        def th_read():#读
            sql = f"SELECT name,academy,number,sno,gender FROM authme WHERE id={self.user_id}"
            result = self.pool._execute_user(sql,method='sql_read')
            #给变量赋值
            self.user_name.set(result[0])
            self.user_academy.set(result[1])
            self.user_phone_number.set(result[2])
            self.user_teacher_number.set(result[3])
            self.user_gender.set(result[4])

            #给副本变量赋值
            self.vv_name = result[0]
            self.vv_academy = result[1]
            self.vv_phone = result[2]
            self.vv_number = result[3]
            self.vv_gender = result[4]

            # 判断性别
            self._identify_gender()

        def th_write():#写
            sql = f"UPDATE authme SET name=%s,academy=%s,number=%s,sno=%s,gender=%s WHERE id={self.user_id}"
            self.pool._execute_user(sql,method='sql_write',elements=self.temporary)

        try:
            if method == 'sql_read':
                t = threading.Thread(target=th_read)
                t.start()
            elif method == 'sql_write':
                t= threading.Thread(target=th_write)
                t.start()
        except Exception as e:
            messagebox.showerror("错误","请检查网络后重试.",parent=self.win)
            raise e

##########################################################################

##########################################################################
# 图片载入和悬浮文字部分
    def _resize(self, w, h, w_box, h_box, pill_image):  # 自动调节图片大小函数
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        # 强制图片缩放后的宽度和高度比例与要放置的区域的宽度和高度比例一致
        factor = min([f1, f2])
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
#页面进入和退出以及页面切换部分
    def _start(self):#进入gui
        #进入页面设置
        self._gui_setting()

    def _exit(self):
        self.win.destroy()
##########################################################################