from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


class ClassSchedule:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Class Schedule")
        self.root.geometry("800x790+0+0")

        self.center_window()

        self.ClassId=StringVar()
        self.ClassName=StringVar()
        self.DaysClass=StringVar()
        self.Time=StringVar()
        self.RoomNumber=StringVar()

        lbltitle=Label(self.root,bd=20,relief="solid",text="CLASS SCHEDULE",fg="Black",bg="white",font=("arial",40,"bold"))
        lbltitle.place(x=0,y=0,width=800,height=100)


        Dataframe=Frame(self.root,bd=20,relief="solid")
        Dataframe.place(x=0,y=130,width=800,height=230)

        ButtonFrame=Frame(self.root,bd=20,relief="solid")
        ButtonFrame.place(x=0,y=385,width=800,height=87) 

        DetailsFrame=Frame(self.root,bd=20,relief="solid")
        DetailsFrame.place(x=0,y=498,width=800,height=250)

        lblClassId=Label(Dataframe,font=("arial",12,"bold"),text="Class Id:",padx=2,pady=7)
        lblClassId.grid(row=0,column=0,sticky=W)
        txtClassId=Entry(Dataframe,font=("arial",12,"bold"),textvariable=self.ClassId,width=30)
        txtClassId.grid(row=0,column=1)

        lblClassName=Label(Dataframe,font=("arial",12,"bold"),text="Class Name:",padx=2,pady=7)
        lblClassName.grid(row=1,column=0,sticky=W)
        txtClassName=Entry(Dataframe,font=("arial",12,"bold"),textvariable=self.ClassName,width=30)
        txtClassName.grid(row=1,column=1)

        lblDayClass=Label(Dataframe,font=("arial",12,"bold"),text="Days:",padx=2,pady=7)
        lblDayClass.grid(row=2,column=0,sticky=W)
        txtDayClass=Entry(Dataframe,font=("arial",12,"bold"),textvariable=self.DaysClass,width=30)
        txtDayClass.grid(row=2,column=1)

        lblTime=Label(Dataframe,font=("arial",12,"bold"),text="Time:",padx=2,pady=7)
        lblTime.grid(row=3,column=0,sticky=W)
        txtTime=Entry(Dataframe,font=("arial",12,"bold"),textvariable=self.Time,width=30)
        txtTime.grid(row=3,column=1)

        lblRoomNumber=Label(Dataframe,font=("arial",12,"bold"),text="Room Number:",padx=2,pady=7)
        lblRoomNumber.grid(row=4,column=0,sticky=W)
        txtRoomNumber=Entry(Dataframe,font=("arial",12,"bold"),textvariable=self.RoomNumber,width=30)
        txtRoomNumber.grid(row=4,column=1)

        btnAdd=Button(ButtonFrame,text="Add",command=self.addClass,bg="red",fg="white",font=("arial",12,"bold"),width=18,padx=2,pady=8)
        btnAdd.grid(row=0,column=0)

        btnUpdate=Button(ButtonFrame,text="Update",command=self.update_data,bg="red",fg="white",font=("arial",12,"bold"),width=18,padx=2,pady=8)
        btnUpdate.grid(row=0,column=1)

        btnClear=Button(ButtonFrame,text="Clear",command=self.clear,bg="red",fg="white",font=("arial",12,"bold"),width=18,padx=2,pady=8)
        btnClear.grid(row=0,column=2)

        btnDelete=Button(ButtonFrame,text="Delete",command=self.idelete,bg="red",fg="white",font=("arial",12,"bold"),width=18,padx=2,pady=8)
        btnDelete.grid(row=0,column=3)

        scroll_x=ttk.Scrollbar(DetailsFrame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(DetailsFrame,orient=VERTICAL)
        self.class_table=ttk.Treeview(DetailsFrame,column=("classid","classname","daysclass","time","roomnumber"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x=ttk.Scrollbar(command=self.class_table.xview)
        scroll_y=ttk.Scrollbar(command=self.class_table.yview)

        self.class_table.heading("classid",text="Class Id")
        self.class_table.heading("classname",text="Class Name")
        self.class_table.heading("daysclass",text="Days Class")
        self.class_table.heading("time",text="Time")
        self.class_table.heading("roomnumber",text="Room Number")

        self.class_table["show"]="headings"

        self.class_table.column("classid",width=100)
        self.class_table.column("classname",width=100)
        self.class_table.column("daysclass",width=100)
        self.class_table.column("time",width=100)
        self.class_table.column("roomnumber",width=100)

        self.class_table.pack(fill=BOTH,expand=1)
        self.class_table.bind("<ButtonRelease-1>",self.get_cursor)

        self.fetch_data()
        
    def center_window(self):
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (800 / 2)  
        y = (screen_height / 2) - (750 / 2) 
        self.root.geometry(f"800x750+{int(x)}+{int(y)}")


    def addClass(self):
        if self.ClassId.get()=="" or self.ClassName.get()=="" or self.DaysClass.get()=="" or self.Time.get()=="" or self.RoomNumber.get()=="":
            messagebox.showerror("Error","All Fields are required")
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="Gitmaster0817$",database="mydata")
            my_cursor=conn.cursor()
            my_cursor.execute("insert into class values(%s,%s,%s,%s,%s)",(
                              self.ClassId.get(),
                              self.ClassName.get(),
                              self.DaysClass.get(),
                              self.Time.get(),
                              self.RoomNumber.get(),
                              ))
            conn.commit()
            self.fetch_data()
            self.clear()
            conn.close()
            messagebox.showinfo("Success","Record Inserted Successfully")

    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",user="root",password="Gitmaster0817$",database="mydata")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from class")
        rows=my_cursor.fetchall()
        if len(rows) != 0:
            self.class_table.delete(*self.class_table.get_children())
            for i in rows:
                self.class_table.insert("",END,values=i)
            conn.commit()
        conn.close() 

    def get_cursor(self,event=""):
        cursor_row=self.class_table.focus()    
        content=self.class_table.item(cursor_row)
        row=content["values"]
        self.ClassId.set(row[0])
        self.ClassName.set(row[1])
        self.DaysClass.set(row[2])
        self.Time.set(row[3])
        self.RoomNumber.set(row[4])

        
    def clear(self):
        self.ClassId.set("")
        self.ClassName.set("")
        self.DaysClass.set("")
        self.Time.set("")
        self.RoomNumber.set("")
        
    def update_data(self):
        conn=mysql.connector.connect(host="localhost",user="root",password="Gitmaster0817$",database="mydata")
        my_cursor=conn.cursor()
       
        

        try: 
            if self.ClassId.get()=="" or self.ClassName.get()=="" or self.DaysClass.get()=="" or self.Time.get()=="" or self.RoomNumber.get()=="":
                messagebox.showerror("Error","Fields not Filled out");
                return
            my_cursor.execute("update class set classname=%s,daysclass=%s,time=%s,roomnumber=%s where classid=%s"
                          , (
                              self.ClassName.get(),
                              self.DaysClass.get(),
                              self.Time.get(),
                              self.RoomNumber.get(),
                              self.ClassId.get()))
            conn.commit()
            self.fetch_data()
            
            messagebox.showinfo("Success","Record Updated Successfully")
        except Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")
        finally:
            conn.close()       
        

    def idelete(self):
      if self.ClassId.get()=="":
        messagebox.showerror("Error","No Record Selected")
      else:  
        conn=mysql.connector.connect(host="localhost",user="root",password="Gitmaster0817$",database="mydata")
        my_cursor=conn.cursor()
        query="delete from class where classid=%s"
        value=(self.ClassId.get(),)
        my_cursor.execute(query,value)     
        conn.commit()   
        self.fetch_data()
        self.clear()
        conn.close()
        messagebox.showinfo("Deleted","Record has been deleted successfully")         


if __name__ == "__main__":
    root=Tk()
    application=ClassSchedule(root) 
    root.mainloop()  