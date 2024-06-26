
# Developed By Eng. Ali Donea

__author__ = "Al-shamel Center"
import sqlite3
import re
import os
import uuid
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date, datetime
from tkinter.constants import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import shutil
from fpdf import FPDF
import arabic_reshaper
import bidi.algorithm
with sqlite3.connect("./Database/NBDb.db") as db:
    cur = db.cursor()
def ar_display(val):
    return bidi.algorithm.get_display(arabic_reshaper.reshape(str(val)))
def num2day(date1):
    days = ['الإثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت','الأحد']
    day = datetime.strptime(date1,'%Y-%m-%d').weekday()
    return days[day]
def Exit():
    sure = messagebox.askyesno("تنبيه","هل تريد بالتأكيد إغلاق البرنامج",parent = main)
    if sure == True:
        main.destroy()
        db.close()

main = Tk()
main.geometry("1366x768")
main.title("دفتر الديون")
main.iconbitmap("./images/ico2.ico")
main.resizable(0, 0)

user = StringVar()
passwd = StringVar()
authorizeFlage = IntVar(value=0)
current_selected_customer_name = StringVar(value='')
current_selected_customer_phone = StringVar(value='')
class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.iconbitmap("./images/ico2.ico")
        top.resizable(0, 0)
        top.title("تسجيل الدخول")
        #top.attributes('-topmost', 1)

        self.label1 = Label(main)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/login.png")
        self.label1.configure(image=self.img)
        self.change_password = Button(main,text = 'إدارة المستخدمين')
        self.change_password.place(x=725, y=470,width = 180,height=30)
        self.change_password.configure(relief="flat")
        self.change_password.configure(overrelief="flat")
        self.change_password.configure(activebackground="#105da8")
        self.change_password.configure(activeforeground="#ffffff")
        self.change_password.configure(cursor="hand2")
        self.change_password.configure(foreground="#105da8")
        self.change_password.configure(background="#ffffff")
        self.change_password.configure(borderwidth="0")
        self.change_password.configure(font="-family {tajawal} -size 14 -weight bold ")
        self.change_password.configure(command=self.change_pass)
        
        self.button1 = Button(main)
        self.button1.place(x=538, y=587, width=289, height=67)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#105da8")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#105da8")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(font="-family {Poppins SemiBold} -size 22 -weight bold")
        self.button1.configure(command=self.login)
        

        self.entry1 = Entry(main)
        self.entry1.place(x=476, y=275, width=413, height=23)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)
        self.entry1.configure(justify=CENTER)
        self.entry1.focus()

        self.entry2 = Entry(main)
        self.entry2.place(x=476, y=417, width=413, height=23)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)
        self.entry2.configure(justify=CENTER)
        

        self.backup_btn = Button(main)
        self.backup_btn.place(x=476, y=680, width=200, height=23)
        self.backup_btn.configure(relief="flat")
        self.backup_btn.configure(overrelief="flat")
        self.backup_btn.configure(activebackground="#105da8")
        self.backup_btn.configure(cursor="hand2")
        self.backup_btn.configure(foreground="#ffffff")
        self.backup_btn.configure(background="#105da8")
        self.backup_btn.configure(borderwidth="0")
        self.backup_btn.configure(text="""إنشاء نسخة احتياطية""")
        self.backup_btn.configure(font="-family Tajawal -size 12 -weight bold")
        self.backup_btn.configure(command=self.backup_db)

        self.down_bkp_btn = Button(main)
        self.down_bkp_btn.place(x=700, y=680, width=200, height=23)
        self.down_bkp_btn.configure(relief="flat")
        self.down_bkp_btn.configure(overrelief="flat")
        self.down_bkp_btn.configure(activebackground="#105da8")
        self.down_bkp_btn.configure(cursor="hand2")
        self.down_bkp_btn.configure(foreground="#ffffff")
        self.down_bkp_btn.configure(background="#105da8")
        self.down_bkp_btn.configure(borderwidth="0")
        self.down_bkp_btn.configure(text="""تحميل نسخة احتياطية""")
        self.down_bkp_btn.configure(font="-family Tajawal -size 12 -weight bold")
        self.down_bkp_btn.configure(command=self.download_backup)

        top.bind("<Return>", self.login)
    def backup_db(self):
        sure= messagebox.askyesno('تنبيه','هل تريد بالتأكيد أخذ نسخة احتياطية لقاعدة البيانات',parent=main)
        if sure:
            date1 = str(date.today())
            path = asksaveasfilename(defaultextension='db',initialfile=f'backup{date1}',initialdir='./Backups')    
            newfile = f'{path}'
            oldfile = './Database/NBDb.db'
            shutil.copyfile(oldfile, newfile)
    def download_backup(self):
        #firstly : take a backup of current basic db as temp
        if os.path.exists('./Database/NBDb.db') : 
            oldfile = './Database/NBDb.db'
            newfile = f'./Database/temp.db'
            shutil.copyfile(oldfile, newfile)
        #secondly : replace current db with downloaded backup
        filename = askopenfilename(initialdir='./Backups')
        newfile = f'./Database/NBDb.db'
        shutil.copyfile(filename, newfile)
        #3rd : copy temp as last to backup folder
        if os.path.exists("./Database/temp.db"):
            oldfile = './Database/temp.db'
            newfile = f'./Backups/last.db'
            shutil.copyfile(oldfile, newfile)
        #finaly : delete temp
            os.remove("./Database/temp.db")
    def change_pass(self):
        with sqlite3.connect("./Database/NBDb.db") as db:
            cur = db.cursor()
        cur.execute("SELECT type FROM LoginData")
        fetch_type = cur.fetchall()
        if not fetch_type ==[]:
            cur.execute("SELECT * FROM LoginData WHERE username = ? and password = ?",(self.entry1.get().strip(),self.entry2.get().strip()))
            fetch = cur.fetchall()
            if not fetch == []:
                for i in fetch:
                    if i[3] == 'مدير':
                        global changeLogin,page20
                        changeLogin = Toplevel()
                        page20 = ChangeLogin(changeLogin)
                        changeLogin.grab_set()
                        changeLogin.protocol("WM_DELETE_WINDOW", Exit)
                        changeLogin.mainloop()
                    else:
                        messagebox.showerror("خطأ","يمكن للمدير فقط الدخول إلى الصفحه")
                        self.entry1.delete(0,END)
                        self.entry2.delete(0,END)
                        self.entry1.focus()   
            else:
                messagebox.showerror("خطأ","خطأ في اسم المستخدم أو كلمة المرور")
                self.entry1.delete(0,END)
                self.entry2.delete(0,END)
                self.entry1.focus()
        else:
            #global changeLogin,page20
            changeLogin = Toplevel()
            page20 = ChangeLogin(changeLogin)
            changeLogin.grab_set()
            changeLogin.protocol("WM_DELETE_WINDOW", Exit)
            changeLogin.mainloop()    
    def login(self, Event=None):
        username = user.get()
        password = passwd.get()
        find_user = "SELECT * FROM LoginData WHERE username = ?"
        cur.execute(find_user, (self.entry1.get(),))
        results = cur.fetchall()
        if results != []:
            f = 1 if results[0][3] == 'مدير' else 0
            
            if self.entry1.get().strip() == results[0][1]:
                if self.entry2.get().strip() == results[0][2]:
                    messagebox.showinfo("نجاح", "تم تسجيل الدخول بنجاح",parent=main)
                    authorizeFlage.set(f)
                    self.entry1.delete(0, END)
                    self.entry2.delete(0, END)
                    main.withdraw()
                    global notebookTop
                    global page2
                    notebookTop = Toplevel()
                    page2 = NoteBook(notebookTop)
                    #page2.time()
                    notebookTop.protocol("WM_DELETE_WINDOW", Exit)
                    notebookTop.mainloop()
                else:
                    messagebox.showerror("Error", "كلمة المرور غير صحيحه",parent=main)
                    self.entry2.delete(0, END)
            
        else:
            messagebox.showerror("Error", "اسم المستخدم غير صحيح",parent=main)

