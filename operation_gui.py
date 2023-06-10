import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import ttk as tttk
from ttkbootstrap.tooltip import ToolTip
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import threading
import queue
import sql
from users_student import Gui_student
from excel_gui import Excel_Gui


class Student_Operation:#主页面类
    def __init__(self,id):
        # flag判断当前页面是否打开(1->已打开,0->未打开)
        self.flag = 0
        #用户的id->区分用户的唯一标识
        self.user_id = id

#####################################################################################
# 页面基本设置部分
    def _first_base(self):
        self.pool = sql.MySQL()
        self.win = ttk.Toplevel()
        self.win.title("学籍管理系统V2.0")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)#设置关闭该页面执行的操作
        #页面设置
        self._base_setting()
        #部件样式设置
        self._style_setting()
        #分割线
        self._separator()
        #加载图片
        self._load_photo()
        #悬浮文字
        self._text_load()
        #学生信息页面实例
        self.student_instance = Gui_student(self.win,self,self.user_id)
        #属性管理页面实例
        self.arrtibute_instance = Manage_Attribute(self.win,self,self.user_id)
        #excel页面实例
        self.excel_instance = Excel_Gui(self,self.win,self.user_id)
        # 设置窗口左上角图标
        self.win.iconbitmap("stbu.ico")

    def _base_setting(self):
        self.screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        self.screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        self.left = (self.screenWidth - 1000) / 2  # 获取屏幕左方大小
        self.height = (self.screenHeight - 700) / 2  # 获取屏幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (1000, 700, self.left, self.height))

        #定义三查询输入框中的变量
        self.v_sno = tk.StringVar()
        self.v_name = tk.StringVar()
        self.v_num = tk.StringVar()
        self.query_result_list = []

        self.button_1 = ttk.Button(self.win,text="添加学生",bootstyle="success",command=self._student_gui)
        self.button_1.place(relx=0.01,rely=0.22,width=130,height=60)

        self.button_2 = ttk.Button(self.win, text="修改学生", bootstyle="success",command=self._modify_student)
        self.button_2.place(relx=0.01, rely=0.32, width=130,height=60)

        self.button_3 = ttk.Button(self.win, text="删除学生", bootstyle="success",command=self._delete_student)
        self.button_3.place(relx=0.01, rely=0.42, width=130,height=60)

        self.button_4 = ttk.Button(self.win,text="属性管理",bootstyle="danger",command=self._attribute_gui)
        self.button_4.place(relx=0.01,rely=0.52,width=130,height=60)

        self.button_5 = ttk.Button(self.win,text="批量处理",bootstyle="danger",command=self._excel_gui)
        self.button_5.place(relx=0.01,rely=0.72,width=130,height=60)

        self.right_frame = tk.LabelFrame(self.win,font=("微软雅黑",12),text="学生信息查询",width=830,height=70)
        self.right_frame.place(relx=0.16,rely=0.21)

        self.label_sno = ttk.Label(self.win,text="学号:",font=("微软雅黑",13))
        self.label_sno.place(relx=0.17,rely=0.25)

        self.entry_sno = tk.Entry(self.win,font="13",textvariable=self.v_sno)
        self.entry_sno.place(relx=0.22,rely=0.25,width=100,height=25)

        self.label_name = ttk.Label(self.win, text="姓名:", font=("微软雅黑", 13))
        self.label_name.place(relx=0.33, rely=0.25)

        self.entry_name = tk.Entry(self.win,font="13",textvariable=self.v_name)
        self.entry_name.place(relx=0.38, rely=0.25, width=100, height=25)

        self.label_num = ttk.Label(self.win, text="手机号:", font=("微软雅黑", 13))
        self.label_num.place(relx=0.49, rely=0.25)

        self.entry_num = tk.Entry(self.win, font="13",textvariable=self.v_num)
        self.entry_num.place(relx=0.56, rely=0.25, width=100, height=25)

        self.button_inquiry = ttk.Button(self.win,bootstyle="dark",text="查询",command=self._query_data)
        self.button_inquiry.place(relx=0.7,rely=0.24,width=80,height=40)

        self.button_inquiry_all = ttk.Button(self.win,bootstyle="dark",text="显示全部学生",command=self._reload_data)
        self.button_inquiry_all.place(relx=0.79,rely=0.24,width=140,height=40)

        #####################################
        # 树状表:
        #获取用户的所有Treeview的列:
        self.columns = self._initialize_heading()
        #获取用户的树状表数据:
        self.data = self._initialize_data(flag='main')        #->注意与上面的self.columns的先后顺序不能变！！！！
        #树状表基本设置函数:
        self._treeview()
        #添加鼠标点击事件->打开具体的学生信息
        self.tree_view.bind("<Double-1>",self._on_click)
        #树状表滚动条函数,->给树状图添加滚动条
        self._scoalled()
        #载入树状表数据
        self._load_data(self.data)
        #####################################

    def _separator(self):
        self._sp_1 = ttk.Label(self.win,bootstyle="inverse-primary")
        self._sp_1.place(rely=0.205,width=1000,height=5)

        self._sp_2 = ttk.Label(self.win,bootstyle="inverse-primary")
        self._sp_2.place(relx=0.15,rely=0.2,width=5,height=560)

    def _style_setting(self):
        #按钮样式设置
        self.style_button = ttk.Style()
        self.style_button.configure('danger.TButton',font=("微软雅黑",15),foreground="black")#设置按钮字体大小
        self.style_button.configure('success.TButton', font=("微软雅黑",15),foreground="black")
        self.style_button.configure('dark.TButton', font=("微软雅黑", 13), foreground="white")
        #Treeview样式设置
        self.style_value = tttk.Style()
        self.style_value.configure("Treeview", rowheight=25, font=("微软雅黑", 15))
        self.style_heading = tttk.Style()
        self.style_heading.configure("Treeview.Heading", font=("微软雅黑", 15))
