from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry #Nhớ pip install tkcalendar


#Functionality Part
def employee_form():
  global back_image #Biến toàn cục để tránh bị thu khi hàm kết thúc
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
  search_combobox=ttk.Combobox(search_frame, values=('Id','Name', 'Email'), font=("Times New Roman", 12), state="readonly", justify=CENTER)
  search_combobox.set("Search By")
  search_combobox.grid(row=0, column=0, padx=20)
  
  search_entry=Entry(search_frame, font=("Times New Roman", 12),bg="lightyellow")
  search_entry.grid(row=0, column=1)
  
  search_button=Button(search_frame, text="Search", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d")
  search_button.grid(row=0, column=2, padx=20)
  
  show_button=Button(search_frame, text="Show All", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d")
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
  
  doj_label = Label(detail_frame, text="Date of Birth", font=("Times New Roman", 12), bg="white")
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
  
  add_button=Button(button_frame, text="Add", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d")
  add_button.grid(row=0, column=0, padx=20)
  
  update_button=Button(button_frame, text="Update", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d")
  update_button.grid(row=0, column=1, padx=20)
  
  delete_button=Button(button_frame, text="Delete", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d")
  delete_button.grid(row=0, column=2, padx=20)
  
  clear_button=Button(button_frame, text="Clear", font=("Times New Roman", 12), width=10, cursor="hand2", fg="white", bg="#0f4d7d")
  clear_button.grid(row=0, column=3, padx=20)
  
#GUI Part
window = Tk()
window.title("Dashboard")
window.geometry("1270x668")
window.resizable(0,0) #Không cho phép người dùng thay đổi kích thước của sổ
window.config(bg="white")

bg_image=PhotoImage(file=r"helpers/icons/inventory.png")
titleLabel = Label(window, image=bg_image,compound=LEFT, text="  Inventory Management System", font=("Times New Roman", 40, "bold"), bg="#010c48", fg="white",anchor="w", padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

logoutButton = Button(window, text="Logout", font=("Times New Roman", 20, "bold"),fg="#010c48", cursor="hand2")
logoutButton.place(x=1100, y=10)

subtitleLabel = Label(window, text="Welcome Admin\t\t Data: 08-07-2024\t\t Time: 12:36:17 pm", font=("Times New Roman", 15), bg="#4d636d", fg="white")
subtitleLabel.place(x=0, y=70, relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=0,y=102, width=200, height=555)

logoImage=PhotoImage(file=r"helpers/icons/logo.png")
imageLabel = Label(leftFrame, image=logoImage)
imageLabel.grid(row=0, column=0)
imageLabel.pack()

menuLabel = Label(leftFrame, text="Menu", font=("Times New Roman", 20, "bold"), bg="#009688")
menuLabel.pack(fill=X)

employee_icon=PhotoImage(file=r"helpers/icons/employee.png")
employee_button = Button(leftFrame,image=employee_icon, compound=LEFT, text=" Employees", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w", padx=10, command=employee_form)
employee_button.pack(fill=X)

supplier_icon=PhotoImage(file=r"helpers/icons/supplier.png")
supplier_button = Button(leftFrame,image=supplier_icon, compound=LEFT, text="  Supplier", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w")
supplier_button.pack(fill=X)

category_icon=PhotoImage(file=r"helpers/icons/category.png")
category_button = Button(leftFrame,image=category_icon, compound=LEFT, text="  Category", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w")
category_button.pack(fill=X)

product_icon=PhotoImage(file=r"helpers/icons/product.png")
product_button = Button(leftFrame,image=product_icon, compound=LEFT, text="  Product", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w")
product_button.pack(fill=X)

sales_icon=PhotoImage(file=r"helpers/icons/sales.png")
sales_button = Button(leftFrame,image=sales_icon, compound=LEFT, text="  Sales", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w")
sales_button.pack(fill=X)

exit_icon=PhotoImage(file=r"helpers/icons/exit.png")
exit_button = Button(leftFrame,image=exit_icon, compound=LEFT, text="  Exit", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w")
exit_button.pack(fill=X)

#total employee
emp_frame = Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
total_emp_icon=PhotoImage(file=r"helpers/icons/total_employee.png")
total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg="#2C3E50") 
total_emp_icon_label.pack()

total_emp_label = Label(emp_frame, text="Total Employees", font=("Times New Roman", 15, "bold"), bg="#2C3E50", fg="white")
total_emp_label.pack()

total_emp_count_label = Label(emp_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#2C3E50", fg="white")
total_emp_count_label.pack()

#total supplier
sup_frame = Frame(window, bg="#8E44AD", bd=3, relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
total_sup_icon=PhotoImage(file=r"helpers/icons/total_sup.png")
total_sup_icon_label = Label(sup_frame, image=total_sup_icon, bg="#8E44AD") 
total_sup_icon_label.pack()

total_sup_label = Label(sup_frame, text="Total Suppliers", font=("Times New Roman", 15, "bold"), bg="#8E44AD", fg="white")
total_sup_label.pack()

total_sup_count_label = Label(sup_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#8E44AD", fg="white")
total_sup_count_label.pack()

#total category
cat_frame = Frame(window, bg="#27AE60", bd=3, relief=RIDGE)
cat_frame.place(x=400, y=310, height=170, width=280)
total_cat_icon=PhotoImage(file=r"helpers/icons/total_cat.png")
total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg="#27AE60") 
total_cat_icon_label.pack()

total_cat_label = Label(cat_frame, text="Total Categories", font=("Times New Roman", 15, "bold"), bg="#27AE60", fg="white")
total_cat_label.pack()

total_cat_count_label = Label(cat_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#27AE60", fg="white")
total_cat_count_label.pack()

#total product
prod_frame = Frame(window, bg="#E74C3C", bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
total_prod_icon=PhotoImage(file=r"helpers/icons/total_prod.png")
total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg="#E74C3C") 
total_prod_icon_label.pack()

total_prod_label = Label(prod_frame, text="Total Products", font=("Times New Roman", 15, "bold"), bg="#E74C3C", fg="white")
total_prod_label.pack()

total_prod_count_label = Label(prod_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#E74C3C", fg="white")
total_prod_count_label.pack()


#total sales
sales_frame = Frame(window, bg="#6D3CE7", bd=3, relief=RIDGE)
sales_frame.place(x=600, y=495, height=170, width=280)
total_sales_icon=PhotoImage(file=r"helpers/icons/total_sales.png")
total_sales_icon_label = Label(sales_frame, image=total_sales_icon, bg="#6D3CE7") 
total_sales_icon_label.pack(pady=10)

total_sales_label = Label(sales_frame, text="Total Sales", font=("Times New Roman", 15, "bold"), bg="#6D3CE7", fg="white")
total_sales_label.pack()

total_sales_count_label = Label(sales_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#6D3CE7", fg="white")
total_sales_count_label.pack()

window.mainloop()