class ChangeLogin:
    def __init__(self,top=None):
        top.geometry("530x680+425+75")
        top.resizable(0, 0)
        top.title("إدارة المستخدمين")
        top.overrideredirect(True)
        top.configure(background="#ffffff")
        #top.attributes('-topmost', 1)
        
        self.btnCancel = self.BTN(changeLogin,480,45,15,600,'#bc8d14',"#ffffff","#bc8d14","رجوع",self.Cancel)

        self.add_user = self.BTN(changeLogin,80,30,15,30,"#105da8","#ffffff","#105da8","إضافة",self.add)
        self.delete_user = self.BTN(changeLogin,80,30,15,90,"#105da8","#ffffff","#105da8","حذف",self.delete)        
        self.update_user = self.BTN(changeLogin,80,30,15,150,"#105da8","#ffffff","#105da8","تعديل",self.update)
        
        
        
        self.user_name = self.ENT(changeLogin,110,30,220,30,14,"#eeeeee","#ffffff")
        self.user_pass = self.ENT(changeLogin,110,90,220,30,14,"#eeeeee","#ffffff")
        #self.user_type = self.ENT(changeLogin,110,150,220,30,14,"lightgray","#ffffff")
    
    
        
        self.combobox_var1 = StringVar()
        self.combobox = ttk.Combobox(changeLogin, textvariable=self.combobox_var1,justify=CENTER)
        self.combobox.place(width=220,height=30,x=110,y=150)
        self.combobox.configure(font="-family tajawal -size 10 -weight bold")
        self.combobox['values']=['موظف','مدير']
        self.combobox.current(0)
    
        
        self.user_name_lbl = Label(changeLogin,text=": اسم المستخدم",background="#ffffff",foreground="#000000")
        self.user_name_lbl.configure(font="-family tajawal -size 16")
        self.user_name_lbl.place(x=355,y=27)
        
        self.user_name_lbl = Label(changeLogin,text=": كلمة المرور",background="#ffffff",foreground="#000000")
        self.user_name_lbl.configure(font="-family tajawal -size 16")
        self.user_name_lbl.place(x=355,y=87)

        self.user_name_lbl = Label(changeLogin,text=": الصلاحيه",background="#ffffff",foreground="#000000")
        self.user_name_lbl.configure(font="-family tajawal -size 16")
        self.user_name_lbl.place(x=355,y=147)
        
        # self.f1 = Frame(changeLogin,background="#000000")
        # self.f1.place(x=15,y=190,width=500,height=400)
        
        changeLogin.bind("<Return>",self.add)
    
        self.scrollbary = Scrollbar(changeLogin, orient=VERTICAL)
        self.scrollbary.place(x=495,y=190,width=20,height=400)
        self.tree = ttk.Treeview(changeLogin)
        self.tree.place(x=15,y=190,width=480,height=400)
        self.tree.configure(yscrollcommand=self.scrollbary.set)
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)


        self.tree.configure(
             columns=(
                 "type",
                 "password",
                 "user_name",
             )
         )
        self.tree.heading("user_name", text="اسم المستخدم",anchor=CENTER)
        self.tree.heading("password", text="كلمة المرور",anchor=CENTER)
        self.tree.heading("type", text="الصلاحيه",anchor=CENTER)
        
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=160,anchor=CENTER)
        self.tree.column("#2", stretch=NO, minwidth=0, width=180,anchor=CENTER)
        self.tree.column("#3", stretch=NO, minwidth=0, width=160,anchor=CENTER)
        self.display()
        
    def add(self,e=None):
        user_name = self.user_name.get().strip()
        password = self.user_pass.get().strip()
        type = self.combobox_var1.get()
        cur.execute("SELECT * FROM LoginData")
        fetchh = cur.fetchall()
        for i in fetchh:
            if i[3] == 'مدير' and type == 'مدير':
                messagebox.showerror("خطأ","يمكن إضافة مدير واحد فقط",parent=changeLogin)
                self.user_name.delete(0,END)
                self.user_pass.delete(0,END)
                self.user_name.focus()
                return
        cur.execute("SELECT * FROM LoginData WHERE username=:PN1",{'PN1' :user_name})
        fetch = cur.fetchall()
        if fetch == []:
            #if user_name:
                #if password:
                    #if len(password) >= 8 :
            insert = (
                        "INSERT INTO LoginData (username,password,type) VALUES(?,?,?)"
                    )
            cur.execute(insert,[user_name,password,type])
            db.commit()
            messagebox.showinfo("نجاح", "تمت إضافة المستخدم بنجاح",parent=changeLogin)
            self.display()
            self.user_name.delete(0,END)
            self.user_pass.delete(0,END)
            self.user_name.focus()
                    #else:
                    #    messagebox.showerror("خطأ!","كلمة المرور قصيره",parent=changeLogin)    
                    #    self.user_pass.delete(0,END)
                    #    self.user_pass.focus()
                #else:
                #    messagebox.showerror("خطأ!", "حقل كلمة المرور فارغ",parent=changeLogin)
            #else:
            #    messagebox.showerror("خطأ!", "حقل اسم المستخدم فارغ",parent=changeLogin)
        else:
            messagebox.showerror("خطأ!", "المستخدم موجود مسبقا",parent=changeLogin)

    def update(self):
        user_name = self.user_name.get().strip()
        user_pass = self.user_pass.get().strip()
        user_type = self.combobox_var1.get()
        x = self.tree.selection()
        if len(x)!=0:
            selected= self.tree.focus()
            values = self.tree.item(selected, 'values')
            if values == '' :
                return
            userid = values[2]
            update = (
                        "UPDATE LoginData SET username = ?, password = ?, type = ? WHERE username = ?"
                        )
            cur.execute(update, [user_name, user_pass, user_type, userid])
            db.commit()
            messagebox.showinfo("نجاح", "تم تعديل معلومات المستخدم بنجاح",parent=changeLogin)
            self.display()
            self.user_name.delete(0,END)
            self.user_pass.delete(0,END)
            self.user_name.focus()
        else:
            messagebox.showerror("خطأ!","قم باختيار مستخدم أولاً", parent=changeLogin)
    def delete(self):
        with sqlite3.connect("./Database/NBDb.db") as db:
            cur = db.cursor()
        user_name = self.user_name.get().strip()
        cur.execute("SELECT userid FROM LoginData WHERE username =?",(user_name,))
        fetch = cur.fetchall()
        userid = fetch[0]
        x1 = self.tree.selection()
        type_to_check = []
        for record in x1:
            type_to_check.append(self.tree.item(record,'values')[0])
        if type_to_check[0] == 'مدير':
            messagebox.showerror("خطأ","لايمكن حذف المدير",parent=changeLogin)
        else:
            sure = messagebox.askyesno("انتبه", "هل أنت متأكد من حذف المستخدم المحدد؟", parent=changeLogin)
            if sure == True:
                x = self.tree.selection()
                if len(x)!=0:
                    ids_to_delete = []
                    for record in x:
                        ids_to_delete.append(self.tree.item(record,'values')[2])
                        type_to_check.append(self.tree.item(record,'values')[0])
                    for record in x :
                        self.tree.delete(record)
                    
                    delete = "DELETE FROM LoginData WHERE userid = ?"
                    cur.execute(delete, (userid))
                    db.commit()  
                    self.display()
                    self.user_name.delete(0,END)
                    self.user_pass.delete(0,END)
                    self.user_name.focus()  
                    messagebox.showinfo("نجاح!", "تم حذف المستخدم بنجاح", parent=changeLogin)
                else:
                    messagebox.showerror("خطأ!","قم باختيار مستخدم أولاً", parent=changeLogin)
            
    def display(self):
        with sqlite3.connect("./Database/NBDb.db") as db:
            cur = db.cursor()
        cur.execute("SELECT * FROM LoginData")
        fetch = cur.fetchall()
        if fetch == []:
            self.combobox.current(1)
        else:
            self.combobox.current(0)
        self.tree.delete(*self.tree.get_children())
        for data in fetch:
            self.tree.insert("", "end", values=(data[3],data[2],data[1]))
    def BTN(self,pay_card,width,height,x,y,activebackground,foreground,background,text1,command=None):
        btn = Button(pay_card,text=text1)
        btn.place(width=width,height=height,x=x,y=y)
        btn.configure(activebackground=activebackground)
        btn.configure(relief="flat")
        btn.configure(overrelief="flat")
        btn.configure(cursor="hand2")
        btn.configure(foreground=foreground)
        btn.configure(background=background)
        btn.configure(font="-family tajawal -size 14 -weight bold")
        btn.configure(borderwidth="0")
        btn.configure(command=command)
        return btn
    
    def ENT(self,pay_card,x,y,width,height,size,bg,disabledforeground):
        ent = Entry(pay_card,borderwidth=0,justify=CENTER,bg=bg,disabledbackground=disabledforeground)
        ent.configure(justify = CENTER)
        ent.configure(font=f"-family tajawal -size {size}")
        ent.place(width=width,height=height,x=x,y=y)
        return ent
    def on_tree_select(self, e):
        self.user_name.delete(0,END)
        self.user_pass.delete(0,END)
        selected= self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values == '' :
            return
        self.user_name.insert(0,values[2])
        self.user_pass.insert(0,values[1])
        if values[0]=='موظف':
            self.combobox.current(0)
        else:
            self.combobox.current(1)
    
    def Cancel(self,e=None):
        main.focus()
        changeLogin.destroy()

