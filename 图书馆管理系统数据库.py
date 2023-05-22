import pymysql
import tkinter as tk
import tkinter.messagebox
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='L96732140',
    port=3306,          
    db='library',
    charset='utf8'     
)
tcursor = conn.cursor()

def login():
    def goto(num):
        root.destroy()
        if num == 1:
            reader_control()
        if num == 2:
            book_control()
        if num == 3:
            borrow_back()
            
    root = tk.Tk()    
    root.title('主菜单')
    tk.Label(root, text="欢迎进入图书管理系统！",width = 40,height =4,bg = "orange", fg = "black",font=("黑体",30)).pack()
    tk.Button(root, text='管理用户', width=10, command=lambda:goto(1)).pack()
    tk.Button(root, text='管理书籍', width=10, command=lambda:goto(2)).pack()
    tk.Button(root, text='借阅管理', width=10, command=lambda:goto(3)).pack()
    # 退出按钮
    tk.Button(root, text='退出', width=10, command=lambda:exit_login(root)).pack()
    root.mainloop()

def reader_control():
    def gotoreader(num):
        root.destroy()
        if num == 1:
            insert()
        if num == 2:
            delete()
        if num == 3:
            select()
        if num == 4:
            update()
        if num == 5:
            login()
    root = tk.Tk()    
    root.title('读者管理')
    tk.Button(root, text='增加用户', width=10, command=lambda:gotoreader(1)).pack()
    tk.Button(root, text='注销用户', width=10, command=lambda:gotoreader(2)).pack()
    tk.Button(root, text='查询用户', width=10, command=lambda:gotoreader(3)).pack()
    tk.Button(root, text='更新用户', width=10, command=lambda:gotoreader(4)).pack()

    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:gotoreader(5)).pack()

def update():
    def gotologin(num):
        root1.destroy()
        if num == 1:
            reader_control()
    root1 = tk.Tk()
    root1.title('更新用户')
    v1 = tk.StringVar()

    # ID标签，位置在第0行第0列
    tk.Label(root1, text='用户ID:').grid(row=0, column=0)
    # ID输入框
    global input61
    input61 = tk.Entry(root1, textvariable=v1)
    input61.grid(row=0, column=1, padx=10, pady=5)
    
    # 登录按钮
    tk.Button(root1, text='确认', width=10, command=lambda:auto_update(root1)).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root1, text='返回', width=10, command=lambda:gotologin(1)).grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)
    root1.mainloop()

def auto_update(root1):
    entry1 = input61.get()
    sql = 'select * from reader_information where reader_information.reader_id = %s'
    param =(entry1)
    tcursor.execute(sql,param)
    list_re = tcursor.fetchall()
    if len(list_re) <= 0:
        tkinter.messagebox.showinfo('提示',entry1+'用户不存在，请输入其他用户ID！')
    else:
        root1.destroy()
        def gotoinsert():
            root.destroy()
            update()
        root = tk.Tk()
        root.title('更新内容')
        v1 = tk.StringVar()
        v2 = tk.StringVar()
        global input62,input63
        tk.Label(root, text='新名称:').grid(row=0, column=0)
        tk.Label(root, text='新ID:').grid(row=1, column=0)
        input62 = tk.Entry(root, textvariable=v1)
        input62.grid(row=0, column=1, padx=10, pady=5)
        input63 = tk.Entry(root, textvariable=v2)
        input63.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text='确认', width=10, command=lambda:autoupdate(root,entry1)).grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        tk.Button(root, text='返回', width=10, command=gotoinsert).grid(row=2, column=2, sticky=tk.E, padx=10, pady=5)

