# dashboard.py (đã bổ sung nút Tax)
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from employees import employee_form
from supplier import supplier_form
from tax import tax_form
import sys
sys.stdout.reconfigure(encoding='utf-8')
print(1)
window = Tk()
window.title("Dashboard")
window.geometry("1270x668")
window.resizable(0,0)
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
imageLabel.pack()

menuLabel = Label(leftFrame, text="Menu", font=("Times New Roman", 20, "bold"), bg="#009688")
menuLabel.pack(fill=X)

employee_icon=PhotoImage(file=r"helpers/icons/employee.png")
employee_button = Button(leftFrame,image=employee_icon, compound=LEFT, text=" Employees", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w", padx=10, command=lambda:employee_form(window))
employee_button.pack(fill=X)

supplier_icon=PhotoImage(file=r"helpers/icons/supplier.png")
supplier_button = Button(leftFrame,image=supplier_icon, compound=LEFT, text="  Supplier", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w", padx=10, command=lambda: supplier_form(window))
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

tax_icon=PhotoImage(file=r"helpers/icons/tax.png")
tax_button = Button(leftFrame,image=tax_icon, compound=LEFT, text="  Tax", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w", padx=10, command=lambda:tax_form(window))
tax_button.pack(fill=X)

exit_icon=PhotoImage(file=r"helpers/icons/exit.png")
exit_button = Button(leftFrame,image=exit_icon, compound=LEFT, text="  Exit", font=("Times New Roman", 20, "bold"), cursor="hand2",anchor="w")
exit_button.pack(fill=X)

emp_frame = Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
total_emp_icon=PhotoImage(file=r"helpers/icons/total_employee.png")
total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg="#2C3E50")
total_emp_icon_label.pack()

total_emp_label = Label(emp_frame, text="Total Employees", font=("Times New Roman", 15, "bold"), bg="#2C3E50", fg="white")
total_emp_label.pack()

total_emp_count_label = Label(emp_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#2C3E50", fg="white")
total_emp_count_label.pack()

sup_frame = Frame(window, bg="#8E44AD", bd=3, relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
total_sup_icon=PhotoImage(file=r"helpers/icons/total_sup.png")
total_sup_icon_label = Label(sup_frame, image=total_sup_icon, bg="#8E44AD")
total_sup_icon_label.pack()

total_sup_label = Label(sup_frame, text="Total Suppliers", font=("Times New Roman", 15, "bold"), bg="#8E44AD", fg="white")
total_sup_label.pack()

total_sup_count_label = Label(sup_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#8E44AD", fg="white")
total_sup_count_label.pack()

cat_frame = Frame(window, bg="#27AE60", bd=3, relief=RIDGE)
cat_frame.place(x=400, y=310, height=170, width=280)
total_cat_icon=PhotoImage(file=r"helpers/icons/total_cat.png")
total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg="#27AE60")
total_cat_icon_label.pack()

total_cat_label = Label(cat_frame, text="Total Categories", font=("Times New Roman", 15, "bold"), bg="#27AE60", fg="white")
total_cat_label.pack()

total_cat_count_label = Label(cat_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#27AE60", fg="white")
total_cat_count_label.pack()

prod_frame = Frame(window, bg="#E74C3C", bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
total_prod_icon=PhotoImage(file=r"helpers/icons/total_prod.png")
total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg="#E74C3C")
total_prod_icon_label.pack()

total_prod_label = Label(prod_frame, text="Total Products", font=("Times New Roman", 15, "bold"), bg="#E74C3C", fg="white")
total_prod_label.pack()

total_prod_count_label = Label(prod_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#E74C3C", fg="white")
total_prod_count_label.pack()

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