class NoteBook:
    def __init__(self,top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.iconbitmap("./images/ico2.ico")
        top.title('دفتر الديون')   
        self.top = top
        self.label1 = Label(top)
        self.label1.place(x=0, y=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/notebook.png")
        self.label1.configure(image=self.img)
        self.top = top
        self.top.protocol("WM_DELETE_WINDOW", Exit) 
        self.current_selected_transaction_id = None
        self.current_selected_transaction_type= None
        self.curCus = ''
        self.add_product_btn = self.BTN(top,72,45,1139,249,"#105da8","#ffffff","#105da8","اضافة",self.add_product)
        self.delete_product_btn = self.BTN(top,72,45,1002,249,'#bc8d14',"#ffffff","#bc8d14","حذف",self.delete_transaction)
        self.edite_product_btn = self.BTN(top,72,45,1002,310,'#1782ea',"#ffffff","#1782ea","تعديل",self.update_product)
        self.init_product_btn = self.BTN(top,72,45,1139,310,'#1782ea',"#ffffff","#1782ea","تهيئة",self.product_clear_JustENT)

 
        self.add_payment_btn = self.BTN(top,72,45,1139,497,"#105da8","#ffffff","#105da8","اضافة",self.add_payment)
        self.delete_payment_btn = self.BTN(top,72,45,1002,497,'#bc8d14',"#ffffff","#bc8d14","حذف",self.delete_transaction)
        self.edite_payment_btn = self.BTN(top,72,45,1002,558,'#1782ea',"#ffffff","#1782ea","تعديل",self.update_payment)
        self.init_payment_btn = self.BTN(top,72,45,1139,558,'#1782ea',"#ffffff","#1782ea","تهيئة",self.payment_clear_JustENT)
        

        self.calc_btn = self.BTN(top,105,45,560,645,'#1782ea',"#ffffff","#1782ea","جمع",self.calculate)
        self.back_btn = self.BTN(top,105,45,1055,645,"#121212","#ffffff","#121212","عودة",self.GoBack)
        self.Print_pdf_btn = self.BTN(top,180,45,360,645,'#1782ea',"#ffffff","#1782ea","PDF طباعة إلى ",self.Print_to_pdf)
        self.delete_cus_btn = self.BTN(top,180,45,160,645,'#1782ea',"#ffffff","#bc8d14","حذف حساب الزبون",self.delete_customer)
        self.select_cus_btn = self.BTN(top,100,45,685,645,'#1782ea',"#ffffff","#bc8d14","الزبائن",self.GoCustomersView)
        self.new_bill_btn = self.BTN(top,20,20,45,45,'#1782ea',"#ffffff","#bc8d14","+",self.new_bill)
        self.e2 = Listbox(top)
        
        self.customer_name_ent = self.ENT(top,600,117,265,20,12)
        self.customer_phone_ent = self.ENT(top,100,117,265,20,12)
        
        self.product_name_ent = self.ENT(top,941,108,337,20,12)
        self.quant_ent = self.ENT(top,1137,198,141,17,12)
        self.singl_price_ent = self.ENT(top,946,198,141,17,12)
        
        self.payment_cash_ent = self.ENT(top,941,439,337,22,12)
        
        self.tree = ttk.Treeview(top)
        self.scrollbary = Scrollbar(top)        
    
                
        self.count = 0
        self.remain=0
        self.theirsTotal=0
        self.oursTotal=0

            

        self.customer_name_ent.delete(0,END)
        self.customer_phone_ent.delete(0,END)
               
        self.create_tree()
        self.customer_name_ent.bind('<Down>',self.down2)
        self.customer_name_ent.bind('<KeyRelease>',self.lstbx2)
        self.customer_name_ent.bind('<Return>',self.add_customer)
        self.customer_phone_ent.bind('<Return>',self.add_customer)
        
        self.var1=IntVar()
        self.var1.set(0)
        self.chkreturn = Checkbutton(top,variable=self.var1)
        self.chkreturn.place(x=920, y=400)
        self.returnTxt = Label(top,text=':مرتجع',bg='#ffffff',font='-family tajawal -size 12 -weight bold')
        self.returnTxt.place(x=950, y=400)
        self.quant_ent.bind('<Return>',self.add_product)
        self.singl_price_ent.bind('<Return>',self.add_product)
        self.product_name_ent.bind('<Return>',self.add_product)
        self.tree.bind('<Delete>',self.delete_transaction)
        self.payment_cash_ent.bind('<Return>',self.add_payment) 
        self.product_btn_dis()
        self.payment_btn_dis()
        self.pdf = FPDF()
        self.customer_name_ent.focus()
        
    def new_bill(self):
        global tempBillTop,page5
        tempBillTop = Toplevel()
        page5 = BillCreator(tempBillTop)
        tempBillTop.grab_set()
        tempBillTop.protocol("WM_DELETE_WINDOW", Exit)
        tempBillTop.mainloop()
    def GoCustomersView(self):
        global CustomerViewTop,page3
        CustomerViewTop = Toplevel()
        page3 = CustomerView(CustomerViewTop)
        CustomerViewTop.grab_set()
        CustomerViewTop.protocol("WM_DELETE_WINDOW", Exit)
        CustomerViewTop.mainloop()
    def select_cus(self):
        self.customer_name_ent.delete(0,END)
        self.customer_phone_ent.delete(0,END)
        self.customer_name_ent.insert(0,current_selected_customer_name.get().strip())
        self.customer_phone_ent.insert(0,current_selected_customer_phone.get().strip())
        self.curCus = self.customer_name_ent.get().strip()
        self.Display_Data()
    def delete_customer(self):
        sure1 = messagebox.askyesno('تنبيه','هل أنت متأكد من أنك تريد حذف كامل ملف الزبون؟',parent= self.top)
        if sure1 == True:
            sure2 = messagebox.askyesno('تنبيه','يجب التأكيد على ذلك مرة ثانية',parent= self.top)
            if sure2 == True:
                query1 = 'delete from transactions WHERE customer_name == ?'
                cur.execute(query1,(self.curCus,))
                query2 = 'delete from customers WHERE customer_name == ?'
                cur.execute(query2,(self.curCus,))
                db.commit()
                messagebox.showinfo('تنبيه',f'تم حذف ملف الزبون {self.curCus}',parent= self.top)
                self.customer_name_ent.delete(0,END)
                self.customer_phone_ent.delete(0,END)
                self.curCus = ''
                self.Display_Data()
    def create_tree(self):
        s = ttk.Style()
        s.configure('Treeview', rowheight=30)
        self.f1 = Frame(self.top)
        self.f1.place(x=75,y=185,width=776,height=432)
        self.scrollbary = Scrollbar(self.top, orient=VERTICAL)
        self.tree = ttk.Treeview(self.f1)
        self.tree.place(relx=0,rely=0,width=776,height=432)
        self.tree.configure(yscrollcommand=self.scrollbary.set)
        self.tree.configure(selectmode="extended")
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbary.place(x=855,y=185, width=18, height=432)
        self.tree.configure(
            columns=(
                "theirs",
                "ours",
                "sale_price",
                "quantity",
                "transaction_time",
                "transaction_day",
                "transaction_date",
                "transaction_type",
                "transaction_name",
                "tslsl",
                "transaction_id",
                
                
            )
        )
        self.tree.heading("theirs", text="له",anchor=CENTER)
        self.tree.heading("ours", text="الإجمالي",anchor=CENTER)
        self.tree.heading("sale_price", text="السعر",anchor=CENTER)
        self.tree.heading("quantity", text="كمية",anchor=CENTER)
        self.tree.heading("transaction_time", text="وقت",anchor=CENTER)
        self.tree.heading("transaction_day", text="يوم",anchor=CENTER)
        self.tree.heading("transaction_date", text="تاريخ",anchor=CENTER)
        self.tree.heading("transaction_type", text="نوع",anchor=CENTER)
        self.tree.heading("transaction_name", text="البيان",anchor=CENTER)
        self.tree.heading("tslsl", text="#",anchor=CENTER)
        self.tree.heading("transaction_id", text="##",anchor=CENTER)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=90,anchor=CENTER)
        self.tree.column("#2", stretch=NO, minwidth=0, width=90,anchor=CENTER)
        self.tree.column("#3", stretch=NO, minwidth=0, width=80,anchor=CENTER)
        self.tree.column("#4", stretch=NO, minwidth=0, width=60,anchor=CENTER)
        self.tree.column("#5", stretch=NO, minwidth=0, width=60,anchor=CENTER)
        self.tree.column("#6", stretch=NO, minwidth=0, width=60,anchor=CENTER)
        self.tree.column("#7", stretch=NO, minwidth=0, width=100,anchor=CENTER)
        self.tree.column("#8", stretch=NO, minwidth=0, width=60,anchor=CENTER)
        self.tree.column("#9", stretch=NO, minwidth=0, width=150,anchor=CENTER)
        self.tree.column("#10", stretch=NO, minwidth=0, width=25,anchor=CENTER)
        self.tree.column("#11", stretch=NO, minwidth=0, width=5,anchor=CENTER)

        self.tree.tag_configure('sale', background = "#ffffff",font='-family tajawal -size 11')
        self.tree.tag_configure('brief', background = "#de9999",font='-family tajawal -size 11')
        self.tree.tag_configure('billTot', background = "#d2d297",font='-family tajawal -size 11')
        self.tree.tag_configure('remain', background = "#7ef9fb",font='-family tajawal -size 11') #aaffaa
        self.tree.tag_configure('payment', background = "#fcdd64",font='-family tajawal -size 11')
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
    
    def add_product(self,e=None):
        cusName = self.curCus
        if cusName.strip():
            cur.execute('SELECT customer_phone from customers WHERE customer_name = ?',(cusName,))
            fet= cur.fetchone()
            if fet == None :
                messagebox.showerror('خطأ', 'تأكد من اسم الزبون',parent = self.top)
                self.customer_name_ent.focus()
                return 
            if self.product_name_ent.get().strip():
                if self.quant_ent.get().strip():
                    if self.singl_price_ent.get().strip():
                        try:
                            transPrice = float(self.singl_price_ent.get().strip())
                            transQuantity = float(self.quant_ent.get().strip())
                        except ValueError :
                            messagebox.showerror('خطأ', 'قيم غير صحيحة',parent = self.top)
                            return
                        
                        transName=self.product_name_ent.get().strip()
                        transDate = date.today()
                        transTime = datetime.now().strftime("%H:%M")
                        cur.execute('SELECT max(transaction_id) from transactions')
                        sel= cur.fetchone()
                        transId = sel[0]+1 if sel[0] != None else 1
                        cur.execute("INSERT INTO transactions VALUES (:transaction_id ,:customer_name,:transaction_name,:transaction_type ,:transaction_date ,:transaction_time,:quantity,:sale_price,:Ours,:Theirs)",
                                                                    {
                                                                        'transaction_id':transId ,
                                                                        'customer_name': cusName,
                                                                        'transaction_name':transName  ,
                                                                        'transaction_type':'بيع' ,
                                                                        'transaction_date': transDate,
                                                                        'transaction_time': transTime ,
                                                                        'quantity' : transQuantity  ,
                                                                        'sale_price':transPrice ,
                                                                        'Ours' : float(transPrice)*float(transQuantity) ,
                                                                        'Theirs': 0.0
                                                                    })
                        db.commit()
                        self.Display_Data()
                        self.product_clear_JustENT()
                        self.product_name_ent.focus()
                    else:
                        messagebox.showerror('خطأ', 'أدخل السعر',parent = self.top)
                        self.singl_price_ent.focus()
                else:
                    messagebox.showerror('خطأ', 'أدخل الكمية',parent = self.top)
                    self.quant_ent.focus()
            else:
                messagebox.showerror('خطأ', 'أدخل اسم المنتج',parent = self.top)
                self.product_name_ent.focus()
        else:
            messagebox.showerror('خطأ', 'أدخل اسم الزبون أولاً',parent = self.top)
            self.customer_name_ent.focus()    

    def update_product(self):
        
        if self.current_selected_transaction_type == 'بيع' :
            cusName = self.curCus
            if cusName.strip():
                cur.execute('SELECT customer_phone from customers WHERE customer_name = ?',(cusName,))
                fet= cur.fetchone()
                if fet == None :
                    messagebox.showerror('خطأ', 'تأكد من اسم الزبون',parent = self.top)
                    self.customer_name_ent.focus()
                    return 
                if self.product_name_ent.get().strip():
                    if self.quant_ent.get().strip():
                        if self.singl_price_ent.get().strip():
                            try:
                                transPrice = float(self.singl_price_ent.get().strip())
                                transQuantity = float(self.quant_ent.get().strip())
                            except ValueError :
                                messagebox.showerror('خطأ', 'قيم غير صحيحة',parent = self.top)
                                return
                            
                            update = (
                                            "UPDATE transactions SET sale_price = ?, quantity = ?,Ours = ?  WHERE transaction_id = ?"
                                            )
                            cur.execute(update, (transPrice, transQuantity,transPrice*transQuantity,self.current_selected_transaction_id))
                            db.commit()
                            self.Display_Data()
                            self.product_clear_JustENT()
                            self.product_name_ent.focus()
                            self.product_btn_dis()
                        else:
                            messagebox.showerror('خطأ', 'أدخل السعر',parent = self.top)
                            self.singl_price_ent.focus()
                    else:
                        messagebox.showerror('خطأ', 'أدخل الكمية',parent = self.top)
                        self.quant_ent.focus()
                else:
                    messagebox.showerror('خطأ', 'أدخل اسم المنتج',parent = self.top)
                    self.product_name_ent.focus()
            else:
                messagebox.showerror('خطأ', 'قم بإدخال اسم الزبون أولاً',parent = self.top)
                self.customer_name_ent.focus()    
    def product_clear_JustENT(self):
        self.product_name_ent.delete(0,END)
        self.quant_ent.delete(0,END)
        self.singl_price_ent.delete(0,END)
    
    def add_payment(self,e=None):
        cusName = self.curCus
        if cusName.strip():
            cur.execute('SELECT customer_phone from customers WHERE customer_name = ?',(cusName,))
            fet= cur.fetchone()
            if fet == None :
                messagebox.showerror('خطأ', 'تأكد من اسم الزبون',parent = self.top)
                self.customer_name_ent.focus()
                return 
            if self.payment_cash_ent.get().strip():
                try:
                    payment_cash = float(self.payment_cash_ent.get().strip())
                except ValueError :
                    messagebox.showerror('خطأ', 'قيمة الدفعة غير صحيحة',parent = self.top)
                    return
                if self.var1.get()== 0:
                    transName='دفعة عالحساب'
                    transType ='دفعة'
                else:
                    transName='مرتجع فاتورة'
                    transType ='مرتجع'
                transDate = date.today()
                transTime = datetime.now().strftime("%H:%M")
                cur.execute('SELECT max(transaction_id) from transactions')
                sel= cur.fetchone()
                transId = sel[0]+1 if sel[0] != None else 1
                cur.execute("INSERT INTO transactions VALUES (:transaction_id ,:customer_name,:transaction_name,:transaction_type ,:transaction_date ,:transaction_time,:quantity,:sale_price,:Ours,:Theirs)",
                                                            {
                                                                'transaction_id':transId ,
                                                                'customer_name': cusName,
                                                                'transaction_name':transName  ,
                                                                'transaction_type':transType ,
                                                                'transaction_date': transDate,
                                                                'transaction_time': transTime ,
                                                                'quantity' : ''  ,
                                                                'sale_price':'' ,
                                                                'Ours' : 0.0 ,
                                                                'Theirs': float(payment_cash) 
                                                            })
                db.commit()
                self.Display_Data()
            else:
                messagebox.showerror('خطأ', 'أدخل قيمة الدفعة',parent = self.top)
                self.payment_cash_ent.focus()
        else:
            messagebox.showerror('خطأ', 'قم بإدخال اسم الزبون أولاً',parent = self.top)
            self.customer_name_ent.focus()    
    def update_payment(self):
        if self.var1.get()== 0:
                    transName='دفعة عالحساب'
                    transType ='دفعة'
        else:
            transName='مرتجع فاتورة'
            transType ='مرتجع'
        if self.current_selected_transaction_type != 'بيع' :
            cusName = self.curCus
            if cusName.strip():
                cur.execute('SELECT customer_phone from customers WHERE customer_name = ?',(cusName,))
                fet= cur.fetchone()
                if fet == None :
                    messagebox.showerror('خطأ', 'تأكد من اسم الزبون',parent = self.top)
                    self.customer_name_ent.focus()
                    return 
                if self.payment_cash_ent.get().strip():
                    try:
                        trans_cash = float(self.payment_cash_ent.get().strip())
                    except ValueError :
                        messagebox.showerror('خطأ', 'قيمة دفعة/مرتجع غير صحيحة',parent = self.top)
                        return
                    
                    update = (
                                    "UPDATE transactions SET Theirs = ?,transaction_type=?,transaction_name=? WHERE transaction_id = ?"
                                    )
                    cur.execute(update, (trans_cash,transType,transName,self.current_selected_transaction_id))
                    db.commit()
                    self.Display_Data()
                    self.product_name_ent.focus()
                else:
                    messagebox.showerror('خطأ', 'أدخل قيمة دفعة/مرتجع صحيحة',parent = self.top)
                    self.payment_cash_ent.focus()
            else:
                messagebox.showerror('خطأ', 'قم بإدخال اسم الزبون أولاً',parent = self.top)
                self.customer_name_ent.focus() 
    def payment_clear_JustENT(self):
        self.payment_cash_ent.delete(0,END)
    def delete_transaction(self,e=None):
        if self.current_selected_transaction_type == 'بيع' :
            msg = 'هل تريد بالتأكيد حذف المنتج المحدد من الفاتورة؟'
        elif self.current_selected_transaction_type == 'دفعة':
            msg = 'هل تريد بالتأكيد حذف الدفعة المحددة؟؟'
        elif self.current_selected_transaction_type == 'مرتجع':
            msg = 'هل تريد بالتأكيد حذف المرتجع المحدد؟؟'
        else:
            return
        sure = messagebox.askyesno('تنبيه',msg,parent=self.top)
        if sure :
            delete = "DELETE FROM transactions WHERE transaction_id = ?"
            cur.execute(delete,(self.current_selected_transaction_id,))
            db.commit()
        self.Display_Data()
    def Display_Data(self):
        if self.tree.winfo_exists():
            cur.execute("SELECT * FROM transactions WHERE customer_name == ?",(self.curCus,))
            fetch = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            tslsl=0
            payment_tslsl=0
            self.oursTotal=0
            LocaloursTotal = 0
            self.theirsTotal=0
            self.remain=0
            
            for data in fetch:

                if data[3]=='بيع':
                    tslsl+=1
                    self.tree.insert("", "end",tags='sale' ,values=(data[9],data[8],data[7],data[6],data[5],num2day(str(data[4])),data[4],data[3],data[2],tslsl,data[0]))
                    self.oursTotal+=data[8]
                    LocaloursTotal+=data[8]
                else:
                    payment_tslsl+=1
                    tslsl=0
                    if LocaloursTotal!=0 :
                        self.tree.insert("", "end",tags='billTot', values=('',LocaloursTotal,'','','','','','','مجموع فاتورة','',None))
                    self.tree.insert("", "end",tags='payment',values=(data[9],LocaloursTotal+self.remain,'-','-',data[5],num2day(str(data[4])),data[4],data[3],data[2],payment_tslsl,data[0]))
                    

                    self.theirsTotal+=data[9]
                    self.remain=self.oursTotal-self.theirsTotal
                    
                    if self.remain < 0 :
                        self.tree.insert("", "end",tags='remain',values=(abs(self.remain),0,'','','','','','-','باقي الحساب','',None))
                    elif self.remain > 0 :
                        self.tree.insert("", "end",tags='remain',values=(0,self.remain,'','','','','','-','باقي الحساب','',None))
                    else:
                        self.tree.insert("", "end",tags='remain',values=(0,0,'','','','','','-','باقي الحساب','',None))
                    LocaloursTotal=0
        self.current_selected_transaction_type=None
        self.product_btn_dis()
        self.payment_btn_dis()
        self.payment_clear_JustENT()
        self.product_clear_JustENT()
    def calculate(self):
        if self.curCus :
            cur.execute("SELECT sum(Ours),sum(Theirs) FROM transactions WHERE customer_name == ?",(self.curCus,))
            fetch = cur.fetchone()
            oursTotal=float(fetch[0]) if fetch[0] != None else 0
            theirsTotal=float(fetch[1]) if fetch[1] != None else 0
            remain = oursTotal - theirsTotal
            self.tree.insert("", "end",tags='brief',values=(theirsTotal,oursTotal,'-','-','-','-','-','-','ملخص الحساب الكلي','',None))
            if remain < 0 :
                self.tree.insert("", "end",tags='remain',values=(abs(remain),0,'-','-','-','-','-','-','باقي الحساب','',None))
            elif remain > 0 :
                self.tree.insert("", "end",tags='remain',values=(0.0,remain,'-','-','-','-','-','-','باقي الحساب','',None))
            else:
                self.tree.insert("", "end",tags='remain',values=(0.0,0.0,'-','-','-','-','-','-','باقي الحساب','',None))
    def on_tree_select(self,e):
        selected= self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values == '' :
            return
        self.current_selected_transaction_id = values[10]
        self.current_selected_transaction_type=values[7]
        if values[7]=='بيع':    
            self.product_btn_ena()
            self.payment_btn_dis()
            self.product_name_ent.delete(0,END)
            self.quant_ent.delete(0,END)
            self.singl_price_ent.delete(0,END)
            self.payment_cash_ent.delete(0,END)
            self.product_name_ent.insert(0,values[8])
            self.quant_ent.insert(0,float(values[3]))
            self.singl_price_ent.insert(0,values[2])
        elif values[7] == 'دفعة' or  values[7] == 'مرتجع':
            self.product_btn_dis()
            self.payment_btn_ena()
            self.product_name_ent.delete(0,END)
            self.quant_ent.delete(0,END)
            self.singl_price_ent.delete(0,END)
            self.payment_cash_ent.delete(0,END)
            self.payment_cash_ent.insert(0,values[0])
            
        else:
            self.product_btn_dis()
            self.payment_btn_dis()
            self.Display_Data()
            self.product_clear_JustENT()
            self.payment_clear_JustENT()
            self.current_selected_transaction_id=None
            self.current_selected_transaction_type=None
            return
        if authorizeFlage.get() == 0 :     #Optional[1]
            self.payment_btn_dis()
            self.product_btn_dis()
    def product_btn_dis(self,e=None):
        self.delete_product_btn.configure(state=DISABLED)
        self.edite_product_btn.configure(state=DISABLED)
    def product_btn_ena(self,e=None):
        self.delete_product_btn.configure(state=NORMAL)
        self.edite_product_btn.configure(state=NORMAL)
    def payment_btn_dis(self,e=None):
        self.delete_payment_btn.configure(state=DISABLED)
        self.edite_payment_btn.configure(state=DISABLED)
    def payment_btn_ena(self,e=None):
        self.delete_payment_btn.configure(state=NORMAL)
        self.edite_payment_btn.configure(state=NORMAL)
    def a2(self,e):
        self.customer_name_ent.delete(0,END)
        self.customer_phone_ent.delete(0,END)
        for i in self.e2.curselection():
            self.customer_name_ent.insert(0,self.e2.get(i))
            self.e2.destroy()
        self.curCus=self.customer_name_ent.get().strip()
        cur.execute("SELECT customer_phone FROM customers WHERE customer_name like ?",(self.curCus,))
        fetch = cur.fetchone()
        self.customer_phone_ent.insert(0,fetch[0])
        db.commit()
        self.Display_Data()
        self.product_name_ent.focus()
    def lstbx2(self,e):
        if self.e2.winfo_exists():
            self.e2.destroy()
            
        if  self.customer_name_ent.get().strip():
            self.e2 = Listbox(
            self.top,
            width=20,
            activestyle=None,
            height=5,
            selectmode=SINGLE,
            justify=RIGHT,
            border=0,
            cursor='arrow',
            selectbackground='#ffffff',
            selectforeground='#105da8',
            font=('tajawal 15'))
            self.e2.place(x=600,y=140,width=265,height=85)
            lookup_record = self.customer_name_ent.get().strip()

            if not lookup_record.strip() and self.e2.winfo_exists():
                self.e2.destroy()
            else:
                ss='%'+lookup_record+'%'
                cur.execute("SELECT * FROM customers WHERE customer_name like ?",(ss,))
                fetch = cur.fetchall()
                if fetch==[]:
                    message1 = 'زبون جديد! أدخل الاسم والرقم واضغط انتر'
                    self.e2.insert(END,message1)
                    self.e2.configure(font='tajawal 10')
                    self.e2.configure(justify=CENTER)
                    self.e2.configure(foreground='#bc8d14')
                    self.customer_phone_ent.delete(0,END)
                else:
                    for h in fetch:
                        self.e2.insert(END,h[1])
                    db.commit()
            if self.e2.winfo_exists():    
                self.e2.bind('<Double-1>',self.a2)
                self.e2.bind('<Return>',self.a2)
                self.e2.bind('<Down>',self.down2)
                self.e2.bind('<Up>',self.up2)
            self.customer_name_ent.bind("<Down>",self.fromE2L2)
        else:
            if self.e2.winfo_exists():
                self.e2.destroy()
    def fromE2L2(self,e):
        if self.e2.winfo_exists(): 
            self.count = 0
            self.e2.focus()
            self.count= self.e2.index(ANCHOR)
            x= self.e2.index(ACTIVE)
            self.e2.selection_clear(0,END)
            self.e2.selection_set(x)
    def down2(self,e):
        if self.e2.winfo_exists():
            if self.e2.index(ACTIVE)+1 < self.count :
                self.e2.selection_clear(0,END)
                self.e2.selection_set(self.e2.index(ACTIVE)+1)
    def up2(self,e):
        if self.e2.index(ACTIVE) > 0 :
            self.e2.selection_clear(0,END)
            self.e2.selection_set(self.e2.index(ACTIVE)-1)    
        else:
            self.customer_name_ent.focus()
            self.e2.destroy()
    def add_customer(self,e):
        if not self.customer_name_ent.get().strip():
            messagebox.showwarning("تحذير!","ادخل اسم الزبون",parent=self.top)
            self.customer_name_ent.delete(0,END)
            self.customer_name_ent.focus()
            return
        else:
            if not self.customer_phone_ent.get().strip():
                messagebox.showwarning("تحذير!","ادخل العنوان",parent=self.top)
                self.customer_phone_ent.delete(0,END)
                self.e2.destroy()
                self.customer_phone_ent.focus()
                return
            else:   
                cur.execute("SELECT * FROM customers WHERE customer_name=:PN1",{'PN1' : self.customer_name_ent.get().strip() ,'PN2':self.customer_phone_ent.get()  })
                fetch = cur.fetchall()
                if fetch == []:
                    cur.execute("select max(customer_id) from customers")
                    fetch1 = cur.fetchone() 
                    conter =int(fetch1[0])+1 if fetch1[0]!=None else 0
                    cur.execute("INSERT INTO customers VALUES ( :customer_id,:customer_name , :customer_phone)",
                                {
                                    'customer_id': conter,       
                                    'customer_name':self.customer_name_ent.get().strip(),
                                    'customer_phone': self.customer_phone_ent.get().strip()  
                                } )
                    db.commit()
                    messagebox.showwarning("","تم إضافة الزبون",parent=self.top)
                    self.e2.destroy()
                    self.curCus=self.customer_name_ent.get().strip()
                    self.Display_Data()
                    self.product_name_ent.focus()

                else:
                    messagebox.showwarning("تحذير!","اسم الزبون\العنوان الذي أدخلته موجود مسبقاً",parent=self.top)
    def GoBack(self):
        self.top.destroy()
        main.deiconify()

    def BTN(self,pay_card,width,height,x,y,activebackground,foreground,background,text1,command=None):
        btn = Button(pay_card,text=text1)
        btn.place(width=width,height=height,x=x,y=y)
        btn.configure(activebackground=activebackground)
        btn.configure(relief="flat")
        btn.configure(overrelief="flat")
        btn.configure(cursor="hand2")
        btn.configure(foreground=foreground)
        btn.configure(background=background)
        btn.configure(font="-family tajawal -size 14 -weight bold")
        btn.configure(borderwidth="0")
        btn.configure(command=command)
        return btn
    def ENT(self,root,x,y,width,height,size):
        ent = Entry(root,borderwidth=0,justify=CENTER)
        ent.configure(font=f"-family tajawal -size {size}")
        ent.place(width=width,height=height,x=x,y=y)
        return ent
    
    def create_table(self,table_data, title='', data_size = 12, title_size=12, align_data='C', align_header='C', cell_width='uneven', x_start='x_default',emphasize_data=[], emphasize_style=None, emphasize_color=(255,0,0)):
        default_style = self.pdf.font_style
        if emphasize_style == None:
            emphasize_style = default_style

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                print(data[0],len(data[0]))
                col_width = self.pdf.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = [20,20,20,20,30,80]

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.pdf.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                col_width = col_widths
                


                        ### compare columns 

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int        
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.pdf.font_size * 1.5

        col_width = get_col_widths()
        self.pdf.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from self.pdf width and divide by 2 (margins)
            margin_width = self.pdf.w - table_width
            # TODO: Check if table_width is larger than self.pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.pdf.set_x(x_start)
        elif isinstance(x_start, int):
            self.pdf.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.pdf.set_x(self.pdf.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.pdf.set_font_size(16)
            
            self.pdf.multi_cell(0, line_height, title, border=0, align='C', ln=3, max_line_height=self.pdf.font_size)
            self.pdf.set_font_size(self.pdf.font_size)
            self.pdf.ln(5)
            self.pdf.ln(line_height) # move cursor back to the left margin

        self.pdf.set_font(size=data_size)
        # add header
        y1 = self.pdf.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.pdf.get_x()
        x_right = self.pdf.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.pdf.set_x(x_start)
            for datum in header:
                self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.pdf.font_size)
                x_right = self.pdf.get_x()
            self.pdf.ln(line_height) # move cursor back to the left margin
            y2 = self.pdf.get_y()
            self.pdf.line(x_left,y1,x_right,y1)
            self.pdf.line(x_left,y2,x_right,y2)

            for row in data:
                if self.pdf.get_y() > 240 : 
                    self.pdf.ln()
                    self.pdf.line(x_left,self.pdf.get_y(),x_right,self.pdf.get_y())
                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
                    self.pdf.cell(0,10,f' {self.pdf.page_no()} {ar_display("صفحة")}',align='R',)    
                    self.pdf.ln()
                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=12)

                    self.pdf.add_page()
                if x_start: # not sure if I need this
                    self.pdf.set_x(x_start)
                if data.index(row) > len(data)-3 and data.index(row)      :
                    self.pdf.line(10,self.pdf.get_y(),self.pdf.w-10,self.pdf.get_y())
                    
                for datum in row:
                    if datum in emphasize_data:
                        self.pdf.set_text_color(*emphasize_color)
                        self.pdf.set_font(style=emphasize_style)
                        self.pdf.multi_cell(col_width, line_height, str(datum), border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size)
                        self.pdf.set_text_color(0,0,0)
                        self.pdf.set_font(style=default_style)
                    else:
                        self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self.pdf
                self.pdf.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.pdf.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.pdf.font_size)
                x_right = self.pdf.get_x()
            self.pdf.ln(line_height) # move cursor back to the left margin
            y2 = self.pdf.get_y()
            self.pdf.line(x_left,y1,x_right,y1)
            self.pdf.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if self.pdf.get_y() > 240 : 
                    self.pdf.ln()
                    self.pdf.line(x_left,self.pdf.get_y(),self.pdf.w-5,self.pdf.get_y())
                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
                    self.pdf.cell(0,10,f' {self.pdf.page_no()} {ar_display("صفحة")}',align='R',)    
                    self.pdf.ln()

                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=12)

                    self.pdf.add_page()
                if x_start:
                    self.pdf.set_x(x_start)
                row = data[i]
                self.pdf.line(10,self.pdf.get_y(),self.pdf.w-10,self.pdf.get_y())
                for j in range(len(row)):
                    datum = str(row[j])
                    if not isinstance(datum, str):
                        datum = datum
                    adjusted_col_width = col_width[j]
                    if i > len(data)-3      :
                        self.pdf.set_text_color(*emphasize_color)
                        self.pdf.set_font(style=emphasize_style)
                        self.pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size)
                        self.pdf.set_text_color(0,0,0)
                        self.pdf.set_font(style=default_style)
                    else:
                        self.pdf.multi_cell(adjusted_col_width, line_height, str(datum), border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self.pdf
                        
                        
                self.pdf.ln(line_height) # move cursor back to the left margin
        y3 = self.pdf.get_y()
        self.pdf.line(x_left,y3,x_right,y3)
    def Print_to_pdf(self):
        if not self.curCus:
            messagebox.showerror('خطأ','قم باختيار زبون أولاً',parent= self.top)
            return
        cus_name = self.curCus
        query= 'select Theirs,Ours,sale_price,quantity,transaction_date,transaction_name from transactions WHERE customer_name = ?'
        cur.execute(query,(cus_name,))
        data1 = cur.fetchall()
        data1.insert(0,('له','سعر إجمالي','سعر إفرادي','الكمية','التاريخ','البيان'))
        data1=[list(a) for a in data1]
        query2 = 'select SUM(Theirs),SUM(Ours) from transactions WHERE customer_name = ?'
        cur.execute(query2,(cus_name,))
        totals = cur.fetchone()
        theirs = totals[0]
        ours =  totals[1]
        word1 = 'المجموع'
        word2 = 'الباقي'
        result = [theirs,ours,'-','-','-',word1]
        remain = theirs - ours
        if remain < 0 :
            remainlst =['0.0',abs(remain),'-','-','-',word2]
        else :
            remainlst = [remain,'0.0','-','-','-',word2] 
        data1.append(result)
        data1.append(remainlst)
        for i in range(len(data1)) :
            for j in range(6):
                if data1[i][j]=='  ':
                    data1[i][j] = '-' 
                data1[i][j] = ar_display(data1[i][j])
        

        
        pdfCreationDate = str(date.today())

        tit = ar_display(f'كشف حساب السيد {cus_name} حتى تاريخ {pdfCreationDate}')
        self.pdf = FPDF()
        self.pdf.alias_nb_pages()
        self.pdf.add_font("NotoSansArabic_ExtraCondensed-Regular", style="", fname="./fonts/NotoSansArabic_ExtraCondensed-Regular.ttf")
        #self.pdf.add_font('Tajawal-Regular',style='',fname='Tajawal-Regular.ttf',)
        self.pdf.add_page()
        self.pdf.ln(5)
        self.pdf.image('./images/bill1.png',1,5,self.pdf.w)
        self.pdf.line(10,55,self.pdf.w-10,55)
        self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
        self.pdf.cell(0,10,'',align='L')
        self.pdf.ln()
        self.pdf.cell(0,10,'',align='L')
        self.pdf.ln(40)
        self.create_table(table_data = data1,title=tit, cell_width='uneven')
        self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
        self.pdf.cell(0,10,f' {self.pdf.page_no()} {ar_display("صفحة")}',align='R',)  
        self.pdf.ln()
        wordtype = ' كشف حساب '
        justname = f'{wordtype}{cus_name}{pdfCreationDate}'
        path = asksaveasfilename(initialfile=justname, initialdir='./pdfs')
        if path.strip():
            self.pdf.output(f'{path}.pdf')
class CustomerView:
    def __init__(self,top=None):
        top.geometry("530x680+425+75")
        top.resizable(0, 0)
        top.title("استعراض الزبائن")
        top.overrideredirect(True)
        top.configure(background="#ffffff")
        #top.attributes('-topmost', 1)
        self.top = top
        self.btnCancel = self.BTN(self.top,480,45,15,600,'#bc8d14',"#ffffff","#bc8d14","رجوع",self.Cancel)        

        #self.user_name = self.ENT(self.top,110,30,220,30,14,"#eeeeee","#ffffff")
        
        self.title = Label(self.top,text="دليل الزبائن",background="#105da8",foreground="#ffffff")
        self.title.configure(font="-family tajawal -size 24")
        self.title.place(x=0,y=30,width=530)
        
        self.totaldebt = Label(self.top,text="",background="#ffffff",foreground="#00ff00")
        self.totaldebt.configure(font="-family tajawal -size 12")
        self.totaldebt.place(x=20,y=50,width=100)

        self.scrollbary = Scrollbar(self.top, orient=VERTICAL)
        self.scrollbary.place(x=497,y=100,width=20,height=490)
        self.tree = ttk.Treeview(self.top)
        self.tree.place(x=15,y=100,width=480,height=490)
        self.tree.configure(yscrollcommand=self.scrollbary.set)
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.select_customer)

        self.scrollbary.configure(command=self.tree.yview)
        self.tree.configure(
             columns=(
                 "debt",
                 "customer_phone",
                 "customer_name",
                 "tslsl",
             )
         )
        self.tree.heading("debt", text="لنا",anchor=CENTER)
        self.tree.heading("customer_phone", text="العنوان",anchor=CENTER)
        self.tree.heading("customer_name", text="اسم الزبون",anchor=CENTER)
        self.tree.heading("tslsl", text="#",anchor=CENTER)
        
        
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=120,anchor=CENTER)
        self.tree.column("#2", stretch=NO, minwidth=0, width=160,anchor=CENTER)
        self.tree.column("#3", stretch=NO, minwidth=0, width=180,anchor=CENTER)
        self.tree.column("#4", stretch=NO, minwidth=0, width=20,anchor=CENTER)
        self.tree.tag_configure('finish', background = "#ffffff")
        self.tree.tag_configure('continue', background = "#deaaaa")

        self.display()
    def select_customer(self,e=None):
        CustomerViewTop.destroy()
        NoteBook.select_cus(page2) 
    def display(self):
        with sqlite3.connect("./Database/NBDb.db") as db:
            cur = db.cursor()
        cur.execute("SELECT * FROM customers")
        fetch = cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        tslsl = 0
        tot=0
        for data in fetch:
            tslsl += 1
            cur.execute("SELECT SUM(Ours),SUM(Theirs) FROM transactions where customer_name == ? ",(data[1],))
            res=cur.fetchone()
            dif=float(res[0])-float(res[1]) if res[0]!= None else 0
            tot = tot+dif
            tag = 'finish' if dif == 0 else 'continue' 
            self.tree.insert("", "end",tags=tag, values=(dif,data[2],data[1],tslsl))

        self.totaldebt.configure(text=str(tot)) 
    def BTN(self,pay_card,width,height,x,y,activebackground,foreground,background,text1,command=None):
        btn = Button(pay_card,text=text1)
        btn.place(width=width,height=height,x=x,y=y)
        btn.configure(activebackground=activebackground)
        btn.configure(relief="flat")
        btn.configure(overrelief="flat")
        btn.configure(cursor="hand2")
        btn.configure(foreground=foreground)
        btn.configure(background=background)
        btn.configure(font="-family tajawal -size 14 -weight bold")
        btn.configure(borderwidth="0")
        btn.configure(command=command)
        return btn

    def on_tree_select(self, e):
        selected= self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values == '' :
            return
        current_selected_customer_name.set(values[2])

        current_selected_customer_phone.set(values[1])
    def Cancel(self,e=None):
        #main.focus()
        self.top.destroy()
