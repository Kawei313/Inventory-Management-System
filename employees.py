from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pymysql # pip install pymysql

def connect_database():
  try:
    connection=pymysql.connect(host="localhost", user="root", password="@Bach2004")
    cursor = connection.cursor()
  except:
    messagebox.showerror("Error", "Database connectivity issue try again")
    return None, None
  return cursor, connection

def create_database_table():
  cursor, connection= connect_database()
  cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
  cursor.execute("USE inventory_system")
  cursor.execute("CREATE TABLE IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100), "
                "email VARCHAR(100), gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), employment_type VARCHAR(50), "
                " education VARCHAR(50), word_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary VARCHAR(50), usertype VARCHAR(50), "
                "password VARCHAR(50))")

def treeview_data():
  cursor, connection = connect_database()
  if not cursor or not connection:
    return
  cursor.execute("use inventory_system")
  try:
    cursor.execute("SELECT * from employee_data")
    employee_records = cursor.fetchall() #để lấy tất cả các hàng (rows) của kết quả đó và trả về dạng danh sách (list) của tuple.
    employee_treeview.delete(*employee_treeview.get_children())
    for record in employee_records:
      employee_treeview.insert("", END, values=record)
  except Exception as e:
    messagebox.showerror("Error", f"Error due to {e}")
  finally:
    cursor.close()
    connection.close()
    
def select_data(event,empid_entry, name_entry, email_entry,
                dob_date_entry,gender_combobox, contact_entry, 
                employment_type_combobox,education_combobox, work_shift_combobox,
                address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry):
  index = employee_treeview.selection()
  # print(index)
  content = employee_treeview.item(index)
  # print(content)
  clear_fields(empid_entry, name_entry, email_entry,
              dob_date_entry,gender_combobox, contact_entry, 
              employment_type_combobox,education_combobox, work_shift_combobox,
              address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry, False)
  row = content['values']
  empid_entry.insert(0, row[0])
  name_entry.insert(0, row[1])
  email_entry.insert(0, row[2])
  gender_combobox.set(row[3])
  dob_date_entry.set_date(row[4])
  contact_entry.insert(0, row[5])
  employment_type_combobox.set(row[6])
  education_combobox.set(row[7])
  work_shift_combobox.set(row[8])
  address_text.insert(1.0, row[9])
  doj_date_entry.set_date(row[10])
  salary_entry.insert(0, row[11])
  usertype_combobox.set(row[12])
  password_entry.insert(0,row[13])
  
def update_employee(empid, name, email, gender, dob, contact, employment_type,education, word_shift, address, doj, salary, user_type, password):
  selected = employee_treeview.selection()
  if not selected:
    messagebox.showerror("Error", "No row is selected")
  else:
    cursor, connection = connect_database()
    if not cursor or not connection:
      return
    try:
      cursor.execute('use inventory_system') 
      cursor.execute('SELECT * from employee_data WHERE empid=%s', (empid,))
      curent_data = cursor.fetchone()
      curent_data = curent_data[1:]

      address=address.strip()
      new_data = (name, email, gender, dob, contact, employment_type,education, word_shift, address, doj, salary, user_type, password)
  
      if curent_data==new_data:
        messagebox.showinfo("Information", "No changes detected")
        return
      
      cursor.execute('UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, employment_type=%s,education=%s,'
                    'word_shift=%s, address=%s, doj=%s, salary=%s, usertype=%s, password=%s WHERE empid=%s',
                    (name, email, gender, dob, contact, employment_type,education, word_shift, address, doj, salary, user_type, password, empid))
      connection.commit()
      treeview_data()
      messagebox.showinfo('Success', 'Data is update successfully')
      
    except Exception as e:
      messagebox.showerror("Error", f"Error due to {e}")
    finally:
      cursor.close()
      connection.close()
    