def autoupdate(root1,entry1):
    entry2 = input62.get()
    entry3 = input63.get()
    
    if entry1 and entry2 and entry3:
        sql1 = 'call updatereader(%s,%s,%s)'
        param1 =(entry2,entry3,entry1)
        tcursor.execute(sql1,param1)
        conn.commit()
        root1.destroy()
        def gotoinsert():
            root.destroy()
            update()
        root = tk.Tk()
        root.title('提示')
        tk.Label(root, text="更新成功！").pack()
        tk.Button(root, text='确认', width=10, command=gotoinsert).pack()
        root.mainloop()
    else:
        root1.destroy()
        def gotoinsert():
            root.destroy()
            update()
        root = tk.Tk()
        root.title('提示')
        tk.Label(root, text="更新失败！").pack()
        tk.Button(root, text='确认', width=10, command=gotoinsert).pack()
        root.mainloop()


def insert():
    def gotologin(num):
        root1.destroy()
        if num == 1:
            reader_control()
    root1 = tk.Tk()
    root1.title('增加用户')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()

    # ID标签，位置在第0行第0列
    tk.Label(root1, text='ID:').grid(row=0, column=0)
    # 姓名标签，位置在第1行第0列
    tk.Label(root1, text='姓名:').grid(row=1, column=0)
    # 班级标签，位置在第3行第0列
    tk.Label(root1, text='班级:').grid(row=2, column=0)

    # ID输入框
    global input1
    input1 = tk.Entry(root1, textvariable=v1)
    input1.grid(row=0, column=1, padx=10, pady=5)
    # 姓名输入框
    global input2
    input2 = tk.Entry(root1, textvariable=v2)
    input2.grid(row=1, column=1, padx=10, pady=5)
    #班级输入框
    global input3
    input3 = tk.Entry(root1, textvariable=v3)
    input3.grid(row=2, column=1, padx=10, pady=5)

    # 登录按钮
    tk.Button(root1, text='录入', width=10, command=lambda:auto_insert1(root1)).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root1, text='返回', width=10, command=lambda:gotologin(1)).grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)
    root1.mainloop()

def auto_insert1(root1):
    entry1 = input1.get()
    entry2 = input2.get()
    entry3 = input3.get()

    sql = 'insert into reader_information values(%s,%s,%s,0)'
    param =(entry1,entry2,entry3)
    tcursor.execute(sql,param)
    conn.commit()
    root1.destroy()
    def gotoinsert():
        root.destroy()
        insert()
    root = tk.Tk()
    root.title('提示')
    tk.Label(root, text="插入成功！").pack()
    tk.Button(root, text='确认', width=10, command=gotoinsert).pack()
    root.mainloop()

def delete():
    def gotologin(num):
        root.destroy()
        if num == 1:
            reader_control()
    root = tk.Tk()
    root.title('注销用户')
    v1 = tk.StringVar()

    # 姓名标签，位置在第0行第0列
    tk.Label(root, text='ID:').grid(row=0, column=0)
    # 姓名输入框
    global input1
    input1 = tk.Entry(root, textvariable=v1)
    input1.grid(row=0, column=1, padx=10, pady=5)
    # 登录按钮
    tk.Button(root, text='删除', width=10, command=lambda:auto_delete(root)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:gotologin(1)).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
    root.mainloop()

def auto_delete(root1):
    entry1 = input1.get()
    sql = 'call deletereader(%s)'
    param =(entry1)
    tcursor.execute(sql,param)
    root1.destroy()
    def gotodelete():
        conn.commit()
        root.destroy()
        delete()
    def goto():
        conn.rollback()
        conn.commit()
        root.destroy()
        def gotodelete1():
            root2.destroy()
            delete()
        root2 = tk.Tk()
        root2.title('提示')
        tk.Label(root2, text="撤回成功！").pack()
        tk.Button(root2, text='确认', width=10, command=gotodelete1).pack()
        root2.mainloop()
    root = tk.Tk()
    root.title('提示')
    tk.Label(root, text="删除成功！").pack()
    tk.Button(root, text='确认', width=10, command=gotodelete).pack()
    tk.Button(root, text='取消删除', width=10, command=goto).pack()
    root.mainloop()

def select():
    def gotologin(num):
        root.destroy()
        if num == 1:
            reader_control()
    root = tk.Tk()
    root.title('查询用户')
    v1 = tk.StringVar()

    tk.Label(root, text='ID:').grid(row=0, column=0)
    # 姓名输入框
    global input41
    input41 = tk.Entry(root, textvariable=v1)
    input41.grid(row=0, column=1, padx=10, pady=5)
    # 登录按钮
    tk.Button(root, text='查询', width=10, command=lambda:auto_select(root)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:gotologin(1)).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
    root.mainloop()