#####################################################################################

#####################################################################################
#具体部件实现部分
    def _scoalled(self):#滚动条函数
        #将滚动条添加到当前Treeview
        self.y_bar.config(command=self.tree_view.yview)
        self.x_bar.config(command=self.tree_view.xview)

    def _treeview(self):#树状表
        #垂直和水平滚动条
        #给Treeview添加滚动条
        self.y_bar = tk.Scrollbar(self.win,orient="vertical")
        self.y_bar.place(relx=0.965,rely=0.33,height=440)

        self.x_bar = tk.Scrollbar(self.win,orient="horizontal")
        self.x_bar.place(relx=0.16,rely=0.97,width=800,height=20)

        ################################################################################
        # 设置框架中的表格:[基本的六种属性]->sno,name,gender,subject,num,home.
        #使用的是ttkinter中的treeview，ttkbootstrap中的treeview因为某方面的原因有BUG
        self.tree_view = tttk.Treeview(self.win,style="Custom.Treeview",
                                       columns=self.columns,
                                       show="headings",
                                       height=16,
                                       yscrollcommand=self.y_bar.set,
                                       xscrollcommand=self.x_bar.set)

        self.tree_view.column("sno", width=120, anchor="center")
        self.tree_view.column("name", width=100, anchor="center")
        self.tree_view.column("gender", width=100, anchor="center")
        self.tree_view.column("subject", width=120, anchor="center")
        self.tree_view.column("num", width=120, anchor="center")
        self.tree_view.column("home", width=220, anchor="center")

        self.tree_view.heading("sno",text="学号")
        self.tree_view.heading("name", text="姓名")
        self.tree_view.heading("gender", text="性别")
        self.tree_view.heading("subject", text="专业")
        self.tree_view.heading("num", text="手机号")
        self.tree_view.heading("home", text="家庭住址")

        ###############################################################################
        # 初始化用户自定义添加的列:
        fixed_result = ['sno','name','gender','subject','num','home']
        #筛选出除了[sno,name,gender,subject,num,home]的列->即用户自己添加的列
        self.heading_user = [item for item in self.columns if item not in fixed_result]
        #遍历添加用户自定义列.
        if len(self.heading_user) != 0:
            for value in self.heading_user:
                self.tree_view.column(value, width=200, anchor="center")
                self.tree_view.heading(value, text=value)

        self.tree_view.place(relx=0.16,rely=0.33,width=800)

    def _initialize_heading(self):#初始化用户Treeview中的列
        #查询用户所有的列.
        sql_heading = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'student_{}'".format(self.user_id)
        #储存用户所有的列.
        self.heading_result = self._threading(sql_heading,method='sql_heading')
        #将存储用户的列的格式转换为列表
        self.heading_result = [item[0] for item in self.heading_result]
        #固定需要删除的元素id
        fixed_result = ['id']
        #筛选出除数据库中-[id]-的列.
        self.heading_result = [item for item in self.heading_result if item not in fixed_result]

        return self.heading_result

    def _initialize_data(self,flag=None):#初始化第一次页面数据
        #查询用户数据
        sql_1 = "SELECT {} FROM student_{}".format(",".join(self.columns),self.user_id)
        data = self._threading(sql_1,method='sql_1',flag=flag)
        return data

    def _load_data(self, current_list):  # 显示数据函数
        for i in current_list:
            self.tree_view.insert('', "end", values=i)

    def _query_data(self):#数据查询
        query_condition_1 = self.v_sno.get()
        query_condition_2 = self.v_name.get()
        query_condition_3 = self.v_num.get()

        # 清空已经查询的数据列表->【self.query_result_list】
        self.query_result_list.clear()
        #清空树状表中显示的数据.
        self._delete_data()

        for item in self.data:
            if query_condition_1 in item[0] and query_condition_2 in item[1] and query_condition_3 in item[4]:
                self.query_result_list.append(item)
        #载入数据
        self._load_data(self.query_result_list)

    def _reload_data(self):#给树状图载入全部的数据,->用于查询结束后的显示全部数据
        #先清空树状图中的数据
        self._delete_data()
        #重新给树状图加载数据
        self._load_data(self.data)

    def _update_data(self):#刷新treeview数据->用于经过数据库【增删改查】后。
        #先清空树状图中的数据
        self._delete_data()
        #重新从数据库中读取数据
        self.data = self._initialize_data()
        # 重新给树状图加载数据
        self._load_data(self.data)

    def _delete_data(self):#清空树状表显示的数据
        for i in self.tree_view.get_children():
            self.tree_view.delete(i)

    def _delete_student(self):#删除一个具体的学生数据
        selects = self.tree_view.selection()
        if not selects:
            tk.messagebox.showerror("错误", "您还没有选择一个或多个数据哦", parent=self.win)
        else:
            flag = tk.messagebox.askyesno("删除操作", "确定要删除选中的数据吗？", parent=self.win)
            if flag == True:
                #删除的为id=[]->的记录
                sql_2 = "DELETE FROM student_{} WHERE sno=%s".format(self.user_id)
                #selects是一个包含了多个id的元组，可以用ctrl选中多个学生批量删除.
                #利用for循环遍历删除多个学生数据.
                for s in selects:
                    item = self.tree_view.set(s)
                    #多线程执行删除学生数据.
                    self._threading(sql_2,elements=item['sno'],method='sql_2')
                #重新从数据库中加载数据
                self.data = self._initialize_data()
                #重新给树状图添加数据
                self._reload_data()
                tk.messagebox.showinfo("成功","成功删除数据!",parent=self.win)
            else:
                tk.messagebox.showinfo("失败", "没有数据被删除!",parent=self.win)

    def _modify_student(self):#修改学生
        try:
            select = self.tree_view.selection()[0]
        except Exception:
            tk.messagebox.showwarning("警告","你都没有选择一个数据，你要修改啥？",parent=self.win)
        else:
            list = self.tree_view.item(select,'values')
            self.student_instance._start(llist=self.heading_user,list=list)

    def _on_click(self,event):#点击数据打开页面函数
        # 修改学生函数
        self._modify_student()

    def _update_treeview(self):#用于更新Treeview
        #获取用户的所有Treeview的列:
        self.columns = self._initialize_heading()
        #获取用户的树状表数据:
        self.data = self._initialize_data(flag='main')
        #加载树状图
        self._treeview()
        #加载滚动条
        self._scoalled()
        #载入树状表数据
        self._load_data(self.data)
        #重新添加鼠标点击事件->打开具体的学生信息
        self.tree_view.bind("<Double-1>",self._on_click)
