import time
import pandas as pd
import matplotlib.pyplot as plt
import serial
import argparse
import serial.tools.list_ports
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
def DOpenPort(portx, bps, timeout):
    ret = False
    err = False
    try:
        ser = serial.Serial(portx, bps, timeout=timeout)
        if ser.is_open:
            ret = True
    except Exception as e:
        messagebox.showinfo("提示", str(e))
        err = True
    return ser, ret, err

def DClosePort(ser):
    ser.close()

def trans(s):
    ans = ''
    minus = s[5]
    if minus == '1':
        ans += "1"
    elif minus == 'b':
        ans += "-"
    elif minus == 'c':
        ans += "-1"
    ans += s[7] + '.' + s[9] + s[11] + s[13]
    return ans

def SearchPort():
    port_list = list(serial.tools.list_ports.comports())
    port = ''
    if len(port_list) == 0:
        messagebox.showinfo("提示", "无可用串口")
        Btn1.configure(text = "开始采集", command = Start_collecting)
        return 0
    else:
        for portinfo in port_list:
            if "341" in str(portinfo):
                lbl.configure(text="已经找到仪器")
                port = str(portinfo).split()[0]
                return port
    if not port:
        messagebox.showinfo("提示", "未找到仪器")
        Btn1.configure(text = "开始采集", command = Start_collecting)
        return 0

def Start_collecting():
    Btn1.configure(text = "停止采集", command = Stop_collecting)
    txt.configure(state="normal")
    port = SearchPort()
    number = ent1.get()
    interval = ent2.get()
    if port == 0:
        return
    else:
        global canvas
        global ax
        global fig
        number = ent1.get()
        interval = ent2.get()
        try:
            nxt = int(number) + 1
        except:
            messagebox.showinfo("提示", "您输入的实验序号不是整数")
            Stop_collecting()
            return
        txt.configure(state='normal')
        txt.delete(1.0, END)
        global Judge
        Judge = 1
        df = pd.DataFrame()
        times = []
        temp = []
        starttime = time.time()
        txt.insert(INSERT, "Time/s, Temperature/K \n")
        txt.configure(state='disabled')
        while Judge == 1:
            ser, ret, err = DOpenPort(port, 1200, None)
            if err == True:
                DClosePort(ser)
                Stop_collecting()
            s = str(ser.read(7).hex())
            endtime = time.time()
            loc = s.find("ff")
            if loc:
                ser.read(loc)
            s = str(ser.read(7).hex())
            DClosePort(ser)
            try:
                T = float(trans(s))
            except:
                continue
            else:
                times.append(round(endtime - starttime, 2))
                temp.append(T)
            txt.configure(state='normal')
            txt.insert(INSERT, str(round(endtime - starttime, 2)) + ", " + trans(s) + "\n")
            txt.configure(state='disabled')
            ax.cla()
            ax.plot(times, temp)
            canvas.draw()
            try:
                time.sleep(float(interval))
                win.update()
            except:
                messagebox.showinfo("提示", "您输入的时间间隔不是浮点数")
                Stop_collecting()
    fig.savefig("./figure{}.png".format(number)) 
    df["t"] = times
    df["T"] = temp
    df.to_csv("./data{}.csv".format(number))
    lbl.configure(text = "您所需的文件已保存至figure{}.png和data{}.csv。\n 零散数据储存于info{}.txt。".format(number,number,number))
    mytxt=open("info{}.txt".format(number),'w')
    mytxt.write("实验序号：{}\n".format(ent1.get()))
    ent1.delete(0,END)
    ent1.insert(INSERT, str(nxt))
    mytxt.write("加入物质：{}\n".format(ent3.get()))
    mytxt.write("加入质量：{}\n".format(ent4.get()))
    mytxt.write("通电时间：{}\n".format(ent5.get()))
    mytxt.write("通电时间：{}\n".format(txt.get(1.0, END)))
    mytxt.close()

def Stop_collecting():
    global Judge
    Judge = 0
    Btn1.configure(text = "开始采集", command = Start_collecting)

def Start_heating():
    global Btn2
    var = IntVar()
    ent5.delete(0, END)
    Btn2.configure(text = "停止加热！", command=lambda: var.set(1))
    heat_time = time.time()
    global heat
    heat = 1
    Btn2.wait_variable(var)
    end_heat_time = time.time()
    ent5.insert(INSERT, "{}".format(str(round(end_heat_time - heat_time, 2))))
    Btn2.configure(text = "开始加热！", command = Start_heating)

def _quit():
    win.quit()
    win.destroy()

win = Tk()
win.title("物理化学实验燃烧热/溶解热数据采集小帮手")
win.geometry("1500x1500")
win.protocol("WM_DELETE_WINDOW", _quit)
Judge = 0
Btn1 = Button(win, text = "开始采集",
    font=("宋体", 21),
    command = Start_collecting)
Btn1.grid(row=0,column = 0, )
Btn1.grid(row=0,column = 0, )
Btn2 = Button(win, text = "开始加热！",
    font=("宋体", 21),
    command = Start_heating)
Btn2.grid(row=0,column = 2, )
lbl = Label(win, 
    text="您好！欢迎使用陈硕航开发的物化实验小助手！\n 本程序旨在帮助大家减少读数的烦恼。\n以及，诚挚招聘UI一名。\n 祝学习愉快！\n P.S.:感谢罗伟梁学长提供的读数接口程序。",
    font=("宋体", 18))
lbl.grid(row = 1, columnspan=4)
txt = scrolledtext.ScrolledText(win, width=50, height=15, font=("宋体", 15))
txt.grid(row = 3, column = 4, rowspan=4)
lbl1 = Label(win, 
    text="实验序号：",
    font=("宋体", 18))
lbl1.grid(row = 2, column=0, )
ent1 = Entry(win, font=("宋体", 15))
ent1.grid(row = 2, column=1, )
lbl2 = Label(win,
    text="采样时间间隔：",
    font=("宋体", 18))
lbl2.grid(row=2, column =2)
ent2 = Entry(win, font=("宋体", 15))
ent2.grid(row = 2, column = 3)
ent1.insert(INSERT, "0")
ent2.insert(INSERT, "0.4")
lbl3 = Label(win, 
    text = "加入物质（可多个）：",
    font=("宋体", 18))
lbl3.grid(row = 3, column= 0, )
ent3 = Entry(win, font=("宋体", 15))
ent3.grid(row = 3, column= 1)
lbl4 = Label(win, 
    text = "加入质量（可多个）：",
    font=("宋体", 18))
lbl4.grid(row = 3, column= 2)
ent4 = Entry(win, font=("宋体", 15))
ent4.grid(row = 3, column= 3)
lbl5 = Label(win, 
    text = "通电时间：",
    font=("宋体", 18))
lbl5.grid(row = 4, column= 0)
ent5 = Entry(win, font=("宋体", 15))
ent5.grid(row = 4, column= 1)
fig, ax = plt.subplots(figsize = (5,5))
ax.set_xlabel(r"$t/\mathrm{s}$")
ax.set_ylabel(r"$\Delta T/\mathrm{K}$")
canvas = FigureCanvasTkAgg(fig, master = win)
canvas.get_tk_widget().grid(column=4 ,row = 0, rowspan = 2)

if __name__ == "__main__":    
    win.mainloop()