def add_employee(empid, name, email, gender, dob, contact, employment_type,education, word_shift, address, doj, salary, user_type, password):
  if (empid=="" or name=="" or email=="" or gender=="Select Gender" or contact=="" or employment_type=="Select type" or
      education=="Select Education" or word_shift=="Select Shift" or address == '' or 
      user_type=="Select User Type" or password==""):
    
    messagebox.showerror("Error", "All fields are required")
    
  else: 
    cursor, connection=connect_database()
    if not cursor or not connection:
      return
    cursor.execute("use inventory_system")
    try: 
      cursor.execute("SELECT empid from employee_data WHERE empid=%s", (empid))
      if cursor.fetchone():
        messagebox.showerror("Error", "Id already exists")
        return
      address=address.strip()
      cursor.execute("INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(empid, name, email, gender, dob, contact, employment_type,education, word_shift, address, doj, salary, 
                                                                                                    user_type, password))
      connection.commit() #Lưu lại xác nhận
      treeview_data()
      messagebox.showinfo("Success", "Data is inserted successfully")
    except Exception as e:
      messagebox.showerror("Error", f"Error due to {e}")
    finally:
      cursor.close()
      connection.close()
      
    
def clear_fields(empid_entry, name_entry, email_entry,
                dob_date_entry,gender_combobox, contact_entry, 
                employment_type_combobox,education_combobox, work_shift_combobox, 
                address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry, check):
  empid_entry.delete(0, END)
  name_entry.delete(0, END)
  email_entry.delete(0, END)
  from datetime import date
  dob_date_entry.set_date(date.today())
  gender_combobox.set("Select Gender")
  contact_entry.delete(0, END)
  employment_type_combobox.set("Select Type")
  education_combobox.set("Select Education")
  work_shift_combobox.set("Select Work Shift")
  address_text.delete(1.0, END)
  doj_date_entry.set_date(date.today())
  salary_entry.delete(0, END)
  usertype_combobox.set("Select User Type")
  password_entry.delete(0, END)
  
  if check:
    employee_treeview.selection_remove(employee_treeview.selection())

def delete_employee(empid, ):
  selected = employee_treeview.selection()
  if not selected:
    messagebox.showerror("Error", "No row is selected")
  else:
    result=messagebox.askyesno('Confirm', 'Do you want to delete the record')
    if result:
      cursor, connection = connect_database()
      if not cursor or not connection:
        return
      try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM employee_data WHERE empid=%s', (empid,))
        connection.commit()
        treeview_data()
        messagebox.showinfo('Success', 'Record is deleted')
      except Exception as e:
          messagebox.showerror("Error", f"Error due to {e}")
      finally:
        cursor.close()
        connection.close()
    
def search_employee(search_option, value):
  if search_option == "Search By":
    messagebox.showerror('Error', 'No option is selected')
  elif value=='':
    messagebox.showerror('Error', 'Enter the value to search')
  else:
    # search_option=search_option.replace(' ','_')
    option_map = {
            'EmpId': 'empid',
            'Name': 'name',
            'Email': 'email',
            'Employment Type': 'employment_type',
            'Education': 'education',
            'Work Shift': 'word_shift'
        }
    search_option = option_map.get(search_option)
    cursor, connection = connect_database()
    if not cursor or not connection:
      return
    try:
      cursor.execute('use inventory_system')
      cursor.execute(f"SELECT * FROM employee_data WHERE {search_option} LIKE %s", (f"%{value}%",))

      records=cursor.fetchall()
      
      employee_treeview.delete(*employee_treeview.get_children()) #Lấy tuple chứa id
      for record in records:
        employee_treeview.insert('', END, value=record)
    except Exception as e:
      messagebox.showerror("Error", f"Error due to {e}")
    finally:
      cursor.close()
      connection.close()

def show_all(search_entry, search_combobox):
  treeview_data()
  search_entry.delete(0, END)
  search_combobox.set('Search By')
  