#####################################################################################

#####################################################################################
#多线程操作部分->数据库操作
    def _threading(self,sql,elements=None,method=None,flag=None):#多线程函数(数据库操作)
        def th_sql_1(sql_1):#sql_1函数
            reponse2 = self.pool._execute_operation_gui(sql_1,method='sql_1')
            q.put(reponse2)

        def th_sql_2(sql_2,elements):#sql_2函数
            self.pool._execute_operation_gui(sql_2,elements,method='sql_2')

        def th_sql_heading(sql_flag):#sql_flag函数，负责查询Treeview有几列
            heading = self.pool._execute_operation_gui(sql_flag,method='sql_heading')
            q.put(heading)

        q = queue.Queue()

        try:
            if method == 'sql_1':
                t = threading.Thread(target=th_sql_1,args=(sql,))
                t.start()
                # 100次循环每次循环0.1秒，最大总计10秒的判断总时间
                for i in range(100):
                    time.sleep(0.1)
                    if not q.empty():
                        return q.get()
                else:
                    pass
            elif method == 'sql_2':
                t = threading.Thread(target=th_sql_2,args=(sql,elements))
                t.start()
                # 休眠0.5毫秒以便t线程运行结束
                time.sleep(0.5)
            elif method == 'sql_heading':
                t = threading.Thread(target=th_sql_heading,args=(sql,))
                t.start()
                # 100次循环每次循环0.1秒，最大总计10秒的判断总时间
                for i in range(100):
                    time.sleep(0.1)
                    if not q.empty():
                        return q.get()
                else:
                    pass
        except Exception as e:
            raise e