def auto_select(root1):
    entry1 = input41.get()
    sql = 'select * from reader_information where reader_information.reader_id=%s'
    param =(entry1)
    tcursor.execute(sql,param)
    list_re = tcursor.fetchall()
    
    if len(list_re) <= 0:
        tkinter.messagebox.showinfo('提示',entry1+'用户不存在，请输入其他用户ID！')
    else:
        sql2 = 'select * from history where 编号=%s'
        param2 =(entry1)
        tcursor.execute(sql2,param2)
        list_re2 = tcursor.fetchall()
        root1.destroy()
        def gotoselect():
            root.destroy()
            select()
        root = tk.Tk()
        root.title('提示')
        tk.Label(root, text="查询结果",width = 40,height =4,bg = "orange", fg = "black",font=("黑体",30)).pack()
        user_id = tk.StringVar()
        user_id.set('')
        user_name = tk.StringVar()
        user_name.set('')
        user_class = tk.StringVar()
        user_class.set('')
        user_borrowednumber = tk.StringVar()
        user_borrowednumber.set('')
        user_id.set(list_re[0][0])
        user_name.set(list_re[0][1])
        user_class.set(list_re[0][2])
        user_borrowednumber.set(list_re[0][3])
        tk.Label(root,text='用户ID：').place(x=40,y=150)
        tk.Label(root, textvariable=user_id).place(x = 100,y=150)
        tk.Label(root,text='姓名：').place(x=40,y=170)
        tk.Label(root, textvariable=user_name).place(x = 100,y=170)
        tk.Label(root,text='班级：').place(x=40,y=190)
        tk.Label(root, textvariable=user_class).place(x = 100,y=190)
        tk.Label(root,text='借阅总数：').place(x=40,y=210)
        tk.Label(root, textvariable=user_borrowednumber).place(x = 100,y=210)
        tk.Label(root,text='借阅历史：').place(x=40,y=230)
        n = len(list_re2)
        t = [tk.StringVar() for _ in range(n)]
        for i in range(n):
            t[i].set(list_re2[i])
            tk.Label(root, textvariable=t[i]).place(x = 40,y=230+(i+1)*20)
        tk.Button(root, text='确认', width=10, command=gotoselect).place(x=120,y=250+n*20)
        tk.Button(root, text='欠费查询', width=10, command=lambda:auto_select_payment(root,list_re[0][0])).place(x=250,y=250+n*20)
        root.mainloop()

def auto_select_payment(root1,entry1):
    sql = 'select * from reader_payment where reader_payment.reader_id=%s'
    param =(entry1)
    tcursor.execute(sql,param)
    list_re = tcursor.fetchall()
    
    if len(list_re) <= 0:
        tkinter.messagebox.showinfo('提示',entry1+'用户不欠费！')
    else:
        root1.destroy()
        def gotoselect(num):
            root.destroy()
            if num == 1:
                delete_payment(entry1)
            if num == 2:
                select()
        root = tk.Tk()
        root.title('欠费详情')
        n = len(list_re)
        tk.Label(root,text='违约次数：').place(x=40,y=90)
        tk.Label(root, text=n).place(x = 100,y=90)
        tk.Button(root, text='缴费', width=10, command=lambda:gotoselect(1)).place(x=100,y=130)
        tk.Button(root, text='返回', width=10, command=lambda:gotoselect(2)).place(x=230,y=130)
        root.mainloop()

def delete_payment(entry1):
    sql = 'delete from reader_payment where reader_payment.reader_id=%s'
    param =(entry1)
    tcursor.execute(sql,param)
    conn.commit()
    def goto():
        root.destroy()
        select()
    root = tk.Tk()
    root.title('提示')
    tk.Label(root, text="缴费成功！").pack()
    tk.Button(root, text='确认', width=10, command=goto).pack()
    root.mainloop()

