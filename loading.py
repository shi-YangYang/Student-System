import tkinter
from pathlib import Path
from itertools import cycle
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageSequence
import sys

class AnimatedGif(ttk.Frame):#动图类
    def __init__(self, master,path):
        super().__init__(master, width=200, height=400)

        # 开启动图
        file_path = Path(__file__).parent / path
        with Image.open(file_path) as im:
            # 创建序列
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # 框架
            self.framerate = im.info["duration"]

        self.img_container = ttk.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill="both", expand="yes")
        self.after_id = self.after(self.framerate, self.next_frame)

    def next_frame(self):
        #动图下一帧
        self.img_container.configure(image=next(self.image_cycle))
        self.after_id = self.after(self.framerate, self.next_frame)

class Create_Loading:#创建动图类
    def __init__(self,path,image_width,image_height):
        #动图的路径
        self.path = path
        #动图的宽度【像素】
        self.image_width = image_width
        #动图的宽度【像素】
        self.image_height = image_height
        #动图基本设置
        self._base_setting()

    def _base_setting(self):
        self.win = ttk.Toplevel()
        #页面尺寸设置
        self._size_setting()
        #动图类实例
        self.gif = AnimatedGif(self.win,self.path)
        self.gif.pack(fill=BOTH, expand=YES)

        self.win.overrideredirect(1)

    def _size_setting(self):
        self.screenWidth = self.win.winfo_screenwidth()
        self.screenHeight = self.win.winfo_screenheight()
        self.left = (self.screenWidth - self.image_width) / 2
        self.height = (self.screenHeight - self.image_height) / 2
        self.win.geometry('%dx%d+%d+%d' % (self.image_width, self.image_height, self.left, self.height))

    def _run(self):
        if not self.win:
            self._base_setting()

    def _exit(self):
        if self.win:
            self.gif.after_cancel(self.gif.after_id)
            self.win.destroy()
        else:
            print("窗体已经不存在了.")

class Create_Loading_extra:#->测试类.
    def __init__(self,path,left,right):
        self.path = path
        self.lleft = left
        self.rright = right
        self._setting()
        self.flag = None

    def _setting(self):

        self.win = tkinter.Tk()
        self._size_set()

        self.gif = AnimatedGif(self.win,self.path)
        self.gif.pack(fill=BOTH, expand=YES)

        self.win.overrideredirect(1)
        self.win.mainloop()

    def _size_set(self):
        self.screenWidth = self.win.winfo_screenwidth()
        self.screenHeight = self.win.winfo_screenheight()
        #self.left = (self.screenWidth - self.lleft) / 2
        self.height = (self.screenHeight - self.rright) / 2
        self.win.geometry('%dx%d+%d+%d' % (self.lleft, self.rright, 200, self.height))

    def _run(self):
        if not self.win:
            self._setting()

    def _exit(self):
        if self.win:
            self.gif.after_cancel(self.gif.after_id)
            self.win.destroy()
            sys.exit(0)
        else:
            print("self.win has already been destroyed")



#测试代码部分.
#a = Create_Loading_extra("photo/login-load.gif", 400, 400)
'''
a = tkinter.Tk()
load = Create_Loading("photo/loading.gif",300,300)
load._run()
a.mainloop()
'''