#####################################################################################

#####################################################################################
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

    def _load_photo(self):#加载所有图片按钮
        self.tip = self._photo("photo/wenhao.png",40,40)#提示
        self.tip_label = ttk.Label(self.win,image=self.tip)
        self.tip_label.place(relx=0.935,rely=0.238)

        self.scenery = self._photo("photo/scenery.png", 1000,140)#顶层
        self.scenery_label = ttk.Label(self.win, image=self.scenery)
        self.scenery_label.place(x=0, y=0)

        self.update = self._photo("photo/update.png",40,40)#刷新
        self.update_button = ttk.Button(self.win,image=self.update,bootstyle="warning-link",command=self._update_gui)
        self.update_button.place(relx=0,rely=0.93)

    def _text_load(self):  # 鼠标移动到固定组件时显示文字
        self.text_tip = """支持模糊查询，也支持多信息查询
即:可以输入学号的一部分，或者同时输入学号和姓名
进行查询。"""
        ToolTip(self.tip_label, text=self.text_tip)
        self.text_update = """点击刷新页面"""
        ToolTip(self.update_button, text=self.text_update)
#####################################################################################

#####################################################################################
#页面跳转与关闭部分->该页面和其它页面
    def _student_gui(self):#具体某个学生的界面
        #llist=self.heading_user->用户自定义属性
        self.student_instance._start(llist=self.heading_user)

    def _attribute_gui(self):#属性管理页面
        #传入用户自定义添加的属性列表->self.heading_user
        self.arrtibute_instance._start(self.heading_user)

    def _excel_gui(self):#excel页面
        self.excel_instance._start()

    def _start(self):#窗体进入
        if self.flag == 0:
            self.flag = 1
            self._first_base()
        else:
            tk.messagebox.showwarning("重复打开", "您已经打开这个页面了请不要重复打开！")

    def _update_gui(self):#刷新页面
        self.win.update()

    def _exit(self):#杀死该页面，并且恢复该页面的创建
        self.flag = 0
        self.win.destroy()
#####################################################################################



class Manage_Attribute:#用户自定义添加学生属性
    def __init__(self,win,instance,id):
        #父页面窗体
        self.original_gui = win
        #父页面实例
        self.original_instance = instance
        self.pool = sql.MySQL()
        #用户id->标志哪一个用户
        self.id = id
        #判断用户是否操作过的标志
        self.flag = False