def book_control():
    def gotobook(num):
        root.destroy()
        if num == 1:
            insert_book()
        if num == 2:
            delete_book()
        if num == 3:
            select_book()
        if num == 4:
            login()
    root = tk.Tk()    
    root.title('图书管理')
    tk.Button(root, text='增加书籍', width=10, command=lambda:gotobook(1)).pack()
    tk.Button(root, text='删除书籍', width=10, command=lambda:gotobook(2)).pack() 
    tk.Button(root, text='查询书籍', width=10, command=lambda:gotobook(3)).pack()
    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:gotobook(4)).pack()

def select_book():
    def gotologin(num):
        root.destroy()
        if num == 1:
            book_control()
    root = tk.Tk()
    root.title('书籍查询')
    v1 = tk.StringVar()

    tk.Label(root, text='书籍名称:').grid(row=0, column=0)
    # 姓名输入框
    global input51
    input51 = tk.Entry(root, textvariable=v1)
    input51.grid(row=0, column=1, padx=10, pady=5)
    # 登录按钮
    tk.Button(root, text='查询', width=10, command=lambda:auto_select_book(root)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:gotologin(1)).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
    root.mainloop()

def auto_select_book(root1):
    entry1 = input51.get()
    sql = 'select * from book_inventory where book_inventory.book_name=%s'
    param =(entry1)
    tcursor.execute(sql,param)
    list_re = tcursor.fetchall()
    
    if len(list_re) <= 0:
        tkinter.messagebox.showinfo('提示',entry1+'不存在，请输入其他书籍名称！')
    else:
        root1.destroy()
        sql2 = 'select * from book_information where book_information.book_name=%s and book_information.book_is_in=1'
        param2 =(entry1)
        tcursor.execute(sql2,param2)
        list_re2 = tcursor.fetchall()
        def gotoselect(num):
            root.destroy()
            if num == 1:
                borrow_book()
            if num == 2:
                select_book()
        root = tk.Tk()
        root.title('提示')
        tk.Label(root, text="查询结果",width = 40,height =4,bg = "orange", fg = "black",font=("黑体",30)).pack()
        book_name = tk.StringVar()
        book_name.set('')
        book_total = tk.StringVar()
        book_total.set('')
        book_sur = tk.StringVar()
        book_sur.set('')
        book_name.set(list_re[0][0])
        book_total.set(list_re[0][1])
        book_sur.set(list_re[0][2])
        tk.Label(root,text='书籍名称：').place(x=40,y=150)
        tk.Label(root, textvariable=book_name).place(x = 100,y=150)
        tk.Label(root,text='馆藏总数：').place(x=200,y=150)
        tk.Label(root, textvariable=book_total).place(x = 270,y=150)
        tk.Label(root,text='在馆数：').place(x=300,y=150)
        tk.Label(root, textvariable=book_sur).place(x = 350,y=150)
        n = len(list_re2)
        t = [tk.StringVar() for _ in range(n)]
        for i in range(n):
            t[i].set(list_re2[i][0:5])
            tk.Label(root, textvariable=t[i]).place(x = 40,y=150+(i+1)*20)
        tk.Button(root, text='借阅', width=10, command=lambda:gotoselect(1)).place(x=40,y=170+n*20)
        tk.Button(root, text='返回', width=10, command=lambda:gotoselect(2)).place(x=190,y=170+n*20)
        root.mainloop()

