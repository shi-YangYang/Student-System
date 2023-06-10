import time
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import sql
import threading
import queue

class Gui_student:#学生详细信息页面
    def __init__(self,win_main,student_operation,id):
        #父页面窗体
        self.win_main = win_main
        #父页面实例
        self.student_operation = student_operation
        #创建一个连接池实例
        self.pool = sql.MySQL()
        #用户id
        self.user_id = id
#####################################################################################
#页面基本设置部分
    def _gui_base(self):
        self.win = tk.Toplevel(self.win_main)
        self.win.title("学生修改&&添加")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        #部件样式设置
        self._style_setting()
        #基本设置
        self._base_setting()
        #悬浮文字设置
        self._tooltip()
        # 设置窗口左上角图标
        self.win.iconbitmap("stbu.ico")

    def _base_setting(self):
        self.win.protocol("WM_DELETE_WINDOW",self._exit)
        self.screenWidth = self.win.winfo_screenwidth()  # 获取显示区域宽度
        self.screenHeight = self.win.winfo_screenheight()  # 获取显示区域高度
        self.left = (self.screenWidth - 800) / 2  # 获取屏幕左方大小
        self.height = (self.screenHeight - 600) / 2  # 获取屏幕上方大小
        self.win.geometry('%dx%d+%d+%d' % (800, 500, self.left, self.height))

        self.sno_label = ttk.Label(self.win,bootstyle="dark",text="学号:",font=("微软雅黑",13))
        self.sno_label.place(relx=0.06,rely=0)

        self.name_label = ttk.Label(self.win,bootstyle="dark",text="姓名:",font=("微软雅黑",13))
        self.name_label.place(relx=0.06,rely=0.1)

        self.subject_label = ttk.Label(self.win, bootstyle="dark", text="专业:",font=("微软雅黑",13))
        self.subject_label.place(relx=0.06, rely=0.2)

        self.num_label = ttk.Label(self.win, bootstyle="dark", text="手机号:",font=("微软雅黑",13))
        self.num_label.place(relx=0.04, rely=0.3)

        self.home_label = ttk.Label(self.win, bootstyle="dark", text="家庭住址:",font=("微软雅黑",13))
        self.home_label.place(relx=0.02, rely=0.4)

        self.gender_label = ttk.Label(self.win, bootstyle="dark", text="性别:", font=("微软雅黑", 13))
        self.gender_label.place(relx=0.66,rely=0.2)

        self.sno_entry = tk.Entry(self.win,textvariable=self.v_sno,font=("微软雅黑",13))
        self.sno_entry.place(relx=0.2,rely=0)

        self.name_entry = tk.Entry(self.win,textvariable=self.v_name,font=("微软雅黑",13))
        self.name_entry.place(relx=0.2, rely=0.1)

        self.subject_entry = tk.Entry(self.win, textvariable=self.v_subject,font=("微软雅黑",13))
        self.subject_entry.place(relx=0.2, rely=0.2)

        self.num_entry = tk.Entry(self.win, textvariable=self.v_num,font=("微软雅黑",13))
        self.num_entry.place(relx=0.2, rely=0.3)

        self.home_entry = tk.Entry(self.win, textvariable=self.v_home,font=("微软雅黑",13))
        self.home_entry.place(relx=0.2, rely=0.4)

        self.gender_button_female = ttk.Radiobutton(self.win,text="女",value="女",variable=self.v_gender,bootstyle="primary")
        self.gender_button_female.place(relx=0.81,rely=0.2)

        self.gender_button_male = ttk.Radiobutton(self.win,text="男",value="男", variable=self.v_gender,bootstyle="primary")
        self.gender_button_male.place(relx=0.73, rely=0.2)

        self.confirm_photo = self._photo("photo/confirm.png",100,100)
        self.confirm_button = ttk.Button(self.win,image=self.confirm_photo,command=self._check_information,bootstyle='link-success')
        self.confirm_button.place(relx=0.7,rely=0.35)

        #若用户自定义属性个数不为0，则动态添加按钮，标签，输入框等部件.
        if self.number != 0:
            for i in range(self.number):
                self._dynamic_add_widget(i)

    def _variable_setting(self,sno="",name="",gender="",subject="",num="",home="",n1='',n2='',n3='',n4='',n5=''):#变量设置
        #6个基本属性
        self.v_sno = tk.StringVar()
        self.v_sno.set(sno)
        self.v_name = tk.StringVar()
        self.v_name.set(name)
        self.v_gender = tk.StringVar()
        self.v_gender.set(gender)
        self.v_subject = tk.StringVar()
        self.v_subject.set(subject)
        self.v_num = tk.StringVar()
        self.v_num.set(num)
        self.v_home = tk.StringVar()
        self.v_home.set(home)

        #用户可以定义的5个属性
        self.v_n1 = tk.StringVar()
        self.v_n2 = tk.StringVar()
        self.v_n3 = tk.StringVar()
        self.v_n4 = tk.StringVar()
        self.v_n5 = tk.StringVar()
        self.v_n1.set(n1)
        self.v_n2.set(n2)
        self.v_n3.set(n3)
        self.v_n4.set(n4)
        self.v_n5.set(n5)

        #变量的副本
        self.vv_sno = sno
        self.vv_name = name
        self.vv_gender = gender
        self.vv_subject = subject
        self.vv_num = num
        self.vv_home = home

        self.vv_n1 = n1
        self.vv_n2 = n2
        self.vv_n3 = n3
        self.vv_n4 = n4
        self.vv_n5 = n5

        #用户定义属性列表
        self.v_list = [self.v_n1,self.v_n2,self.v_n3,self.v_n4,self.v_n5]

    def _attribute_number(self,llist):#计算用户自定义属性个数
        #用户定义属性列表
        self.attribute_list = []
        #用户自定义属性个数
        self.number = 0
        if len(llist) != 0:
            for item in llist:
                self.number += 1
                self.attribute_list.append(item)
        else:
            pass

    def _dynamic_add_widget(self,number):#动态添加部件
        text = self.attribute_list[number] + ':'
        self.temporary_lable = ttk.Label(self.win,text=text,bootstyle="dark",font=("微软雅黑",13),foreground='red')
        self.temporary_lable.place(relx=0.02,rely=0.4+((number+1)*0.1))
        self.temporary_entry = ttk.Entry(self.win,textvariable=self.v_list[number],font=("微软雅黑",13))
        self.temporary_entry.place(relx=0.2,rely=0.4+((number+1)*0.1))

    def _v_attribute_opreadtion(self):#用户自定义属性的数据库操作
        if self.number == 0:
            return
        sql = f"UPDATE student_{self.user_id} SET "
        #遍历组装sql语句->先添加自定义属性
        for i in range(self.number):
            if i == 0:
                ss = f'{self.attribute_list[i]}=%s'
            else:
                ss = f',{self.attribute_list[i]}=%s'
            sql = sql + ss
        else:
            sql = sql + ' WHERE sno=%s'
        #存储自定义属性值的列表
        value_list = []
        #给列表添加值
        for i in range(self.number):
            value_list.append(self.v_list[i].get())
        #给value_list参数列表添加学生sno
        value_list.append(self.v_sno.get())
        #转换为元组格式
        value_list = tuple(value_list)
        #调用多线程函数给数据库传递自定义属性
        self._threading(sql,method='sql_attribute',elements=value_list)

    def _style_setting(self):#部件样式设置
        #按钮样式
        self.style_button = ttk.Style()
        self.style_button.configure("TRadiobutton",font=("微软雅黑",13))
        self.style_button.configure("Link.TButton",font=("微软雅黑",18))