#Functionality Part
def employee_form(window):
  global back_image, employee_treeview #Biến toàn cục để tránh bị thu khi hàm kết thúc
  employee_frame=Frame(window, width=1070, height=567, bg="white")
  employee_frame.place(x=200, y=100)
  heading_label = Label(employee_frame, text="Manage Employee Details", font=("Times New Roman", 16, "bold"), bg="#0f4d7d", fg="white")
  heading_label.place(x=0, y=0, relwidth=1) 
  
  top_frame = Frame(employee_frame, bg="white")
  top_frame.place(x=0, y=40, relwidth=1, height=235)
  
  back_image=PhotoImage(file=r"helpers/icons/back_button.png")
  back_button = Button(top_frame, image=back_image, cursor="hand2", bd=0,bg="white", command=lambda:employee_frame.place_forget()) #lambda: hàm không tên
  back_button.place(x=10, y=0)
  
  search_frame = Frame(top_frame, bg="white")
  search_frame.pack()
  search_combobox=ttk.Combobox(search_frame, values=('EmpId','Name', 'Email', 'Employment Type', 'Education', 'Work Shift'), font=("Times New Roman", 12), state="readonly", justify=CENTER)
  search_combobox.set("Search By")
  search_combobox.grid(row=0, column=0, padx=20)
  
  search_entry=Entry(search_frame, font=("Times New Roman", 12),bg="lightyellow")
  search_entry.grid(row=0, column=1)
  
  search_button=Button(search_frame, text="Search", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda: search_employee(search_combobox.get(), search_entry.get()))
  search_button.grid(row=0, column=2, padx=20)
  
  show_button=Button(search_frame, text="Show All", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda:show_all(search_entry, search_combobox))
  show_button.grid(row=0, column=3)
  
  employee_treeview = ttk.Treeview(top_frame, columns=("empid", "name", "email", "gender", "dob", "contact",
                                                    "employement_type", "education", "work_shift", "address",
                                                    "doj", "salary", "usertype"), show="headings")
  
  #Tạo thanh cuộn ngang
  x_scroll = ttk.Scrollbar(top_frame, orient=HORIZONTAL, command=employee_treeview.xview)
  employee_treeview.configure(xscrollcommand=x_scroll.set)
  x_scroll.pack(side=BOTTOM, fill=X)

  #Thêm thanh cuộn dọc 
  y_scroll = ttk.Scrollbar(top_frame, orient=VERTICAL, command=employee_treeview.yview)
  employee_treeview.configure(yscrollcommand=y_scroll.set)
  y_scroll.pack(side=RIGHT, fill=Y, pady=(10,0))
  
  employee_treeview.pack(pady=(10,0), fill=BOTH, expand=True)

  employee_treeview.heading('empid', text="EmpId")
  employee_treeview.heading('name', text="Name")
  employee_treeview.heading('email', text="Email")
  employee_treeview.heading('gender', text="Gender")
  employee_treeview.heading('dob', text="Date of Birth")
  employee_treeview.heading('contact', text="Contact")
  employee_treeview.heading('employement_type', text="Employement Type")
  employee_treeview.heading('education', text="Education")
  employee_treeview.heading('work_shift', text="Work Shift")
  employee_treeview.heading('address', text="Address")
  employee_treeview.heading('doj', text="Date of Joining")
  employee_treeview.heading('salary', text="Salary")
  employee_treeview.heading('usertype', text="User Type")
  
  employee_treeview.column('empid', width=60)
  employee_treeview.column('name', width=140)
  employee_treeview.column('email', width=180)  
  employee_treeview.column('gender', width=80)
  employee_treeview.column('dob', width=100)  
  employee_treeview.column('contact', width=100)
  employee_treeview.column('employement_type', width=120)
  employee_treeview.column('education', width=120)
  employee_treeview.column('work_shift', width=100)
  employee_treeview.column('address', width=200)
  employee_treeview.column('doj', width=100)
  employee_treeview.column('salary', width=140)
  employee_treeview.column('usertype', width=100)
  
  # Không cho người dùng kéo dãn cột
  employee_treeview.bind('<Button-1>', lambda e: 'break' if employee_treeview.identify_region(e.x, e.y) == "separator" else None)
  
  treeview_data()
  
  detail_frame = Frame(employee_frame, bg="white")
  detail_frame.place(x=20, y=280, relwidth=1)
  
  empid_label = Label(detail_frame, text="EmpId", font=("Times New Roman", 12), bg="white")
  empid_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
  empid_entry=Entry(detail_frame, font=("Times New Roman", 12), bg="lightyellow")
  empid_entry.grid(row=0, column=1, padx=20, pady=10)
  
  name_label = Label(detail_frame, text="Name", font=("Times New Roman", 12), bg="white")
  name_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")
  name_entry=Entry(detail_frame, font=("Times New Roman", 12), bg="lightyellow")
  name_entry.grid(row=0, column=3, padx=20, pady=10)
  
  email_label = Label(detail_frame, text="Email", font=("Times New Roman", 12), bg="white")
  email_label.grid(row=0, column=4, padx=20, pady=10, sticky="w")
  email_entry=Entry(detail_frame, font=("Times New Roman", 12), bg="lightyellow")
  email_entry.grid(row=0, column=5, padx=20, pady=10)
  
  gender_label = Label(detail_frame, text="Gender", font=("Times New Roman", 12), bg="white")
  gender_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
  gender_combobox=ttk.Combobox(detail_frame, values=("Male", "Female"), font=("Times New Roman", 12), width=18, state="readonly", justify=CENTER)
  gender_combobox.set("Select Gender")
  gender_combobox.grid(row=1, column=1, padx=20, pady=10)
  
  dob_label = Label(detail_frame, text="Date of Birth", font=("Times New Roman", 12), bg="white")
  dob_label.grid(row=1, column=2, padx=20, pady=10, sticky="w")
  dob_date_entry = DateEntry(detail_frame, width=18, font=("Times New Roman", 12), state="readonly", justify=CENTER, date_pattern="dd-mm-yyyy")
  dob_date_entry.grid(row=1, column=3)
  
  contact_label = Label(detail_frame, text="Contact", font=("Times New Roman", 12), bg="white")
  contact_label.grid(row=1, column=4, padx=20, pady=10, sticky="w")
  contact_entry=Entry(detail_frame, font=("Times New Roman", 12), bg="lightyellow")
  contact_entry.grid(row=1, column=5, padx=20, pady=10)
  
  employment_type_label = Label(detail_frame, text="Employment Type", font=("Times New Roman", 12), bg="white")
  employment_type_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
  employment_type_combobox=ttk.Combobox(detail_frame, values=("Full Time", "Part Time", "Casual", "Contract", "Intern"), font=("Times New Roman", 12), width=18, state="readonly", justify=CENTER)
  employment_type_combobox.set("Select Type")
  employment_type_combobox.grid(row=2, column=1, padx=20, pady=10)
  
  education_label = Label(detail_frame, text="Education", font=("Times New Roman", 12), bg="white")
  education_label.grid(row=2, column=2, padx=20, pady=10, sticky="w")
  education_options=["High School", "Diploma", "Bachelor's", "Master's", "PhD"]
  education_combobox=ttk.Combobox(detail_frame, values=education_options, font=("Times New Roman", 12), width=18, state="readonly", justify=CENTER)
  education_combobox.set("Select Education")
  education_combobox.grid(row=2, column=3, padx=20, pady=10)
  
  work_shift_label = Label(detail_frame, text="Work Shift", font=("Times New Roman", 12), bg="white")
  work_shift_label.grid(row=2, column=4, padx=20, pady=10, sticky="w")
  work_shift_combobox=ttk.Combobox(detail_frame, values=("Morning", "Evening", "Night"), font=("Times New Roman", 12), width=18, state="readonly", justify=CENTER)
  work_shift_combobox.set("Select Work Shift")
  work_shift_combobox.grid(row=2, column=5, padx=20, pady=10)
  
  address_label = Label(detail_frame, text="Address", font=("Times New Roman", 12), bg="white")
  address_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
  address_text = Text(detail_frame, font=("Times New Roman", 12), width=20, height=3, bg="lightyellow")
  address_text.grid(row=3, column=1)
  
  doj_label = Label(detail_frame, text="Date of Joining", font=("Times New Roman", 12), bg="white")
  doj_label.grid(row=3, column=2, padx=20, pady=10, sticky="w")
  doj_date_entry = DateEntry(detail_frame, width=18, font=("Times New Roman", 12), state="readonly", justify=CENTER, date_pattern="dd-mm-yyyy")
  doj_date_entry.grid(row=3, column=3)
  
  usertype_label = Label(detail_frame, text="User Type", font=("Times New Roman", 12), bg="white")
  usertype_label.grid(row=4, column=2, padx=20, pady=10, sticky="w")
  usertype_combobox=ttk.Combobox(detail_frame, values=("Admin", "Employee"), font=("Times New Roman", 12), width=18, state="readonly", justify=CENTER)
  usertype_combobox.set("Select User Type")
  usertype_combobox.grid(row=4, column=3, padx=20, pady=10)
  
  salary_label = Label(detail_frame, text="Salary", font=("Times New Roman", 12), bg="white")
  salary_label.grid(row=3, column=4, padx=20, pady=10, sticky="w")
  salary_entry=Entry(detail_frame, font=("Times New Roman", 12), bg="lightyellow")
  salary_entry.grid(row=3, column=5, padx=20, pady=10)
  
  password_label = Label(detail_frame, text="Password", font=("Times New Roman", 12), bg="white")
  password_label.grid(row=4, column=4, padx=20, pady=10, sticky="w")
  password_entry=Entry(detail_frame, font=("Times New Roman", 12), bg="lightyellow")
  password_entry.grid(row=4, column=5, padx=20, pady=10)
  
  button_frame = Frame(employee_frame, bg="white")
  button_frame.place(x=200, y=530)
  
  add_button=Button(button_frame, text="Add", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(), 
                                                                                                                                                      dob_date_entry.get(), contact_entry.get(), employment_type_combobox.get(), 
                                                                                                                                                      education_combobox.get(), work_shift_combobox.get(), address_text.get(1.0, END),
                                                                                                                                                      doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
  add_button.grid(row=0, column=0, padx=20)
  
  update_button=Button(button_frame, text="Update", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda:update_employee(empid_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(), 
                                                                                                                                                      dob_date_entry.get(), contact_entry.get(), employment_type_combobox.get(), 
                                                                                                                                                      education_combobox.get(), work_shift_combobox.get(), address_text.get(1.0, END),
                                                                                                                                                      doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
  update_button.grid(row=0, column=1, padx=20)
  
  delete_button=Button(button_frame, text="Delete", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda:delete_employee(empid_entry.get(), ))
  delete_button.grid(row=0, column=2, padx=20)
  
  clear_button=Button(button_frame, text="Clear", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda:clear_fields(empid_entry, name_entry, email_entry,
                                                                                                                                                                  dob_date_entry,gender_combobox, contact_entry, 
                                                                                                                                                                  employment_type_combobox,education_combobox, work_shift_combobox,
                                                                                                                                                                  address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry, True))
  clear_button.grid(row=0, column=3, padx=20)
  employee_treeview.bind("<ButtonRelease-1>", lambda event:select_data(event,empid_entry, name_entry, email_entry,
                                                          dob_date_entry,gender_combobox, contact_entry, 
                                                          employment_type_combobox,education_combobox, work_shift_combobox,
                                                          address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry))
  create_database_table()