def insert_book():
    def back(num):
        root1.destroy()
        if num == 1:
            book_control()
    root1 = tk.Tk()
    root1.title('增加图书')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    v5 = tk.StringVar()

    # ID标签，位置在第0行第0列
    tk.Label(root1, text='编号:').grid(row=0, column=0)
    # 姓名标签，位置在第1行第0列
    tk.Label(root1, text='书名:').grid(row=1, column=0)
    # 班级标签，位置在第3行第0列
    tk.Label(root1, text='作者:').grid(row=2, column=0)
    # 总借阅标签，位置在第3行第0列
    tk.Label(root1, text='类型:').grid(row=3, column=0)
    tk.Label(root1, text='出版商:').grid(row=4, column=0) 
    # ID输入框
    global input11
    input11 = tk.Entry(root1, textvariable=v1)
    input11.grid(row=0, column=1, padx=10, pady=5)
    # 姓名输入框
    global input12
    input12 = tk.Entry(root1, textvariable=v2)
    input12.grid(row=1, column=1, padx=10, pady=5)
    #班级输入框
    global input13
    input13 = tk.Entry(root1, textvariable=v3)
    input13.grid(row=2, column=1, padx=10, pady=5)
    #总借阅输入框
    global input14
    input14 = tk.Entry(root1, textvariable=v4)
    input14.grid(row=3, column=1, padx=10, pady=5)
    global input15
    input15 = tk.Entry(root1, textvariable=v5)
    input15.grid(row=4, column=1, padx=10, pady=5)
    # 登录按钮
    tk.Button(root1, text='录入', width=10, command=lambda:auto_insert_book(root1)).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root1, text='返回', width=10, command=lambda:back(1)).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)
    root1.mainloop()

def auto_insert_book(root1):
    entry1 = input11.get()
    entry2 = input12.get()
    entry3 = input13.get()
    entry4 = input14.get()
    entry5 = input15.get()

    if entry1 and entry2 and entry3 and entry4 and entry5:
        sql = 'insert into book_information values(%s,%s,%s,%s,%s,1,0)'
        param =(entry1,entry2,entry3,entry4,entry5)
        tcursor.execute(sql,param)
        conn.commit()
        root1.destroy()
        def gotoinsert():
            root.destroy()
            insert_book()
        root = tk.Tk()
        root.title('提示')
        tk.Label(root, text="插入成功！").pack()
        tk.Button(root, text='确认', width=10, command=gotoinsert).pack()
        root.mainloop()
    else:
        sql = 'insert into book_information values(%s,%s,%s,%s,%s,1,0)'
        param =(entry1,entry2,entry3,entry4,"")
        tcursor.execute(sql,param)
        conn.commit()
        sql = 'delete from book_information where book_id=%s'
        param =("")
        tcursor.execute(sql,param)
        conn.commit()
        root1.destroy()
        def gotoinsert():
            root.destroy()
            insert_book()
        root = tk.Tk()
        root.title('提示')
        tk.Label(root, text="插入失败！").pack()
        tk.Button(root, text='确认', width=10, command=gotoinsert).pack()
        root.mainloop()

def delete_book():
    def back(num):
        root.destroy()
        if num == 1:
            book_control()
    root = tk.Tk()
    root.title('删除图书')
    v1 = tk.StringVar()

    # 姓名标签，位置在第0行第0列
    tk.Label(root, text='ID:').grid(row=0, column=0)
    # 姓名输入框
    global input1
    input1 = tk.Entry(root, textvariable=v1)
    input1.grid(row=0, column=1, padx=10, pady=5)
    # 登录按钮
    tk.Button(root, text='删除', width=10, command=lambda:auto_delete_book(root)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:back(1)).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
    root.mainloop()

def auto_delete_book(root1):
    entry1 = input1.get()
    sql = 'delete from book_information where book_information.book_id=%s'
    param =(entry1)
    tcursor.execute(sql,param)
    conn.commit()
    root1.destroy()
    def gotodelete():
        root.destroy()
        delete_book()
    root = tk.Tk()
    root.title('提示')
    tk.Label(root, text="删除成功！").pack()
    tk.Button(root, text='确认', width=10, command=gotodelete).pack()
    root.mainloop()

def borrow_back():
    def goto(num):
        root.destroy()
        if num == 1:
            borrow_book()
        if num == 2:
            back_book()
        if num == 3:
            login()
    root = tk.Tk()    
    root.title('借阅管理')
    tk.Button(root, text='借书', width=10, command=lambda:goto(1)).pack()
    tk.Button(root, text='还书', width=10, command=lambda:goto(2)).pack()
    # 退出按钮
    tk.Button(root, text='返回', width=10, command=lambda:goto(3)).pack()