#####################################################################################

#####################################################################################
#功能设置部分
    def _check_information(self):
        # 取变量
        sno = self.v_sno.get()
        name = self.v_name.get()
        gender = self.v_gender.get()
        subject = self.v_subject.get()
        num = self.v_num.get()
        home = self.v_home.get()
        n1 = self.v_n1.get()
        n2 = self.v_n2.get()
        n3 = self.v_n3.get()
        n4 = self.v_n4.get()
        n5 = self.v_n5.get()

        # 查询
        sql = "SELECT sno FROM student_{} WHERE sno=%s".format(self.user_id)
        # 添加
        sql_extra = "INSERT INTO student_{} (sno,name,gender,subject,num,home) VALUES (%s,%s,%s,%s,%s,%s)".format(self.user_id)
        # 修改
        sql_additional = "UPDATE student_{} SET sno=%s,name=%s,gender=%s,subject=%s,num=%s,home=%s WHERE sno=%s".format(self.user_id)

        if (sno,name,gender,subject,num,home,n1,n2,n3,n4,n5) == (self.vv_sno,self.vv_name,self.vv_gender,self.vv_subject,
                                                                 self.vv_num,self.vv_home,self.vv_n1,self.vv_n2,self.vv_n3,
                                                                 self.vv_n4,self.vv_n5):
            tk.messagebox.showinfo("逗我呢","你没有做出任何修改，不需要提交",parent=self.win)
        else:
            if sno == "":#判断是否为空
                tk.messagebox.showinfo("学号不能为零","学号不能为零",parent=self.win)
            else:#判断是添加还是修改
                flag = self._threading(sql,elements=sno,method='sql')
                if self.vv_sno == sno:#修改
                    flag_extra = tk.messagebox.askyesno("请确认","确定信息无误了吗？(修改)",parent=self.win)
                    if flag_extra == True:
                        try:
                            self._threading(sql_additional, elements=(sno,name,gender,subject,num,home,sno), method='sql_additional')
                            self._v_attribute_opreadtion()
                        except Exception:
                            tk.messagebox.showinfo("错误","出现了一个错误.可能是由于网络问题导致的,请稍后再试,或尝试联系管理员",parent=self.win)
                        else:
                            tk.messagebox.showinfo("成功","成功修改这条信息",parent=self.win)
                            self.student_operation._update_data()
                            self._exit()
                else:#添加
                    if flag:
                        tk.messagebox.showwarning("学号重复", "学号重复啦，请尝试更换",parent=self.win)
                    else:
                        flag_extra = tk.messagebox.askyesno("请确认", "确定信息无误了吗？(添加)", parent=self.win)
                        if flag_extra == True:
                            try:
                                self._threading(sql_extra,elements=(sno,name,gender,subject,num,home),method='sql_extra')
                                self._v_attribute_opreadtion()
                            except Exception:
                                tk.messagebox.showinfo("错误", "出现了一个错误.可能是由于网络问题导致的,请稍后再试,或尝试联系管理员", parent=self.win)
                            else:
                                tk.messagebox.showinfo("成功", "成功增加这条信息", parent=self.win)
                                self.student_operation._update_data()
                                self._exit()