#####################################################################################
#页面基本设置部分
    def _gui_setting(self,list):#页面设置
        self.win = ttk.Toplevel(self.original_gui)
        self.win.title("属性管理")
        self.win.resizable(False, False)
        #关闭页面执行的操作
        self.win.protocol("WM_DELETE_WINDOW",self._exit)

        self.screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        self.screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        self.left = (self.screenWidth - 600) / 2  # 获取屏幕左方大小
        self.height = (self.screenHeight - 600) / 2  # 获取屏幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (600, 600, self.left, self.height))

        #样式设置
        self._style_setting()
        #给变量传值
        self._variable_setting(*list)
        #基本设置
        self._base_setting()
        # 设置窗口左上角图标
        self.win.iconbitmap("stbu.ico")

    def _variable_setting(self,n1='',n2='',n3='',n4='',n5=''):#变量设置
        self.v_attribute_1 = tk.StringVar()
        self.v_attribute_2 = tk.StringVar()
        self.v_attribute_3 = tk.StringVar()
        self.v_attribute_4 = tk.StringVar()
        self.v_attribute_5 = tk.StringVar()

        self.v_attribute_1.set(n1)
        self.v_attribute_2.set(n2)
        self.v_attribute_3.set(n3)
        self.v_attribute_4.set(n4)
        self.v_attribute_5.set(n5)

        #添加属性的变量
        self.v_add = tk.StringVar()

        #属性列表
        self.list = [self.v_attribute_1,self.v_attribute_2,self.v_attribute_3,self.v_attribute_4,self.v_attribute_5]

        #用户添加的属性数量
        self.number = tk.IntVar()
        #计算用户已添加属性数量
        self._for_attribute_number()

    def _base_setting(self):#页面基本设置
        #五个属性
        self.attribute_1_label = ttk.Label(self.win,font=("微软雅黑",20),text="属性[1]:",foreground="blue")
        self.attribute_1_label.place(relx=0.05,rely=0.1)

        self.attribute_2_label = ttk.Label(self.win,font=("微软雅黑",20),text="属性[2]:",foreground="blue")
        self.attribute_2_label.place(relx=0.05,rely=0.25)

        self.attribute_3_label = ttk.Label(self.win,font=("微软雅黑",20),text="属性[3]:",foreground="blue")
        self.attribute_3_label.place(relx=0.05,rely=0.4)

        self.attribute_4_label = ttk.Label(self.win,font=("微软雅黑",20),text="属性[4]:",foreground="blue")
        self.attribute_4_label.place(relx=0.05,rely=0.55)

        self.attribute_5_label = ttk.Label(self.win,font=("微软雅黑",20),text="属性[5]:",foreground="blue")
        self.attribute_5_label.place(relx=0.05,rely=0.7)

        #添加属性
        self.add_label = ttk.Label(self.win,font=("微软雅黑",20),text="添加属性:",foreground="purple")
        self.add_label.place(relx=0.02,rely=0.85)

        #不为空属性数量
        self.number_label_front = ttk.Label(self.win,font=("微软雅黑",15),text="已添加属性数量:",foreground="purple")
        self.number_label_front.place(relx=0.2,rely=0.02)

        self.number_label_behind = ttk.Label(self.win,font=("微软雅黑",15),textvariable=self.number,foreground="red")
        self.number_label_behind.place(relx=0.45,rely=0.02)

        #输入框
        self.attribute_1_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.v_attribute_1,foreground="green",state='disabled')
        self.attribute_1_entry.place(relx=0.25,rely=0.1)

        self.attribute_2_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.v_attribute_2,foreground="green",state='disabled')
        self.attribute_2_entry.place(relx=0.25,rely=0.25)

        self.attribute_3_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.v_attribute_3,foreground="green",state='disabled')
        self.attribute_3_entry.place(relx=0.25,rely=0.4)

        self.attribute_4_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.v_attribute_4,foreground="green",state='disabled')
        self.attribute_4_entry.place(relx=0.25,rely=0.55)

        self.attribute_5_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.v_attribute_5,foreground="green",state='disabled')
        self.attribute_5_entry.place(relx=0.25,rely=0.7)

        self.add_entry = ttk.Entry(self.win,font=("微软雅黑",20),textvariable=self.v_add,foreground="black")
        self.add_entry.place(relx=0.25,rely=0.85)

        #按钮
        self.attribute_1_button = ttk.Button(self.win,text="删除",bootstyle="outline_primary",command=lambda :self._index_delete('delete_1'))
        self.attribute_1_button.place(relx=0.85,rely=0.1)

        self.attribute_2_button = ttk.Button(self.win,text="删除",bootstyle="outline_primary",command=lambda :self._index_delete('delete_2'))
        self.attribute_2_button.place(relx=0.85,rely=0.25)

        self.attribute_3_button = ttk.Button(self.win,text="删除",bootstyle="outline_primary",command=lambda :self._index_delete('delete_3'))
        self.attribute_3_button.place(relx=0.85,rely=0.4)

        self.attribute_4_button = ttk.Button(self.win,text="删除",bootstyle="outline_primary",command=lambda :self._index_delete('delete_4'))
        self.attribute_4_button.place(relx=0.85,rely=0.55)

        self.attribute_5_button = ttk.Button(self.win,text="删除",bootstyle="outline_primary",command=lambda :self._index_delete('delete_5'))
        self.attribute_5_button.place(relx=0.85,rely=0.7)

        self.add_button = ttk.Button(self.win,text="添加",bootstyle="outline_success",command=self._add_funcition)
        self.add_button.place(relx=0.85,rely=0.85)

    def _style_setting(self):#样式设置
        #按钮样式设置
        self.confirm_button_style = ttk.Style()
        self.confirm_button_style.configure("TButton",font=("微软雅黑",20))