def borrow_book():
    def back(num):
        root1.destroy()
        if num == 1:
            borrow_back()
    root1 = tk.Tk()
    root1.title('借书')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()

    tk.Label(root1, text='书籍编号:').grid(row=0, column=0)
    tk.Label(root1, text='书籍名称:').grid(row=1, column=0)
    tk.Label(root1, text='读者编号:').grid(row=2, column=0)
    tk.Label(root1, text='借书日期:').grid(row=3, column=0)

    global input21
    input21 = tk.Entry(root1, textvariable=v1)
    input21.grid(row=0, column=1, padx=10, pady=5)

    global input22
    input22 = tk.Entry(root1, textvariable=v2)
    input22.grid(row=1, column=1, padx=10, pady=5)

    global input23
    input23 = tk.Entry(root1, textvariable=v3)
    input23.grid(row=2, column=1, padx=10, pady=5)

    global input24
    input24 = tk.Entry(root1, textvariable=v4)
    input24.grid(row=3, column=1, padx=10, pady=5)
    
    # 登录按钮
    tk.Button(root1, text='录入', width=10, command=lambda:auto_borrow_book(root1)).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root1, text='返回', width=10, command=lambda:back(1)).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)
    root1.mainloop()

def auto_borrow_book(root1):
    entry1 = input21.get()
    entry2 = input22.get()
    entry3 = input23.get()
    entry4 = input24.get()
    sql = 'call insert_into_readerborrow(%s,%s,%s,%s)'
    param =(entry1,entry2,entry3,entry4)
    tcursor.execute(sql,param)
    conn.commit()
    root1.destroy()
    def gotoborrow():
        root.destroy()
        borrow_book()
    root = tk.Tk()
    root.title('提示')
    tk.Label(root, text="借阅成功！").pack()
    tk.Button(root, text='确认', width=10, command=gotoborrow).pack()
    root.mainloop()

def back_book():
    def back(num):
        root1.destroy()
        if num == 1:
            borrow_back()
    root1 = tk.Tk()
    root1.title('还书')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()

    tk.Label(root1, text='书籍编号:').grid(row=0, column=0)
    tk.Label(root1, text='书籍名称:').grid(row=1, column=0)
    tk.Label(root1, text='读者编号:').grid(row=2, column=0)
    tk.Label(root1, text='还书日期:').grid(row=3, column=0)

    global input31
    input31 = tk.Entry(root1, textvariable=v1)
    input31.grid(row=0, column=1, padx=10, pady=5)

    global input32
    input32 = tk.Entry(root1, textvariable=v2)
    input32.grid(row=1, column=1, padx=10, pady=5)

    global input33
    input33 = tk.Entry(root1, textvariable=v3)
    input33.grid(row=2, column=1, padx=10, pady=5)

    global input34
    input34 = tk.Entry(root1, textvariable=v4)
    input34.grid(row=3, column=1, padx=10, pady=5)
    
    # 登录按钮
    tk.Button(root1, text='录入', width=10, command=lambda:auto_back_book(root1)).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    # 退出按钮
    tk.Button(root1, text='返回', width=10, command=lambda:back(1)).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)
    root1.mainloop()

def auto_back_book(root1):
    entry1 = input31.get()
    entry2 = input32.get()
    entry3 = input33.get()
    entry4 = input34.get()
    sql = 'call insert_into_readerback(%s,%s,%s,%s)'
    param =(entry1,entry2,entry3,entry4)
    tcursor.execute(sql,param)
    conn.commit()
    sql2 = 'call ispayment(%s,%s)'
    param2 =(entry1,entry3)
    tcursor.execute(sql2,param2)
    conn.commit()
    root1.destroy()
    def gotoborrow():
        root.destroy()
        borrow_book()
    root = tk.Tk()
    root.title('提示')
    tk.Label(root, text="归还成功！").pack()
    tk.Button(root, text='确认', width=10, command=gotoborrow).pack()
    root.mainloop()

def exit_login(root):
    root.destroy()
    pass

if __name__ == '__main__':
    login()