#####################################################################################

#####################################################################################
#多线程部分
    def _threading(self,sql,elements=None,method=None):#多线程(数据库操作)
        def _sql(sql,elements):
            flag = self.pool._execute_Gui_Student(sql,elements,method='sql')
            q.put(flag)

        def _sql_extra(sql_extra,elements):
            self.pool._execute_Gui_Student(sql_extra,elements,method='sql_extra')

        def _sql_additional(sql_additional,elements):
            self.pool._execute_Gui_Student(sql_additional,elements,method='sql_additional')

        def _sql_attribute(sql_attribute,elements):
            self.pool._execute_Gui_Student(sql_attribute,elements,method='sql_attribute')

        q = queue.Queue()
        try:
            if method == 'sql':
                t = threading.Thread(target=_sql,args=(sql,elements,))
                t.start()
                time.sleep(0.3)
                if not q.empty():
                    return q.get()
                else:
                    pass
            elif method == 'sql_extra':
                t = threading.Thread(target=_sql_extra,args=(sql,elements,))
                t.start()
                time.sleep(0.3)
            elif method == 'sql_additional':
                t = threading.Thread(target=_sql_additional,args=(sql,elements,))
                t.start()
                time.sleep(0.3)
            elif method == 'sql_attribute':
                t = threading.Thread(target=_sql_attribute,args=(sql,elements))
                t.start()
                time.sleep(0.3)
        except Exception as e:
            raise e
#####################################################################################

#####################################################################################
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

    def _tooltip(self):
        self.confirm_text = "点击确认数据."
        ToolTip(self.confirm_button,text=self.confirm_text)
#####################################################################################

#####################################################################################
#页面进入与退出部分
    def _start(self,llist=[],list=[]):#入口
        #进入用户定义属性设置函数->llist表示属性
        self._attribute_number(llist)
        #进入变量设置函数->list表示属性的值
        self._variable_setting(*list)
        self.win_main.attributes("-disabled",1)#令学生页面不能操作
        #进入页面设置
        self._gui_base()

    def _exit(self):
        self.win_main.attributes("-disabled",0)#令学生页面可以操作
        self.win.destroy()
#####################################################################################