class BillCreator:
    def __init__(self,top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.iconbitmap("./images/ico2.ico")
        top.title('فاتورة جديدة')   
        self.top = top
        self.label1 = Label(top)
        self.label1.place(x=0, y=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/bill.png")
        self.label1.configure(image=self.img)
        self.top = top
        self.top.protocol("WM_DELETE_WINDOW", Exit) 
        self.current_selected_transaction_id = None
        self.curCus = ''
        self.add_product_btn = self.BTN(top,72,45,1139,249,"#105da8","#ffffff","#105da8","اضافة",self.add_product)
        self.delete_product_btn = self.BTN(top,72,45,1002,249,'#bc8d14',"#ffffff","#bc8d14","حذف",self.delete_transaction)
        self.edite_product_btn = self.BTN(top,72,45,1002,310,'#1782ea',"#ffffff","#1782ea","تعديل",self.update_product)
        self.init_product_btn = self.BTN(top,72,45,1139,310,'#1782ea',"#ffffff","#1782ea","تهيئة",self.product_clear_JustENT)
        #self.btn2.configure(state="disabled")
        #self.btn3.configure(state="disabled")

        self.calc_btn = self.BTN(top,105,45,560,645,'#1782ea',"#ffffff","#1782ea","جمع",self.calculate)
        self.back_btn = self.BTN(top,105,45,1055,649,"#121212","#ffffff","#121212","عودة",self.GoBack)
        self.Print_pdf_btn = self.BTN(top,180,45,360,645,'#1782ea',"#ffffff","#1782ea","PDF طباعة إلى ",self.Print_to_pdf)
        self.clear_tree = self.BTN(top,105,45,235,645,'#1782ea',"#ffffff","#1782ea","تهيئة",self.cleartree)
        self.clear_note = self.BTN(top,85,40,1065,562,'#1782ea',"#ffffff","#1782ea","مسح",self.clearnote)
        self.e2 = Listbox(top)
        
        self.customer_name_ent = self.ENT(top,600,117,265,20,12)
        self.customer_phone_ent = self.ENT(top,100,117,265,20,12)
        
        self.product_name_ent = self.ENT(top,941,108,337,20,12)
        self.quant_ent = self.ENT(top,1137,198,141,17,12)
        self.singl_price_ent = self.ENT(top,946,198,141,17,12)
        
        self.note_ent = self.ENT(top,941,430,337,100,12)
        #self.note_ent.tag_config('center',justify='center')
        #self.note_ent.tag_add("center", 1.0, "end")
        #self.note_ent.configure(font="-family tajawal -size 12",)
        #self.note_ent.place(width=400,height=100,x=920,y=430)
        #self.note_ent.configure()#self.ENT(top,941,400,337,100,12)
        self.note_ent.config(borderwidth=3,justify='center',)


        self.tree = ttk.Treeview(top)
        self.scrollbary = Scrollbar(top)        
    
                
        self.count = 0
        self.remain=0
        self.theirsTotal=0
        self.oursTotal=0

            

        self.customer_name_ent.delete(0,END)
        self.customer_phone_ent.delete(0,END)
               
        self.create_tree()
        cur = db.cursor()
        cur.execute(""" CREATE TABLE if not exists tempbill (
            transaction_id INTEGER,
            transaction_name TEXT,
            quantity INTEGER,
            sale_price REAL,
            Ours REAL
        )""")
        self.customer_name_ent.bind('<Down>',self.down2)
        self.customer_name_ent.bind('<KeyRelease>',self.lstbx2)
        self.customer_name_ent.bind('<Return>',self.add_customer)
        self.customer_phone_ent.bind('<Return>',self.add_customer)

        self.quant_ent.bind('<Return>',self.add_product)
        self.singl_price_ent.bind('<Return>',self.add_product)
        self.product_name_ent.bind('<Return>',self.add_product)
        self.tree.bind('<Delete>',self.delete_transaction) 
        self.product_btn_dis()
        self.pdf = FPDF()
        self.customer_name_ent.focus()

    def create_tree(self):
        s = ttk.Style()
        s.configure('Treeview', rowheight=30)
        self.f1 = Frame(self.top)
        self.f1.place(x=75,y=185,width=776,height=432)
        self.scrollbary = Scrollbar(self.top, orient=VERTICAL)
        self.tree = ttk.Treeview(self.f1)
        self.tree.place(relx=0,rely=0,width=776,height=432)
        self.tree.configure(yscrollcommand=self.scrollbary.set)
        self.tree.configure(selectmode="extended")
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbary.place(x=855,y=185, width=18, height=432)
        self.tree.configure(
            columns=(
                "ours",
                "sale_price",
                "quantity",
                "transaction_name",
                "tslsl",
                "transaction_id",
            )
        )
        self.tree.heading("ours", text="الإجمالي",anchor=CENTER)
        self.tree.heading("sale_price", text="السعر",anchor=CENTER)
        self.tree.heading("quantity", text="الكمية",anchor=CENTER)
        self.tree.heading("transaction_name", text="البيان",anchor=CENTER)
        self.tree.heading("tslsl", text="#",anchor=CENTER)
        self.tree.heading("transaction_id", text="",anchor=CENTER)
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=150,anchor=CENTER)
        self.tree.column("#2", stretch=NO, minwidth=0, width=150,anchor=CENTER)
        self.tree.column("#3", stretch=NO, minwidth=0, width=125,anchor=CENTER)
        self.tree.column("#4", stretch=NO, minwidth=0, width=300,anchor=CENTER)
        self.tree.column("#5", stretch=NO, minwidth=0, width=50,anchor=CENTER)
        self.tree.column("#6", stretch=NO, minwidth=0, width=5,anchor=CENTER)
        self.tree.tag_configure('sale', background = "#ffffff",font='-family tajawal -size 11')
        self.tree.tag_configure('brief', background = "#de9999",font='-family tajawal -size 11')
        self.tree.tag_configure('billTot', background = "#d2d297",font='-family tajawal -size 11')
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
    def cleartree(self):
        sure = messagebox.askyesno('تنبيه','هل تريد بالتأكيد تهيئة كامل الفاتورة',parent=self.top)
        if sure :
            self.tree.delete(*self.tree.get_children())
            delete = "DELETE FROM tempbill WHERE transaction_id > 0"
            cur.execute(delete)
            db.commit()
            self.Display_Data()
            self.note_ent.delete(0,END)
            self.product_name_ent.delete(0,END)
            self.quant_ent.delete(0,END)
            self.singl_price_ent.delete(0,END)
            self.customer_name_ent.delete(0,END)
            self.customer_phone_ent.delete(0,END)
    def clearnote(self):
        self.note_ent.delete(0,END)
    def add_product(self,e=None):
        cusName = self.curCus
        if cusName.strip():
            cur.execute('SELECT customer_name from customers WHERE customer_name = ?',(cusName,))
            fet= cur.fetchone()
            if fet == None :
                messagebox.showerror('خطأ', 'تأكد من اسم الزبون',parent = self.top)
                self.customer_name_ent.focus()
                return 
            if self.product_name_ent.get().strip():
                if self.quant_ent.get().strip():
                    if self.singl_price_ent.get().strip():
                        try:
                            transPrice = float(self.singl_price_ent.get().strip())
                            transQuantity = float(self.quant_ent.get().strip())
                        except ValueError :
                            messagebox.showerror('خطأ', 'قيم غير صحيحة',parent = self.top)
                            return
                        
                        transName=self.product_name_ent.get().strip()
                        cur.execute('SELECT max(transaction_id) from tempbill')
                        sel= cur.fetchone()
                        transId = sel[0]+1 if sel[0] != None else 1
                        cur.execute("INSERT INTO tempbill VALUES (:transaction_id,:transaction_name,:quantity,:sale_price,:Ours)",
                                                                    {
                                                                        'transaction_id':transId ,
                                                                        'transaction_name':transName  ,
                                                                        'quantity' : transQuantity  ,
                                                                        'sale_price':transPrice ,
                                                                        'Ours' : float(transPrice)*float(transQuantity) ,
                                                                    })
                        db.commit()
                        self.Display_Data()
                        self.product_clear_JustENT()
                        self.product_name_ent.focus()
                    else:
                        messagebox.showerror('خطأ', 'أدخل السعر',parent = self.top)
                        self.singl_price_ent.focus()
                else:
                    messagebox.showerror('خطأ', 'أدخل الكمية',parent = self.top)
                    self.quant_ent.focus()
            else:
                messagebox.showerror('خطأ', 'أدخل اسم المنتج',parent = self.top)
                self.product_name_ent.focus()
        else:
            messagebox.showerror('خطأ', 'أدخل اسم الزبون أولاً',parent = self.top)
            self.customer_name_ent.focus()    

    def update_product(self):
        cusName = self.curCus
        if cusName.strip():
            cur.execute('SELECT customer_phone from customers WHERE customer_name = ?',(cusName,))
            fet= cur.fetchone()
            if fet == None :
                messagebox.showerror('خطأ', 'تأكد من اسم الزبون',parent = self.top)
                self.customer_name_ent.focus()
                return 
            if self.product_name_ent.get().strip():
                if self.quant_ent.get().strip():
                    if self.singl_price_ent.get().strip():
                        try:
                            transPrice = float(self.singl_price_ent.get().strip())
                            transQuantity = float(self.quant_ent.get().strip())
                        except ValueError :
                            messagebox.showerror('خطأ', 'قيم غير صحيحة',parent = self.top)
                            return
                        
                        update = (
                                        "UPDATE tempbill SET sale_price = ?, quantity = ?,Ours = ?  WHERE transaction_id = ?"
                                        )
                        cur.execute(update, (transPrice, transQuantity,transPrice*transQuantity,self.current_selected_transaction_id))
                        db.commit()
                        self.Display_Data()
                        self.product_clear_JustENT()
                        self.product_name_ent.focus()
                        self.product_btn_dis()
                    else:
                        messagebox.showerror('خطأ', 'أدخل السعر',parent = self.top)
                        self.singl_price_ent.focus()
                else:
                    messagebox.showerror('خطأ', 'أدخل الكمية',parent = self.top)
                    self.quant_ent.focus()
            else:
                messagebox.showerror('خطأ', 'أدخل اسم المنتج',parent = self.top)
                self.product_name_ent.focus()
        else:
            messagebox.showerror('خطأ', 'قم بإدخال اسم الزبون أولاً',parent = self.top)
            self.customer_name_ent.focus()    
    def product_clear_JustENT(self):
        self.product_name_ent.delete(0,END)
        self.quant_ent.delete(0,END)
        self.singl_price_ent.delete(0,END)

    def payment_clear_JustENT(self):
        self.note_ent.delete(0,END)
    def delete_transaction(self,e=None):
        msg = 'هل تريد بالتأكيد حذف المنتج المحدد من الفاتورة؟'

        sure = messagebox.askyesno('تنبيه',msg,parent=self.top)
        if sure :
            delete = "DELETE FROM tempbill WHERE transaction_id = ?"
            cur.execute(delete,(self.current_selected_transaction_id,))
            db.commit()
        self.Display_Data()
    def Display_Data(self):
        if self.tree.winfo_exists():
            cur.execute("SELECT * FROM tempbill")
            fetch = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            tslsl=0
            self.oursTotal=0
            self.theirsTotal=0
            for data in fetch:
                tslsl+=1
                self.tree.insert("", "end",tags='sale' ,values=(data[4],data[3],data[2],data[1],tslsl,data[0]))
        self.product_btn_dis()
        self.product_clear_JustENT()
    def calculate(self):
        if self.curCus :
            cur.execute("SELECT sum(Ours) FROM tempbill")
            fetch = cur.fetchone()
            oursTotal=float(fetch[0]) if fetch[0] != None else 0
            self.tree.insert("", "end",tags='brief',values=(oursTotal,' ',' ','الإجمالي','',None))
    def on_tree_select(self,e):
        selected= self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values == '' :
            return
        self.current_selected_transaction_id = values[5]
        if values[5] != None:    
            self.product_btn_ena()
            self.product_name_ent.delete(0,END)
            self.quant_ent.delete(0,END)
            self.singl_price_ent.delete(0,END)
            self.note_ent.delete(0,END)
            self.product_name_ent.insert(0,values[3])
            self.quant_ent.insert(0,float(values[2]))
            self.singl_price_ent.insert(0,values[1])
        else:
            self.product_btn_dis()
            self.Display_Data()
            self.product_clear_JustENT()
            return
    def product_btn_dis(self,e=None):
        self.delete_product_btn.configure(state=DISABLED)
        self.edite_product_btn.configure(state=DISABLED)
    def product_btn_ena(self,e=None):
        self.delete_product_btn.configure(state=NORMAL)
        self.edite_product_btn.configure(state=NORMAL)
    def a2(self,e):
        self.customer_name_ent.delete(0,END)
        self.customer_phone_ent.delete(0,END)
        for i in self.e2.curselection():
            self.customer_name_ent.insert(0,self.e2.get(i))
            self.e2.destroy()
        self.curCus=self.customer_name_ent.get().strip()
        cur.execute("SELECT customer_phone FROM customers WHERE customer_name like ?",(self.curCus,))
        fetch = cur.fetchone()
        self.customer_phone_ent.insert(0,fetch[0])
        db.commit()
        self.Display_Data()
        self.product_name_ent.focus()
    def lstbx2(self,e):
        if self.e2.winfo_exists():
            self.e2.destroy()
        if  self.customer_name_ent.get().strip():
            self.e2 = Listbox(
            self.top,
            width=20,
            activestyle=None,
            height=5,
            selectmode=SINGLE,
            justify=RIGHT,
            border=0,
            cursor='arrow',
            selectbackground='#ffffff',
            selectforeground='#105da8',
            font=('tajawal 15'))
            self.e2.place(x=600,y=140,width=265,height=85)
            lookup_record = self.customer_name_ent.get().strip()

            if not lookup_record.strip() and self.e2.winfo_exists():
                self.e2.destroy()
            else:
                ss='%'+lookup_record+'%'
                cur.execute("SELECT * FROM customers WHERE customer_name like ?",(ss,))
                fetch = cur.fetchall()
                if fetch==[]:
                    message1 = 'زبون جديد! أدخل الاسم والرقم واضغط انتر'
                    self.e2.insert(END,message1)
                    self.e2.configure(font='tajawal 10')
                    self.e2.configure(justify=CENTER)
                    self.e2.configure(foreground='#bc8d14')
                    self.customer_phone_ent.delete(0,END)
                else:
                    for h in fetch:
                        self.e2.insert(END,h[1])
                    db.commit()
            if self.e2.winfo_exists():    
                self.e2.bind('<Double-1>',self.a2)
                self.e2.bind('<Return>',self.a2)
                self.e2.bind('<Down>',self.down2)
                self.e2.bind('<Up>',self.up2)
            self.customer_name_ent.bind("<Down>",self.fromE2L2)
        else:
            if self.e2.winfo_exists():
                self.e2.destroy()
    def fromE2L2(self,e):
        if self.e2.winfo_exists(): 
            self.count = 0
            self.e2.focus()
            self.count= self.e2.index(ANCHOR)
            x= self.e2.index(ACTIVE)
            self.e2.selection_clear(0,END)
            self.e2.selection_set(x)
    def down2(self,e):
        if self.e2.winfo_exists():
            if self.e2.index(ACTIVE)+1 < self.count :
                self.e2.selection_clear(0,END)
                self.e2.selection_set(self.e2.index(ACTIVE)+1)
    def up2(self,e):
        if self.e2.index(ACTIVE) > 0 :
            self.e2.selection_clear(0,END)
            self.e2.selection_set(self.e2.index(ACTIVE)-1)    
        else:
            self.customer_name_ent.focus()
            self.e2.destroy()
    def add_customer(self,e):
        if not self.customer_name_ent.get().strip():
            messagebox.showwarning("تحذير!","ادخل اسم الزبون",parent=self.top)
            self.customer_name_ent.delete(0,END)
            self.customer_name_ent.focus()
            return
        else:
            if not self.customer_phone_ent.get().strip():
                messagebox.showwarning("تحذير!","ادخل العنوان",parent=self.top)
                self.customer_phone_ent.delete(0,END)
                self.e2.destroy()
                self.customer_phone_ent.focus()
                return
            else:   
                cur.execute("SELECT * FROM customers WHERE customer_name=:PN1",{'PN1' : self.customer_name_ent.get().strip() ,'PN2':self.customer_phone_ent.get()  })
                fetch = cur.fetchall()
                if fetch == []:
                    cur.execute("select max(customer_id) from customers")
                    fetch1 = cur.fetchone() 
                    conter =int(fetch1[0])+1 if fetch1[0]!=None else 0
                    cur.execute("INSERT INTO customers VALUES ( :customer_id,:customer_name , :customer_phone)",
                                {
                                    'customer_id': conter,       
                                    'customer_name':self.customer_name_ent.get().strip(),
                                    'customer_phone': self.customer_phone_ent.get().strip()  
                                } )
                    db.commit()
                    messagebox.showwarning("","تم إضافة الزبون",parent=self.top)
                    self.e2.destroy()
                    self.curCus=self.customer_name_ent.get().strip()
                    self.Display_Data()
                    self.product_name_ent.focus()

                else:
                    messagebox.showwarning("تحذير!","اسم الزبون\العنوان الذي أدخلته موجود مسبقاً",parent=self.top)
    def GoBack(self):
        sure = messagebox.askyesno('تنبيه','!هل أنت متأكد؟ سيتم فقدان بيانات الفاتورة')
        if sure:
            self.top.destroy()
            notebookTop.deiconify()
            delete = "DELETE FROM tempbill WHERE transaction_id > 0"
            cur.execute(delete)
            db.commit()
    def BTN(self,pay_card,width,height,x,y,activebackground,foreground,background,text1,command=None):
        btn = Button(pay_card,text=text1)
        btn.place(width=width,height=height,x=x,y=y)
        btn.configure(activebackground=activebackground)
        btn.configure(relief="flat")
        btn.configure(overrelief="flat")
        btn.configure(cursor="hand2")
        btn.configure(foreground=foreground)
        btn.configure(background=background)
        btn.configure(font="-family tajawal -size 14 -weight bold")
        btn.configure(borderwidth="0")
        btn.configure(command=command)
        return btn
    def ENT(self,root,x,y,width,height,size):
        ent = Entry(root,borderwidth=0,justify=CENTER)
        ent.configure(font=f"-family tajawal -size {size}")
        ent.place(width=width,height=height,x=x,y=y)
        return ent
    
    def create_table(self,table_data, title='', data_size = 14, title_size=12, align_data='C', align_header='C', cell_width='even', x_start='x_default',emphasize_data=[ar_display('البيان')], emphasize_style=None, emphasize_color=(255,0,0)):
        default_style = self.pdf.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.pdf.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = [25,25,20,110,10]

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.pdf.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                col_width = col_widths



                        ### compare columns 

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int        
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.pdf.font_size * 1.5

        col_width = get_col_widths()
        self.pdf.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from self.pdf width and divide by 2 (margins)
            margin_width = self.pdf.w - table_width
            # TODO: Check if table_width is larger than self.pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.pdf.set_x(x_start)
        elif isinstance(x_start, int):
            self.pdf.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.pdf.set_x(self.pdf.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.pdf.set_font_size(16)
            
            self.pdf.multi_cell(0, line_height, title, border=0, align='C', ln=3, max_line_height=self.pdf.font_size)
            self.pdf.set_font_size(self.pdf.font_size)
            self.pdf.ln(5)
            self.pdf.ln(line_height) # move cursor back to the left margin

        self.pdf.set_font(size=data_size)
        # add header
        y1 = self.pdf.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.pdf.get_x()
        x_right = self.pdf.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.pdf.set_x(x_start)
            for datum in header:
                self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.pdf.font_size)
                x_right = self.pdf.get_x()
            self.pdf.ln(line_height) # move cursor back to the left margin
            y2 = self.pdf.get_y()
            self.pdf.line(x_left,y1,x_right,y1)
            self.pdf.line(x_left,y2,x_right,y2)

            for row in data:
                if self.pdf.get_y() > 240 : 
                    self.pdf.ln()
                    self.pdf.line(x_left,self.pdf.get_y(),self.pdf.w-5,self.pdf.get_y())
                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
                    self.pdf.cell(0,10,f' {self.pdf.page_no()} {ar_display("صفحة")}',align='R',)    
                    self.pdf.ln()

                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=12)

                    self.pdf.add_page()
                if x_start: # not sure if I need this
                    self.pdf.set_x(x_start)
                if data.index(row) > len(data)-2 and data.index(row)      :
                    self.pdf.line(10,self.pdf.get_y(),self.pdf.w-15,self.pdf.get_y())
                for datum in row:
                    if datum in emphasize_data:
                        self.pdf.set_text_color(*emphasize_color)
                        self.pdf.set_font(style=emphasize_style)
                        self.pdf.multi_cell(col_width, line_height, str(datum), border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size)
                        self.pdf.set_text_color(0,0,0)
                        self.pdf.set_font(style=default_style)
                    else:
                        self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self.pdf
                self.pdf.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.pdf.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.pdf.font_size)
                x_right = self.pdf.get_x()
            self.pdf.ln(line_height) # move cursor back to the left margin
            y2 = self.pdf.get_y()
            self.pdf.line(x_left,y1,x_right,y1)
            self.pdf.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if self.pdf.get_y() > 240 : 
                    self.pdf.ln()
                    self.pdf.line(x_left,self.pdf.get_y(),self.pdf.w-5,self.pdf.get_y())
                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
                    self.pdf.cell(0,10,f' {self.pdf.page_no()} {ar_display("صفحة")}',align='R',)    
                    self.pdf.ln()

                    self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=12)

                    self.pdf.add_page()
                if x_start:
                    self.pdf.set_x(x_start)
                row = data[i]
                self.pdf.line(10,self.pdf.get_y(),self.pdf.w-10,self.pdf.get_y())
                for j in range(len(row)):
                    datum = str(row[j])
                    if not isinstance(datum, str):
                        datum = datum
                    adjusted_col_width = col_width[j]
                    if i > len(data)-2:
                        self.pdf.set_text_color(*emphasize_color)
                        self.pdf.set_font(style=emphasize_style)
                        self.pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size)
                        self.pdf.set_text_color(0,0,0)
                        self.pdf.set_font(style=default_style)
                    else:
                    
                        self.pdf.multi_cell(adjusted_col_width, line_height, str(datum), border=0, align=align_data, ln=3, max_line_height=self.pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self.pdf
                    
                        
                self.pdf.ln(line_height) # move cursor back to the left margin
        y3 = self.pdf.get_y()
        self.pdf.line(x_left,y3,x_right,y3)
    def Print_to_pdf(self):
        if not self.curCus:
            messagebox.showerror('خطأ','قم باختيار زبون أولاً',parent= self.top)
            return
        cus_name = self.curCus
        query= 'select Ours,sale_price,quantity,transaction_name from tempbill'
        cur.execute(query)
        data1 = cur.fetchall()
        data1.insert(0,('الإجمالي','السعر','الكمية','البيان','م'))
        data1=[list(a) for a in data1]
        tslsl=0
        for i in range(1,len(data1)) :
            tslsl+=1
            data1[i].insert(4,tslsl) 
        query2 = 'select SUM(Ours) from tempbill'
        cur.execute(query2)
        totals = cur.fetchone()
        ours =  totals[0] if totals[0] != None else 0
        word1 = 'المجموع'
        result = [ours,' ',' ',word1,' ']
        data1.append(result)
        for i in range(len(data1)) :
            for j in range(5):
                data1[i][j] = ar_display(data1[i][j])
        pdfCreationDate = str(date.today())

        cusN = ar_display(f'فاتورة للسيد : {cus_name}')
        Bdate = ar_display(f'بتاريخ :  {pdfCreationDate}')
        tit = f'{cusN}'
        GainPercen = ar_display('نسبة الربح :')
        self.pdf = FPDF()
        self.pdf.alias_nb_pages()
        self.pdf.add_font("NotoSansArabic_ExtraCondensed-Regular", style="", fname="./fonts/NotoSansArabic_ExtraCondensed-Regular.ttf")
        self.pdf.add_page()
        self.pdf.ln(5)
        self.pdf.image('./images/bill1.jpg',1,5,self.pdf.w)
        self.pdf.line(10,55,self.pdf.w-10,55)
        self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=14)
        self.pdf.ln(40)
        self.pdf.cell(0,10,'',align='L')
        self.pdf.ln()
        self.pdf.cell((self.pdf.w-20)/2,10,Bdate,align='L')
        self.pdf.cell((self.pdf.w-20)/2,10,tit,align='R')
        #self.pdf.ln()
        
        self.pdf.ln(5)
        self.pdf.set_text_color(0,200,0)
        #self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=12)
        self.pdf.ln()        
        self.pdf.cell(0,10,f'{ar_display("بالمئة")} {12} {GainPercen}',align='C')
        self.pdf.ln()
        self.pdf.set_text_color(0,0,0)
        self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=14)
        self.create_table(table_data = data1,title='', cell_width='uneven')
        
        note = f'ملاحظة: {self.note_ent.get()}'
        if self.note_ent.get().strip():
            self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=12)
            self.pdf.ln()
            self.pdf.ln()
            self.pdf.set_text_color(255,0,0)
            self.pdf.cell(0,10,ar_display(note),align='R')
            self.pdf.ln()
        self.pdf.set_text_color(0,0,0)
        self.pdf.set_font('Arial',size=10)
        self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
        self.pdf.cell(0,10,f' {self.pdf.page_no()} {ar_display("صفحة")}',align='R',)
        self.pdf.set_font("NotoSansArabic_ExtraCondensed-Regular", size=10)
        self.pdf.ln()
        wordtype = ' فاتورة '
        justname = f'{wordtype}{cus_name}{pdfCreationDate}'
        path = asksaveasfilename(initialfile=justname, initialdir='./pdfs')
        if path.strip():
            self.pdf.output(f'{path}.pdf')
page1 = login_page(main)
main.mainloop()

""" thismachine = hex(uuid.getnode())
print(thismachine)
authorized = ["0xffffffffffff","add your device Mac address Here using this format : 0xffffffffffff"]
if thismachine in authorized :
    main.mainloop()
else:
     messagebox.showerror("عذراً", "هذا الجهاز غير مصرح له بالدخول إلى البرنامج") """