#####################################################################################

#####################################################################################
#功能部分
    def _add_funcition(self):#添加属性函数
        #存储添加属性变量的值
        vv = self.v_add.get()
        #判断添加属性变量的值是否为空
        if vv == '':
            messagebox.showerror("属性为空","你尚未输入任何数据.",parent=self.win)
            return
        if 0 <= self.number.get() < 5:
            #遍历寻找不为空的元素
            for item in self.list:
                if item.get() == '':
                    v = item
                    break
            #将flag标志变为True->表示用户进行过操作
            self.flag = True
            #将该元素的值赋值为输入的值
            v.set(vv)
            #调用数据库函数将属性添加到数据库中
            self._add_sql(vv)
            #清空输入框
            self.add_entry.delete(0,"end")
            #重新计算用户已添加属性数量
            self._for_attribute_number()
        else:
            messagebox.showerror("属性已满","你已经添加了五个属性了，不能再继续添加了",parent=self.win)

    def _index_delete(self,name):#删除函数索引->用来标记删除的是第几个属性
        #判断哪一个按钮的删除
        if name == 'delete_1':
            self._delete_function(self.v_attribute_1)
        elif name == 'delete_2':
            self._delete_function(self.v_attribute_2)
        elif name == 'delete_3':
            self._delete_function(self.v_attribute_3)
        elif name == 'delete_4':
            self._delete_function(self.v_attribute_4)
        elif name == 'delete_5':
            self._delete_function(self.v_attribute_5)

    def _delete_function(self,v):#删除属性函数
        #先判断需要删除的这一个属性是否为空
        if v.get() == '':
            messagebox.showerror("删除失败","该属性本来就是空的，你删什么呢？",parent=self.win)
            return
        flag = messagebox.askyesno("警告","是否要删除该属性?\n一旦删除，将无法恢复!\n请谨慎删除!",parent=self.win,icon='warning')
        if flag == True:
            #将flag标志变为True->表示用户进行过操作
            self.flag = True
            #删除数据库中的该属性
            self._delete_sql(v.get())
            #将该属性的StringVar设置为空字符串
            v.set('')
            #重新计算已添加属性数量
            self._for_attribute_number()

    def _delete_sql(self,vv):#数据库操作->删除属性
        sql = f"ALTER TABLE student_{self.id} DROP COLUMN {vv}"
        self.pool._execute_attribute(sql,method='delete')

    def _add_sql(self,vv):#数据库操作->添加属性
        sql = f"ALTER TABLE student_{self.id} ADD {vv} varchar(255) DEFAULT ''"
        self.pool._execute_attribute(sql,method='add')

    def _for_attribute_number(self):#遍历计算当前用户添加的属性数量
        #初始化为0
        self.number.set(0)
        #遍历不为空的属性数量
        for item in self.list:
            if item.get() != '':
                current_value = self.number.get()  # 获取当前值
                self.number.set(current_value + 1)  # 递增并存回
#####################################################################################

#####################################################################################
#页面退出和进入
    def _start(self,list):#页面进入
        # 令学生页面不能操作
        self.original_gui.attributes("-disabled",1)
        #开始部署页面->list是用户自定义添加的属性
        self._gui_setting(list)

    def _exit(self):#页面关闭
        # 令学生页面可以操作
        self.original_gui.attributes("-disabled",0)
        #检查用户是否进行过操作,若没有则不需要对Treeview进行更新
        if self.flag == True:
            #重新将flag标志变为False
            self.flag = False
            #更新树状图
            self.original_instance._update_treeview()
        self.win.destroy()
#####################################################################################